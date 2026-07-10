from app.services.satellite_query_service import get_all_satellites

results = get_all_satellites()
print("Count:", len(results))
print(results[0].name, results[0].norad_id)