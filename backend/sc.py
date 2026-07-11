from app.database.database import SessionLocal
from app.database.models import CloseApproachDB

db = SessionLocal()
result = db.query(CloseApproachDB).first()
print(result.satellite_1_norad_id, result.satellite_2_norad_id, result.min_distance_km, result.risk_score, result.closest_time_utc)
db.close()