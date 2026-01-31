from fastapi import Depends

from app.ai.llm import llm
from app.service.chat_memory_service import load_chat_history, save_message
from app.service.salesmen_service import handle_salesman_task
from app.utils.chat_intent import is_salesman_task_query
from app.utils.chat_state import MANAGER_TASK_MODE
import json
from app.service.manager_services import (
    handle_manager_task,
    save_daily_task
)
from database.sqllite_engine import get_db


def unified_chat_service(db, user, message: str):
    msg = message.strip()

    # -------------------------------
    # 1️⃣ MANAGER ENTERS TASK MODE
    # -------------------------------
    if user["role"] == "MANAGER" and "update today's task" in msg.lower():
        return handle_manager_task(db, user)

    # --------------------------------
    # 2️⃣ MANAGER PROVIDES TASK DETAILS
    # --------------------------------
    if user["role"] == "MANAGER" and user["id"] in MANAGER_TASK_MODE:
        try:
            parts = [p.strip() for p in msg.split(",")]

            if len(parts) != 3:
                raise ValueError

            product_name = parts[0]
            # print(product_name)
            # print(parts[1])
            # print(parts[2])
            total_quantity = int(parts[1])
            target_per_person = int(parts[2])

            save_daily_task(
                db=db,
                manager_id=user["id"],
                product_name=product_name,
                quantity=total_quantity,
                target=target_per_person
            )

            MANAGER_TASK_MODE.remove(user["id"])

            return {
                "message": (
                    "✅ Today's task updated successfully\n\n"
                    f"Product: {product_name}\n"
                    f"Total Quantity: {total_quantity}\n"
                    f"Target per person: {target_per_person}"
                )
            }

        except Exception:
            return {
                "message": (
                    "❌ Invalid format.\n\n"
                    "Please use:\n"
                    "Product name, total quantity, target per person\n\n"
                    "Example:\n"
                    "Iphone 15, 100, 10"
                )
            }

    # -------------------------------
    # 3️⃣ SALESMAN MODE
    # -------------------------------
    if user["role"] == "TEAM_MEMBER" and is_salesman_task_query(msg.lower()):
        return handle_salesman_task(db, user)

    # -------------------------------
    # 4️⃣ NORMAL CHAT (WITH MEMORY)
    # -------------------------------
    history = load_chat_history(db, user["id"])
    messages = history + [{"role": "user", "content": message}]
    reply = llm.invoke(messages).content

    save_message(db, user["id"], "user", message)
    save_message(db, user["id"], "assistant", reply)

    return {"message": reply}
