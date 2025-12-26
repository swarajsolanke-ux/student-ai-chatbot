# chat.py - Part of routers module
from fastapi import APIRouter
from pydantic import BaseModel
from graph.chatbot_graph import chatbot

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: int
    message: str

@router.post("/chat")
def chat(req: ChatRequest):
    reply = chatbot.invoke({"input": req.message})
    print(f" response received from the model",reply)
  
    return {"reply": reply["output"]}
