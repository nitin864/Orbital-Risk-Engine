from app.collision.risk import calculate_risk_score

print(calculate_risk_score(500, 7.5))    # normal case
print(calculate_risk_score(0, 7.5))      # edge case — should NOT crash
print(calculate_risk_score(0.0001, 7.5)) # near-zero edge case