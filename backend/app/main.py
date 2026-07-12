from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.services.satellite_query_service import (
    get_all_satellites,
    get_all_close_approaches,
    get_top_risks,
    get_satellite_by_norad_id,
)
from app.scheduler.jobs import start_scheduler
from app.orbit.propagator import get_current_position, get_position_at_time


app = FastAPI(title="OrbitShield")


@app.on_event("startup")
def on_startup():
    start_scheduler()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "OrbitShield backend is running"}


@app.get("/satellites")
def get_satellites():
    satellites = get_all_satellites()
    return {
        "count": len(satellites),
        "satellites": satellites[:15993],
    }


@app.get("/satellites/positions")
def get_all_positions(limit: int = 2000):
    """
    Propagates positions for up to `limit` catalog objects in a single
    request. This exists so the frontend can plot thousands of satellites
    without firing one HTTP request per satellite (which is what was
    capping the globe at ~60 plotted objects before).

    IMPORTANT: this route must stay declared before `/satellites/{norad_id}`
    below — FastAPI matches routes in declaration order, and the dynamic
    `{norad_id}` route would otherwise swallow requests to this path,
    treating "positions" as if it were a NORAD ID (which is exactly the
    "Satellite positions not found" 404 you were seeing).

    `limit` is intentionally capped at 10,000 — propagating the full
    ~16k-object catalog in one synchronous request would make this
    endpoint take too long to be usable interactively. If you want the
    entire catalog live at once, the right next step is a background job
    that recomputes positions on a timer and caches them (e.g. in Redis
    or an in-memory dict), so this endpoint just reads the cache instead
    of propagating on every request.
    """
    limit = max(1, min(limit, 10000))
    satellites = get_all_satellites()[:limit]

    positions = {}
    for sat in satellites:
        try:
            positions[sat.norad_id] = get_current_position(sat)
        except Exception:
            # skip objects that fail to propagate (bad/missing TLE, decayed, etc.)
            continue

    return {"count": len(positions), "positions": positions}


@app.get("/conjunctions")
def get_conjunctions():
    approaches = get_all_close_approaches()

    result = []
    for a in approaches:
        result.append({
            "satellite_1": a.satellite_1_norad_id,
            "satellite_2": a.satellite_2_norad_id,
            "min_distance_km": a.min_distance_km,
            "closest_time_utc": a.closest_time_utc,
        })

    return {
        "count": len(result),
        "conjunctions": result,
    }


@app.get("/risks")
def get_risks(limit: int = 20):
    approaches = get_top_risks(limit)
    result = []
    for a in approaches:
        result.append({
            "satellite_1": a.satellite_1_norad_id,
            "satellite_2": a.satellite_2_norad_id,
            "min_distance_km": a.min_distance_km,
            "closest_time_utc": a.closest_time_utc,
            "risk_score": a.risk_score,
        })
    return {
        "count": len(result),
        "risks": result,
    }


@app.get("/satellites/{norad_id}")
def get_satellite(norad_id: str):
    satellite = get_satellite_by_norad_id(norad_id)

    if satellite is None:
        raise HTTPException(status_code=404, detail=f"Satellite {norad_id} not found")

    return {
        "norad_id": satellite.norad_id,
        "name": satellite.name,
        "inclination": satellite.inclination,
        "eccentricity": satellite.eccentricity,
        "mean_motion": satellite.mean_motion,
        "orbital_period_minutes": satellite.orbital_period_minutes,
    }


@app.get("/satellites/{norad_id}/position")
def get_satellite_position(norad_id: str):
    satellite = get_satellite_by_norad_id(norad_id)

    if satellite is None:
        raise HTTPException(status_code=404, detail=f"Satellite {norad_id} not found")

    position = get_current_position(satellite)

    return {
        "norad_id": satellite.norad_id,
        "name": satellite.name,
        "position": position,
    }


@app.get("/satellites/{norad_id}/orbit-path")
def get_orbit_path(norad_id: str, points: int = 60):
    satellite = get_satellite_by_norad_id(norad_id)

    if satellite is None:
        raise HTTPException(status_code=404, detail=f"Satellite {norad_id} not found")

    from skyfield.api import load
    ts = load.timescale()
    t = ts.now()

    period_minutes = satellite.orbital_period_minutes
    step_minutes = period_minutes / points

    path = []
    for i in range(points):
        time_at_step = t + (i * step_minutes / 1440)
        pos = get_position_at_time(satellite, time_at_step)
        path.append(pos)

    return {"norad_id": norad_id, "points": path}