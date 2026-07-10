from app.database.database import SessionLocal
from app.database.models import SatelliteDB


def sync_satellites_to_db(satellites: list):
    """
    taking a list of parsed Satellite (Pydantic) objects and
    upserts each one into the database, committing once at the end.
    """
    db = SessionLocal()

    for sat in satellites:
        existing = db.query(SatelliteDB).filter(SatelliteDB.norad_id == sat.norad_id).first()

        if existing:
            existing.name = sat.name
            existing.line1 = sat.line1
            existing.line2 = sat.line2
            existing.inclination = sat.inclination
            existing.eccentricity = sat.eccentricity
            existing.mean_motion = sat.mean_motion
            existing.orbital_period_minutes = sat.orbital_period_minutes
        else:
            new_satellite = SatelliteDB(
                norad_id=sat.norad_id,
                name=sat.name,
                line1=sat.line1,
                line2=sat.line2,
                inclination=sat.inclination,
                eccentricity=sat.eccentricity,
                mean_motion=sat.mean_motion,
                orbital_period_minutes=sat.orbital_period_minutes,
            )
            db.add(new_satellite)

    db.commit()
    db.close()

    return {"synced": len(satellites)}