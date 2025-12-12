from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import dashboard, scripts, auth

app = FastAPI(title="AI Voice Agent API")

# Configure CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(scripts.router, prefix="/api/scripts", tags=["scripts"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "AI Voice Agent API is running"}
