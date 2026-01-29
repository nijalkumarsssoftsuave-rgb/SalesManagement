from langchain.prompts import PromptTemplate
from app.ai.llm import llm

INTENT_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""
You are an intent classifier.

User query: "{query}"

Return JSON only:
{{
  "intent": "...",
  "product": "...",
  "radius_km": 50
}}
"""
)

def parse_intent(query: str) -> dict:
    response = llm.invoke(INTENT_PROMPT.format(query=query))
    return response.content
