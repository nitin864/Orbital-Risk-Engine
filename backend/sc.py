from app.services.satellite_query_service import get_all_satellites
from app.collision.detector import group_satellites_by_band

satellites = get_all_satellites()
sample = satellites[:2000]

bands = group_satellites_by_band(sample)

print("Number of bands:", len(bands))

sizes = sorted(bands.items(), key=lambda item: len(item[1]), reverse=True)
for key, sats in sizes[:5]:
    print(f"Band {key}: {len(sats)} satellites")