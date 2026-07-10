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