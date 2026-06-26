from fastapi import APIRouter, HTTPException
from backend.services.db_service import get_latest_snapshot
import httpx

router = APIRouter()

GROWTH_API_URL = "https://www.usdebtclock.org/api/gpt/growth-rate"

@router.get("/api/v1/metrics/current")
async def get_current_metrics():
    """Fetches the latest database cache layer row and pairs it with live API velocity."""
    data = get_latest_snapshot()

    if not data: 
        raise HTTPException(status_code=404, detail="No fiscal data found in database.")

    # Dynamically fetch the current velocity vector from the external API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(GROWTH_API_URL, timeout=5.0)
            velocity_rate = response.json().get("per_second", 532407)
    except Exception:
        velocity_rate = 532407 # Resilient fallback configuration

    return {
        "status": "success",
        "velocity_per_second": velocity_rate,
        "snapshot": data
    }
