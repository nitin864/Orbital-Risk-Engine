from datetime import datetime, timedelta

from app.services.tle_downloader import TLEDownloader
from app.services.sync_service import sync_satellites_to_db
from app.services.satellite_query_service import get_all_satellites
from app.collision.detector import scan_for_close_approaches
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()

def sync_job():
    """
    created this for downloading fresh TLE data,
    and sync it to database
    """
    
    downloader = TLEDownloader()
    raw = downloader.download()
    satellites = downloader.parse(raw)
    
    result = sync_satellites_to_db(satellites)
    
def scan_job():
    """
    this function is responsible for running collision detection
    and risk_scoring against current DB Data.
    """
    
    satellites = get_all_satellites()
    scan_for_close_approaches(satellites, hours=2, step_minutes=15, threshold_km=100)
    print("Scan job complete")
 


def start_scheduler():
    """
    created this function to registers sync_job and scan_job to run automatically on a schedule,
    then starts the scheduler running in the background.
    """
    # sync_job is cheap (just parses/upserts TLEs), fine to run immediately.
    scheduler.add_job(sync_job, "interval", hours=2, id="sync_job")

    # scan_job does an O(n^2)-ish collision sweep across the whole catalog —
    # heavy enough to peg the CPU and starve the API for a while. APScheduler
    # runs interval jobs immediately by default, which meant every server
    # restart triggered a huge synchronous scan right as the frontend started
    # hitting /satellites/positions, causing intermittent 500s. Delay the
    # first run so the server is idle and responsive on startup.
    scheduler.add_job(
        scan_job,
        "interval",
        hours=2,
        id="scan_job",
        next_run_time=datetime.now() + timedelta(minutes=3),
    )
    scheduler.start()
    print("Scheduler started: sync and scan jobs registered")