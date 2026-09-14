import os
import sys
import time
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "api"))
from app.db import SessionLocal, engine, Base
from app.models import FeedHealthRecord
from feeds.coingecko import CoinGeckoChecker

POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", 30))

# tracks last seen value per source, in memory, to detect staleness between polls
last_seen_values = {}

def check_feed(checker):
    data, latency_ms, error = checker.fetch()
    success = error is None
    is_stale = False

    if success:
        previous = last_seen_values.get(checker.name)
        if previous is not None and previous == data:
            is_stale = True
        last_seen_values[checker.name] = data

    return FeedHealthRecord(
        source=checker.name,
        checked_at=datetime.utcnow(),
        latency_ms=latency_ms,
        is_stale=is_stale,
        seconds_since_update=None,  # filled in once we track per-source last-change timestamps
        success=success,
        error_message=error,
    )

def run():
    Base.metadata.create_all(bind=engine)
    checkers = [CoinGeckoChecker()]

    while True:
        db = SessionLocal()
        try:
            for checker in checkers:
                record = check_feed(checker)
                db.add(record)
                db.commit()
                print(f"[{record.checked_at}] {record.source}: success={record.success} latency={record.latency_ms:.1f}ms stale={record.is_stale}")
        finally:
            db.close()
        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    run()