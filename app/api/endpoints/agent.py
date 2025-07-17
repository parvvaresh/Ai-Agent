from fastapi import APIRouter, Depends, HTTPException
from app.schemas.agent import AskRequest, AskResponse
from app.agent.agent_service import agent_service

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
async def ask_agent(request: AskRequest):
    """
    This endpoint receives a natural language question and returns the agent's response.
    """
    try:
        # Call the agent service to process the request
        response_text = await agent_service.run_agent(request.query, request.session_id)
        return AskResponse(response=response_text, session_id=request.session_id)
    except Exception as e:
        # Handle potential errors during agent execution
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
