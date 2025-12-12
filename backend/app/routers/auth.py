from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
async def login():
    return {"token": "mock-token-123"}

@router.get("/me")
async def read_users_me():
    return {"username": "admin", "email": "admin@example.com"}
