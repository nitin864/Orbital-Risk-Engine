from app.database.database import SessionLocal
from app.database.models import SatelliteDB

def get_all_satellites():
    
    """
    fetching data of all satellite from db
    """
    
    db = SessionLocal()
    
    satellites = db.query(SatelliteDB).all()
    
    db.close()
    
    return satellites