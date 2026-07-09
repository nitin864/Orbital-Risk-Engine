import time
from pathlib import Path

import httpx

from app.models.satellite import Satellite


class TLEDownloader:
    """
    Responsible for downloading and parsing TLE data from CelesTrak.
    Caches results locally to avoid hitting CelesTrak's rate limit
    (they block repeat downloads within their 2-hour update window).
    """

    URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"

    CACHE_FILE = Path("cache/active_satellites.tle")
    CACHE_MAX_AGE_SECONDS = 2 * 60 * 60  # 2 hours

    def download(self) -> str:
        """
        Returns TLE text, using the local cache if it's still fresh.
        Only calls CelesTrak if the cache is missing or expired.
        """
        if self._cache_is_fresh():
            return self.CACHE_FILE.read_text()

        response = httpx.get(self.URL, timeout=30.0)
        response.raise_for_status()

        self._save_cache(response.text)
        return response.text

    def _cache_is_fresh(self) -> bool:
        if not self.CACHE_FILE.exists():
            return False

        age_seconds = time.time() - self.CACHE_FILE.stat().st_mtime
        return age_seconds < self.CACHE_MAX_AGE_SECONDS

    def _save_cache(self, text: str) -> None:
        self.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.CACHE_FILE.write_text(text)

    def parse(self, raw_text: str) -> list[Satellite]:
        """
        Converts raw TLE text into a list of Satellite objects.
        Each satellite occupies exactly 3 lines: name, line1, line2.
        """
        lines = raw_text.splitlines()
        satellites: list[Satellite] = []

        for i in range(0, len(lines), 3):
            try:
                line1 = lines[i + 1].strip()
                line2 = lines[i + 2].strip()

                satellite = Satellite(
                    name=lines[i].strip(),
                    line1=line1,
                    line2=line2,
                    norad_id=line1[2:7].strip(),
                    inclination=float(line2[8:16].strip()),
                    eccentricity=float("0." + line2[26:33].strip()),
                    mean_motion=float(line2[52:63].strip()),
                    orbital_period_minutes=1440 / float(line2[52:63].strip()),
                )

                satellites.append(satellite)
            except IndexError:
                continue

        return satellites