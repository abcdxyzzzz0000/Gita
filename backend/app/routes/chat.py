"""Chat endpoints - Bhagavad Gita RAG chatbot."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.chat_service import generate_chat_response, search_passages

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)


class PassageResult(BaseModel):
    text: str
    relevance_score: float


class ChatResponse(BaseModel):
    response: str
    passages: list[PassageResult]


@router.post("/message", response_model=ChatResponse)
async def send_message(payload: ChatRequest):
    """Send a message to the Gita chatbot and get an AI-powered response."""
    try:
        result = await generate_chat_response(payload.message)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_gita(q: str, top_k: int = 5):
    """Search for relevant passages from the Bhagavad Gita."""
    results = search_passages(q, n_results=top_k)
    return results
