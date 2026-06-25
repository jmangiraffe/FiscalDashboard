from fastapi import APIRouter, HTTPException
from backend.services.db_service import get_latest_snapshot

router = APIRouter()

# Fixed velocity rate per second (can be moved to DB later if it fluctuates)
DEBT_VELOCITY_PER_SECOND = 57000

@router.get("/api/v1/metrics/current")
async def get_current_metrics():
    """
    Returns the latest database snapshot plus the calculation variables
    needed for the frontend Live Ticker.
    """
    data = get_latest_snapshot()
    
    if not data:
        raise HTTPException(status_code=404, detail="No fiscal data found in database.")
        
    return {
        "status": "success",
        "velocity_per_second": DEBT_VELOCITY_PER_SECOND,
        "snapshot": data
    } 
