from fastapi import FastAPI
from app.services.satellite_query_service import get_all_satellites, get_all_close_approaches
from app.services.satellite_query_service import get_all_satellites

app = FastAPI(title="OrbitShield")


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