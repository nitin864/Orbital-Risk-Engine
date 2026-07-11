# OrbitShield — Progress Log (Updated)

## Overall status: ~25-30% of full project by weighted effort

Modules 0-8 done (with documented limitations). Module 9 ~80% done.
Modules 10-15 mostly not started.

---

## Module 8 — Collision Detection: DONE (with known limitations)

- Distance + closest-approach-over-time math working (app/collision/distance.py)
- Altitude pre-filter via Kepler's 3rd law (app/orbit/propagator.py:
  estimate_altitude_km, get_altitude_band)
- Second filter dimension: inclination banding (get_inclination_band)
- group_satellites_by_band() — keys on (altitude_band, inclination_band) tuple
- scan_for_close_approaches() — scans within-band pairs AND neighboring
  bands (+/-2 in both dimensions) to catch boundary-straddling pairs
- Real bug found + fixed: pairs near band boundaries were being silently
  missed with +/-1 neighbor search (found via CALSPHERE1/2 test case,
  real distance ~1968km but estimated altitudes landed 2 bands apart).
  Fixed by widening to +/-2.
- Known unresolved limitation: one mega-constellation cluster (~973
  satellites, near-identical altitude+inclination, likely Starlink) does
  not get meaningfully split even by narrow bins — confirmed genuine
  physical clustering, not a binning artifact. Real fix would require a
  3rd dimension (RAAN) — not implemented, documented as future work.

---

## Module 9 — Risk Scoring: ~80% done

### Done
- get_xyz_and_velocity_at_time() — position + velocity via Skyfield
  (app/orbit/propagator.py)
- calculate_relative_velocity() — vector difference magnitude
  (app/collision/distance.py)
- calculate_risk_score() — relative_velocity / min_distance, with
  zero-distance safeguard (returns 999999.0 if distance <= 0.001km)
  (app/collision/risk.py)
- Wired into scan_for_close_approaches() and CloseApproachDB
  (risk_score column added, migration = dropped + recreated db)
- Full pipeline tested end-to-end on 2000-satellite real sample:
  731 seconds runtime, 61,983 close approaches found at threshold_km=5000

### BUG FOUND, NOT YET FIXED — data quality issue
Top risk-score results are all min_distance_km = 0.0, risk_score =
999999.0, and involve ISS (25544) paired with 4 different satellites
(25575, 26400, 26700, 36086). Four different satellites all showing
EXACT 0.0km distance from the same object is not physically plausible —
this is almost certainly a propagation failure for one or more
satellites (likely decayed/invalid TLEs still present in CelesTrak's
feed), not a real finding.

Was mid-diagnosis when paused. Next step to confirm: check
geocentric.message (Skyfield sets this on SGP4 propagation errors) for
suspect satellites:

```python
from app.services.satellite_query_service import get_all_satellites
from skyfield.api import EarthSatellite, load

satellites = get_all_satellites()
sat_a = next(s for s in satellites if s.norad_id == "25544")
sat_b = next(s for s in satellites if s.norad_id == "25575")

ts = load.timescale()
t = ts.now()
sky_a = EarthSatellite(sat_a.line1, sat_a.line2, sat_a.name)
sky_b = EarthSatellite(sat_b.line1, sat_b.line2, sat_b.name)
geo_a = sky_a.at(t)
geo_b = sky_b.at(t)

print("sat_a position:", geo_a.position.km)
print("sat_b position:", geo_b.position.km)
print("sat_a message:", geo_a.message)
print("sat_b message:", geo_b.message)
```

If message is non-None for either satellite, that confirms a
propagation error. Fix would be: validate satellites before scanning
(skip any where geocentric.message is not None, or add a sanity check
rejecting min_distance_km values suspiciously close to 0 e.g. < 1km
unless independently verified).

### Not done
- The data-quality fix above (diagnosis started, not completed)
- No /risks API endpoint yet (only /satellites, /conjunctions exist)
- No filtering to exclude decayed/invalid satellites from sync itself
  (arguably belongs further upstream, in sync_service.py or
  tle_downloader.py, not just at scan time)

---

## Not started at all
- Module 10 (rest): /risks endpoint, pagination on /satellites
- Module 11: React dashboard
- Module 12: Three.js visualization
- Module 13: Scheduler (apscheduler) — currently all syncing is manual
  via sc.py, no automatic background refresh
- Module 14: Testing (pytest) — zero test coverage currently
- Module 15: Deployment (Docker, cloud)

---

## How to resume
1. Paste this file into a new chat
2. Say: "Continuing OrbitShield — resume from the Module 9 propagation
   data-quality bug (ISS showing 0.0km distance to 4 satellites)"
3. Run the diagnostic snippet above first to confirm root cause before
   deciding on the fix