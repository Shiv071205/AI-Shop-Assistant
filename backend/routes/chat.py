from fastapi import APIRouter
from pydantic import BaseModel
from backend.service.gemini_chain import generate_response

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    history: list[str] = [] 

@router.post("/chat")
async def chat(request: ChatRequest):
    response, updated_history = generate_response(request.query, request.history)
    return {"response": response, "history": updated_history}
