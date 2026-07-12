from fastapi import FastAPI
from app.services.satellite_query_service import get_all_satellites, get_all_close_approaches, get_top_risks,get_satellite_by_norad_id
from app.scheduler.jobs import start_scheduler
from app.orbit.propagator import get_current_position


app = FastAPI(title="OrbitShield")
@app.on_event("startup")
def on_startup():
    start_scheduler()

@app.get("/")
def root():
    return {"status": "OrbitShield backend is running"}


@app.get("/satellites")
def get_satellites():
    satellites = get_all_satellites()
    return {
        "count": len(satellites),
        "satellites": satellites[:5],
    }
    
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