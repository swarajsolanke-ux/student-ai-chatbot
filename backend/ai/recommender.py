
from ai.ollama_llm import llm
from ai.prompts import RECOMMEND_PROMPT

def explain(universities):
    print(f"recommender explain function is calling",universities)
    return llm.invoke(
        RECOMMEND_PROMPT.format(universities=universities)
    ).content
