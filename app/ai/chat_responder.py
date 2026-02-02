from langchain_openai import ChatOpenAI
from app.ai.llm import llm
import os

def normal_chat_response(message: str) -> str:
    response = llm.invoke(message)
    return response.content

def narrate_salesman_response(data: dict) -> str:
    prompt = f"""
    You are a sales assistant.

    Explain the following information to the salesman
    in clear, simple language.

    Information:
    {data}

    Rules:
    - Do not invent data
    - Be concise
    - Use bullet points if helpful
    """

    return llm.invoke(prompt).content
