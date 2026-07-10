from app.services.tle_downloader import TLEDownloader
from app.services.sync_service import sync_satellites_to_db

downloader = TLEDownloader()
raw = downloader.download()
satellites = downloader.parse(raw)

print("Parsed count:", len(satellites))

result = sync_satellites_to_db(satellites)
print(result)