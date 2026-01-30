from langchain_openai import ChatOpenAI
from app.ai.llm import llm
import os

def normal_chat_response(message: str) -> str:
    response = llm.invoke(message)
    return response.content
