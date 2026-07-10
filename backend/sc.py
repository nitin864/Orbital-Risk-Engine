from app.database.database import SessionLocal
from app.database.models import SatelliteDB


def upsert_satellite(db, norad_id, name, line1, line2, inclination,
                      eccentricity, mean_motion, orbital_period_minutes):
    """
    Updates a satellite if this norad_id already exists,
    otherwise inserts a new row.
    """
    existing = db.query(SatelliteDB).filter(SatelliteDB.norad_id == norad_id).first()

    if existing:
        existing.name = name
        existing.line1 = line1
        existing.line2 = line2
        existing.inclination = inclination
        existing.eccentricity = eccentricity
        existing.mean_motion = mean_motion
        existing.orbital_period_minutes = orbital_period_minutes
    else:
        new_satellite = SatelliteDB(
            norad_id=norad_id,
            name=name,
            line1=line1,
            line2=line2,
            inclination=inclination,
            eccentricity=eccentricity,
            mean_motion=mean_motion,
            orbital_period_minutes=orbital_period_minutes,
        )
        db.add(new_satellite)

    db.commit()


db = SessionLocal()

upsert_satellite(
    db,
    norad_id="00900",
    name="CALSPHERE 1",
    line1="1 00900U 64063C   26191.15555999  .00000406  00000+0  40394-3 0  9997",
    line2="2 00900  90.2216  72.3098 0023497 220.5925 303.3745 13.76647064 74583",
    inclination=90.9999,
    eccentricity=0.0023416,
    mean_motion=13.76645956,
    orbital_period_minutes=104.6,
)

result = db.query(SatelliteDB).filter(SatelliteDB.norad_id == "00900").first()
print(result.name, result.inclination)

db.close()

db2 = SessionLocal()
count = db2.query(SatelliteDB).filter(SatelliteDB.norad_id == "00900").count()
print("Row count for 00900:", count)
db2.close()