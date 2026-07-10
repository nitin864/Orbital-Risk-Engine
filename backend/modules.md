# OrbitShield — Full Module Curriculum & Progress Tracker

Satellite conjunction (collision) assessment system. Live TLE ingestion → SGP4
orbit propagation → close-approach detection → risk scoring → API → dashboard.

**Legend:** ✅ Done · 🔶 Partial · ⬜ Not started

---

## Module 0 — Foundations (Orbital Mechanics Concepts)
**Status: ✅ Done**

- What a satellite/orbit is, gravity vs. velocity
- LEO / MEO / GEO regions
- Space debris, Kessler Syndrome
- What a TLE is, what NORAD IDs are, why TLEs go stale
- Coordinate systems, time systems (conceptual only)

No code — conceptual groundwork only.

---

## Module 1 — Project Architecture
**Status: ✅ Done**

- Full folder structure defined (`api/`, `core/`, `models/`, `database/`,
  `services/`, `orbit/`, `collision/`, `scheduler/`, `utils/`, `config/`)
- Single-responsibility principle per folder
- Data flow diagram: CelesTrak → Download → Parse → DB → Propagation →
  Collision Detection → Risk Score → API → Frontend

**Files:** directory tree only, no logic yet.

---

## Module 2 — Python Environment & Dependency Management
**Status: ✅ Done**

- `.venv` created and activated
- `requirements.txt` — fastapi, uvicorn, httpx, pydantic, skyfield installed
  so far (sqlalchemy, psycopg, apscheduler, pytest, black, ruff pending
  actual use)
- Git initialized, `.gitignore` covering `.venv/`, `__pycache__/`, `cache/`,
  `.env`

---

## Module 3 — Downloading Live TLE Data
**Status: ✅ Done**

**File:** `app/services/tle_downloader.py`

- `TLEDownloader.download()` — fetches raw TLE text from CelesTrak via `httpx`
- Local file cache (`cache/active_satellites.tle`) with 2-hour freshness
  check, to respect CelesTrak's rate limit (hit and solved a real 403 during
  build)
- `TLEDownloader.parse()` — splits raw text into 3-line records, builds
  `Satellite` objects
- Error handling: `IndexError` on malformed records skipped; download
  failures surfaced as `503` via `HTTPException` in the API layer

---

## Module 4 — TLE Field Decoding
**Status: ✅ Done**

**File:** `app/models/satellite.py`

Fields extracted via fixed-width string slicing from `line1`/`line2`:

| Field | Type | Source |
|---|---|---|
| `name` | `str` | record line 0 |
| `line1`, `line2` | `str` | raw TLE lines (kept for propagation) |
| `norad_id` | `str` | `line1[2:7]` |
| `inclination` | `float` | `line2[8:16]` |
| `eccentricity` | `float` | `line2[26:33]`, decimal point inserted manually |
| `mean_motion` | `float` | `line2[52:63]` |
| `orbital_period_minutes` | `float` | derived: `(24*60) / mean_motion` |

Cross-validated NORAD ID consistency between line1/line2 manually during dev.

**Not yet extracted:** epoch, RAAN, argument of perigee, mean anomaly (not
needed until/unless a custom propagator or epoch-freshness check is built —
Skyfield handles these internally via the raw TLE lines).

---

## Module 5 — Orbit Propagation (Skyfield / SGP4)
**Status: ✅ Done**

**File:** `app/orbit/propagator.py`

- `get_current_position(satellite: Satellite) -> dict`
  Builds a Skyfield `EarthSatellite` internally from `line1`/`line2`,
  propagates to `ts.now()`, converts to lat/lon/altitude via
  `wgs84.subpoint()`. Returns plain Python floats (explicitly cast to avoid
  `np.float64` leaking into JSON responses).
- `get_position_at_time(satellite: Satellite, time) -> dict`
  Same, but accepts an arbitrary Skyfield time object — this is the function
  that will drive future collision-window checks.
- Skyfield object (`EarthSatellite`) is fully encapsulated inside this
  module — nothing else in the app touches Skyfield directly, only the
  `Satellite` model.

Verified: current vs. future position outputs are meaningfully different,
confirming real propagation (not a stubbed/static return).

---

## Module 6 — Coordinate Systems (Raw XYZ for Distance Math)
**Status: ✅ Done**

**File:** `app/orbit/propagator.py` (extend) or new `app/orbit/coordinates.py`

- [ ] Extract raw geocentric XYZ position (`geocentric.position.km`) instead
      of lat/lon — needed because spherical coordinates are unsuitable for
      direct distance calculations
