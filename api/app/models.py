from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from .db import Base

class FeedHealthRecord(Base):
    __tablename__ = "feed_health_records"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True, nullable=False)  # e.g. "coingecko", "alphavantage"
    checked_at = Column(DateTime, default=datetime.utcnow, index=True)
    latency_ms = Column(Float, nullable=True)  # response time of the poll
    is_stale = Column(Boolean, default=False)  # true if data hasn't changed since last poll
    seconds_since_update = Column(Float, nullable=True)  # gap since feed's own last data timestamp
    success = Column(Boolean, default=True)  # false if the poll itself failed
    error_message = Column(String, nullable=True)