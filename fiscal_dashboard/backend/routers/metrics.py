from fastapi import APIRouter, HTTPException
from backend.services.db_service import get_latest_snapshot [cite: 70, 71]

router = APIRouter() [cite: 72]

# Fixed velocity rate per second (can be moved to DB later if it fluctuates)
DEBT_VELOCITY_PER_SECOND = 57000 [cite: 73, 74]

@router.get("/api/v1/metrics/current")
async def get_current_metrics():
    """
    Returns the latest database snapshot plus the calculation variables
    needed for the frontend Live Ticker.
    """
    data = get_latest_snapshot() [cite: 76, 81]
    
    if not data:
        raise HTTPException(status_code=404, detail="No fiscal data found in database.") [cite: 82, 83]
        
    return {
        "status": "success",
        "velocity_per_second": DEBT_VELOCITY_PER_SECOND,
        "snapshot": data
    } [cite: 84, 85, 86, 87, 88]
