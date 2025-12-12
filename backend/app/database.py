import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")

# In a real environment, we would connect here.
# For now, this is a placeholder.
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.voice_agent

# Helper to retrieve user collection
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "full_name": user["full_name"],
        "email": user["email"],
    }
