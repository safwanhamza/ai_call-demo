from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

# Mock data
mock_stats = {
    "total_calls": 450,
    "success_rate": 0.75,
    "appointments_scheduled": 42,
    "failed_calls": 12,
}

@router.get("/stats")
async def get_stats():
    return mock_stats

@router.get("/calls")
async def get_recent_calls():
    return [
        {
            "id": "1",
            "agent_id": "agent_01",
            "lead_phone": "+15551234567",
            "status": "completed",
            "duration": 120,
            "timestamp": datetime.now().isoformat(),
            "summary": "Customer interested in solar."
        },
        {
            "id": "2",
            "agent_id": "agent_01",
            "lead_phone": "+15559876543",
            "status": "no-answer",
            "duration": 0,
            "timestamp": datetime.now().isoformat(),
            "summary": "Voicemail left."
        }
    ]
