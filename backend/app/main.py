from fastapi import FastAPI

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