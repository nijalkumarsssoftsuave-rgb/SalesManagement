import json
from app.ai.llm import llm

INTENT_SYSTEM_MESSAGE = """
You are an intent detector.

If the user wants to SELL a product, return JSON exactly like this:
{
  "intent": "find_sales_places",
  "product": "<product_name>",
  "radius_km": 50
}

If not, return:
{
  "intent": "none"
}

Return ONLY valid JSON. No text.
"""

def detect_intent(message: str) -> dict:
    response = llm.invoke([
        {"role": "system", "content": INTENT_SYSTEM_MESSAGE},
        {"role": "user", "content": message}
    ])

    try:
        intent = json.loads(response.content)
    except Exception:
        return {"intent": "none"}

    # 🔑 NEW LOGIC
    if intent.get("intent") == "find_sales_places" and not intent.get("product"):
        return {
            "intent": "sell_missing_product"
        }

    return intent
