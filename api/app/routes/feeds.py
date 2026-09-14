from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..db import get_db
from ..models import FeedHealthRecord

router = APIRouter(prefix="/feeds", tags=["feeds"])

@router.get("/{source}/status")
def get_feed_status(source: str, db: Session = Depends(get_db)):
    latest = (
        db.query(FeedHealthRecord)
        .filter(FeedHealthRecord.source == source)
        .order_by(desc(FeedHealthRecord.checked_at))
        .first()
    )
    if not latest:
        raise HTTPException(status_code=404, detail=f"no records found for source '{source}'")

    return {
        "source": latest.source,
        "checked_at": latest.checked_at,
        "success": latest.success,
        "latency_ms": latest.latency_ms,
        "is_stale": latest.is_stale,
        "error_message": latest.error_message,
    }

@router.get("/{source}/history")
def get_feed_history(source: str, limit: int = 50, db: Session = Depends(get_db)):
    records = (
        db.query(FeedHealthRecord)
        .filter(FeedHealthRecord.source == source)
        .order_by(desc(FeedHealthRecord.checked_at))
        .limit(limit)
        .all()
    )
    return records