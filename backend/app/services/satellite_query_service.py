from app.database.database import SessionLocal
from app.database.models import SatelliteDB
from app.database.models import CloseApproachDB

def get_all_satellites():
    
    """
    created this function for fetching data of all satellite from db
    """
    
    db = SessionLocal()
    
    satellites = db.query(SatelliteDB).all()
    
    db.close()
    
    return satellites

def get_all_close_approaches():
    """
    created this function to return all recorded close approaches from the database.
    """
    db = SessionLocal()
    approaches = db.query(CloseApproachDB).all()
    db.close()
    return approaches

def get_top_risks(limit: int = 20):
    """
    creating this function to return close approach, by risk score, giving
    priority to highest first
    """
    db = SessionLocal()
    result = db.query(CloseApproachDB).order_by(CloseApproachDB.risk_score.desc()).limit(limit).all()
    
    db.close()
    return result

def get_satellite_by_norad_id(norad_id: str):
    """
    Returns a single satellite by its NORAD ID, or None if not found.
    """
    db = SessionLocal()
    satellite = db.query(SatelliteDB).filter(SatelliteDB.norad_id == norad_id).first()
    db.close()
    return satellite