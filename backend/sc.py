from app.services.satellite_query_service import get_top_risks

results = get_top_risks(5)
print("Count:", len(results))
print(results[0].satellite_1_norad_id, results[0].risk_score)