import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import time
from feeds.coingecko import CoinGeckoChecker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://radar:radar_dev_password@localhost:5432/cluster_radar")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class FeedHealthRecord(Base):
    __tablename__ = "feed_health_records"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True, nullable=False)
    checked_at = Column(DateTime, default=datetime.utcnow, index=True)
    latency_ms = Column(Float, nullable=True)
    is_stale = Column(Boolean, default=False)
    seconds_since_update = Column(Float, nullable=True)
    success = Column(Boolean, default=True)
    error_message = Column(String, nullable=True)

POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", 30))
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
        seconds_since_update=None,
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