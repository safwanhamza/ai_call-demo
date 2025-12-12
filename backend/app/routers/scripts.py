from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from ..models import Script

router = APIRouter()

# Mock data
mock_scripts = [
    {
        "id": "1",
        "name": "Solar Sales Script V1",
        "content": [{"question": "Hello?", "answer": "Hi, I am calling from Sunrun."}],
        "created_at": datetime.now()
    }
]

@router.get("/", response_model=List[Script])
async def get_scripts():
    return mock_scripts

@router.get("/{script_id}", response_model=Script)
async def get_script(script_id: str):
    for script in mock_scripts:
        if script["id"] == script_id:
            return script
    raise HTTPException(status_code=404, detail="Script not found")

@router.post("/", response_model=Script)
async def create_script(script: Script):
    mock_scripts.append(script.model_dump())
    return script
