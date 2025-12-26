# chatbot_graph.py - Part of graph module
from langgraph.graph import StateGraph
from graph.state import ChatState
from ai.ollama_llm import llm

def respond(state: ChatState):
    result = llm.invoke(state["input"])
    print(f"output response from the model")
    return {"output": result.content}

builder = StateGraph(ChatState)

print(f"builder is calling :{builder}")
builder.add_node("chat", respond)
builder.set_entry_point("chat")
builder.set_finish_point("chat")

chatbot = builder.compile()

