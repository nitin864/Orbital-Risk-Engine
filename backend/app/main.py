from fastapi import FastAPI, HTTPException

from app.services.tle_downloader import TLEDownloader

app = FastAPI(title="OrbitShield")


@app.get("/")
def root():
    return {"status": "OrbitShield backend is running"}


@app.get("/satellites")
def get_satellites():
    downloader = TLEDownloader()

    try:
        raw_text = downloader.download()
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to fetch TLE data: {str(e)}"
        )

    satellites = downloader.parse(raw_text)

    return {
        "count": len(satellites),
        "satellites": satellites[:5],
    }