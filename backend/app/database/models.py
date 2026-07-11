from sqlalchemy import Column, String, Float, Integer

from app.database.database import Base


class SatelliteDB(Base):
    __tablename__ = "satellites"

    id = Column(Integer, primary_key=True, index=True)
    norad_id = Column(String, unique=True, index=True)
    name = Column(String)
    line1 = Column(String)
    line2 = Column(String)
    inclination = Column(Float)
    eccentricity = Column(Float)
    mean_motion = Column(Float)
    orbital_period_minutes = Column(Float)
    
class CloseApproachDB(Base):
    __tablename__ = "close_approaches"

    id = Column(Integer, primary_key=True, index=True)
    satellite_1_norad_id = Column(String, index=True)
    satellite_2_norad_id = Column(String, index=True)
    min_distance_km = Column(Float)
    closest_time_utc = Column(String)
    risk_score = Column(Float)