- [ ] Understand ECI (Earth-Centered Inertial) vs. ECEF — Skyfield's default
      frame and whether conversion is needed for our use case
- [ ] Function: `get_xyz_at_time(satellite, time) -> (x, y, z)` in km

---

## Module 7 — Database Design (PostgreSQL)
**Status: ✅ Done**

Nothing persists between server restarts currently — this is the biggest
structural gap right now.

- [ ] Choose PostgreSQL vs. SQLite for local dev (recommend starting SQLite
      to avoid infra overhead, migrate later)
- [ ] SQLAlchemy models: `satellites`, `tle_history`, `predictions`,
      `close_approaches`, `risk_scores`
- [ ] `app/database/database.py` — engine, session management
- [ ] Migrate `TLEDownloader` output from in-memory list → DB writes
- [ ] Basic indexing strategy (norad_id as primary lookup key)

---

## Module 8 — Collision Detection Algorithm
**Status: WORKING**

- [ ] Distance function between two satellites at a shared timestamp (uses
      Module 6 output)
- [ ] Brute-force O(n²) pairwise check across all satellites (starting point)
- [ ] Threshold-based close-approach flagging (e.g. < 5 km)
- [ ] Optimization pass: KD-Tree / spatial partitioning to avoid O(n²) at
      scale (~16,000 satellites currently in the active dataset)

---

## Module 9 — Risk Scoring
**Status: ⬜ Not started**

- [ ] Minimum separation distance
- [ ] Relative velocity between the two objects at closest approach
- [ ] Combine into a single risk metric
- [ ] (Optional) object type/mass weighting if data available

---

## Module 10 — FastAPI (Full REST Layer)
**Status: 🔶 Partial**

**Done:**
- `GET /` — health check
- `GET /satellites` — download, parse, return preview (first 5)

**Not done:**
- [ ] `GET /satellites/{norad_id}` — single satellite detail
- [ ] `GET /satellites/{norad_id}/position` — live position via propagator
- [ ] `GET /conjunctions` — close approaches (depends on Module 8)
- [ ] `GET /risks` — risk-scored list (depends on Module 9)
- [ ] OpenAPI documentation polish
- [ ] Pagination on `/satellites` (currently hardcoded preview slice)

---

## Module 11 — React Dashboard
**Status: ⬜ Not started**

- [ ] Satellite table with search/filter
- [ ] Risk leaderboard
- [ ] Charts (altitude distribution, risk over time, etc.)

---

## Module 12 — Three.js Visualization
**Status: ⬜ Not started**

- [ ] Earth render
- [ ] Live satellite position markers
- [ ] Orbit paths
- [ ] Close-approach highlight markers

---

## Module 13 — Background Jobs / Scheduler
**Status: ⬜ Not started**

- [ ] `apscheduler` job: refresh TLE cache automatically every N hours
      (currently only refreshes on-demand when `/satellites` is hit)
- [ ] Scheduled recomputation of predictions/conjunctions once DB exists
- [ ] Old-data cleanup job

---

## Module 14 — Testing
**Status: ⬜ Not started**

- [ ] `test_downloader.py` — mock CelesTrak responses, test caching logic
- [ ] `test_parser.py` — TLE slicing edge cases (malformed records)
- [ ] `test_propagator.py` — known-position regression tests
- [ ] `test_collision.py`, `test_api.py` once those modules exist

---

## Module 15 — Deployment
**Status: ⬜ Not started**

- [ ] Dockerfile (backend)
- [ ] docker-compose (backend + PostgreSQL + frontend)
- [ ] Cloud deployment target decision

---

## Overall Completion Snapshot

| Weighting basis | Estimate |
|---|---|
| By module count (5.5 / 15) | ~35% |
| By actual effort (remaining work is harder: DB, algorithm design, frontend, deployment) | ~15–20% |

**Hardest, most novel part of the whole project — orbit propagation — is done.**
Everything remaining from here is comparatively well-trodden engineering
(CRUD + DB, an algorithm you design yourself, standard frontend work,
containerization) rather than domain-specific physics.

---

## How to resume a session

1. Open this file, check the last `Status` line you updated
2. Paste the relevant module section into a new chat
3. State: "Continuing OrbitShield — here's my progress, let's proceed with Module X"
4. At the end of each work session, update the checkboxes/status above and commit:
   ```bash
   git add OrbitShield_Modules.md
   git commit -m "docs: update progress"
   ```