from app.database.database import SessionLocal
from app.database.models import CloseApproachDB

db = SessionLocal()
count = db.query(CloseApproachDB).count()
print("Total close approaches:", count)

# specifically check no 0.0km entries snuck through
zero_km = db.query(CloseApproachDB).filter(CloseApproachDB.min_distance_km <= 0.5).count()
print("Entries with distance <= 0.5km (should be 0):", zero_km)

top5 = db.query(CloseApproachDB).order_by(CloseApproachDB.risk_score.desc()).limit(5).all()
for r in top5:
    print(r.satellite_1_norad_id, r.satellite_2_norad_id, round(r.min_distance_km, 2), round(r.risk_score, 6))

db.close()