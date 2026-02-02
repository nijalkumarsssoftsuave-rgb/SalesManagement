import json
from app.ai.llm import llm

INTENT_PROMPT = """
You are an intent classifier for a sales management system.

User roles:
- MANAGER
- TEAM_MEMBER (salesman)

Possible intents:
- manager_update_task
- salesman_view_task
- salesman_find_shops
- normal_chat

Rules:
- If manager wants to update / change / set today's task → manager_update_task
- If salesman asks about today's task / target → salesman_view_task
- If salesman wants nearby shops / sell / customers → salesman_find_shops
- Otherwise → normal_chat

Return ONLY valid JSON like:
{
  "intent": "<intent_name>"
}
"""

def detect_person_intent(message: str) -> dict:
    res = llm.invoke([
        {"role": "system", "content": INTENT_PROMPT},
        {"role": "user", "content": message}
    ])

    try:
        return json.loads(res.content)
    except Exception:
        return {"intent": "normal_chat"}
