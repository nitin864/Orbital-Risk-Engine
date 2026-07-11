from app.database.database import SessionLocal
from app.database.models import CloseApproachDB

db = SessionLocal()
count = db.query(CloseApproachDB).count()
print("Total close approaches:", count)

top5 = db.query(CloseApproachDB).order_by(CloseApproachDB.risk_score.desc()).limit(5).all()
for r in top5:
    print(r.satellite_1_norad_id, r.satellite_2_norad_id, round(r.min_distance_km, 2), round(r.risk_score, 6))

db.close()