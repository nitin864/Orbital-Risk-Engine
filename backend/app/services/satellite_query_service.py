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