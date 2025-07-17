from fastapi import APIRouter
from app.api.endpoints import agent

api_router = APIRouter()

# Include the agent router with a specified prefix
api_router.include_router(agent.router, prefix="/agent", tags=["Agent"])
