from app.database.database import SessionLocal
from app.database.models import CloseApproachDB

db = SessionLocal()
results = db.query(CloseApproachDB).all()

print("Total close approaches saved:", len(results))

for r in results[:5]:
    print(r.satellite_1_norad_id, r.satellite_2_norad_id, round(r.min_distance_km, 2), r.closest_time_utc)

db.close()