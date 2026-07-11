from app.services.satellite_query_service import get_all_satellites
from app.collision.detector import scan_for_close_approaches

satellites = get_all_satellites()
sample = satellites[:100]

scan_for_close_approaches(sample, hours=2, step_minutes=15, threshold_km=5000)
print("Scan complete")