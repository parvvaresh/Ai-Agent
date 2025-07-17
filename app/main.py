from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings

# Create the main FastAPI app instance
app = FastAPI(
    title="AI Database Agent",
    description="An intelligent agent for interacting with databases using natural language",
    version="1.0.0"
)

# Include the main router in the app with the prefix /api/v1
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint that shows the service health status.
    """
    return {"status": "ok", "message": "AI Database Agent is running!"}
