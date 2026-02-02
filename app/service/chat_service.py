# from fastapi import Depends
#
# from app.ai.llm import llm
# from app.service.chat_memory_service import load_chat_history, save_message
# from app.service.salesmen_service import handle_salesman_task
# from app.utils.chat_intent import is_salesman_task_query
# from app.utils.chat_state import MANAGER_TASK_MODE,SALESMAN_LOCATION_MODE
# import json
# from app.service.manager_services import (
#     handle_manager_task,
#     save_daily_task
# )
# from app.service.salesmen_service import get_today_task_for_salesman
# from app.ai.chat_responder import narrate_salesman_response
# from app.service.sell_plan_service import sell_plan_service
# from app.ai.person_intent_detector import detect_person_intent
#
# def unified_chat_service(db, user, message: str):
#     msg = message.strip().lower()
#
#     intent_data = detect_person_intent(message)
#     intent = intent_data.get("intent")
#
#     # # -------------------------------
#     # # 1️⃣ MANAGER ENTERS TASK MODE
#     # # -------------------------------
#     # if user["role"] == "MANAGER" and "update today's task" in msg:
#     #     return handle_manager_task(db, user)
#
#     # --------------------------------
#     # 2️⃣ MANAGER PROVIDES TASK DETAILS
#     # --------------------------------
#     if user["role"] == "MANAGER" and user["id"] in MANAGER_TASK_MODE:
#         try:
#             parts = [p.strip() for p in message.split(",")]
#
#             if len(parts) != 3:
#                 raise ValueError
#
#             product_name = parts[0]
#             total_quantity = int(parts[1])
#             target_per_person = int(parts[2])
#
#             save_daily_task(
#                 db=db,
#                 manager_id=user["id"],
#                 product_name=product_name,
#                 quantity=total_quantity,
#                 target=target_per_person
#             )
#
#             MANAGER_TASK_MODE.remove(user["id"])
#
#             return {
#                 "message": (
#                     "✅ Today's task updated successfully\n\n"
#                     f"Product: {product_name}\n"
#                     f"Total Quantity: {total_quantity}\n"
#                     f"Target per person: {target_per_person}"
#                 )
#             }
#
#         except Exception:
#             return {
#                 "message": (
#                     "❌ Invalid format.\n\n"
#                     "Please use:\n"
#                     "Product name, total quantity, target per person\n\n"
#                     "Example:\n"
#                     "Iphone 15, 100, 10"
#                 )
#             }
#     if user["role"] == "TEAM_MEMBER" and user["id"] in SALESMAN_LOCATION_MODE:
#             SALESMAN_LOCATION_MODE.remove(user["id"])
#
#             # call your existing routing logic
#             result = sell_plan_service(
#                 db=db,
#                 user=user,
#                 address=message  # or parse lat/lng if provided
#             )
#
#             return result
#
#     # -------------------------------
#     # 3️⃣ SALESMAN: TODAY'S TASK
#     # -------------------------------
#     if user["role"] == "TEAM_MEMBER" and "today's task" in msg.lower():
#         task = get_today_task_for_salesman(db, user)
#
#         # mark that next input should be location
#         SALESMAN_LOCATION_MODE.add(user["id"])
#
#         return {
#             "message": (
#                     narrate_salesman_response(task)
#                     + "\n\n📍 Please share your current location (address or lat,lng) "
#                       "so I can find nearby shops."
#             )
#         }
#
#     # -------------------------------
#     # 4️⃣ SALESMAN: NEARBY SHOPS
#     # -------------------------------
#     if user["role"] == "TEAM_MEMBER" and "nearby shops" in msg:
#         return {
#             "message": "Please share your current location or address"
#         }
#
#     # -------------------------------
#     # 5️⃣ SALESMAN GENERIC TASK FLOW
#     # -------------------------------
#     if user["role"] == "TEAM_MEMBER" and is_salesman_task_query(msg):
#         return handle_salesman_task(db, user)
#
#     # -------------------------------
#     # 6️⃣ NORMAL CHAT (WITH MEMORY)
#     # -------------------------------
#     history = load_chat_history(db, user["id"])
#     messages = history + [{"role": "user", "content": message}]
#     reply = llm.invoke(messages).content
#
#     save_message(db, user["id"], "user", message)
#     save_message(db, user["id"], "assistant", reply)
#
#     return {"message": reply}

from app.ai.llm import llm
from app.service.chat_memory_service import load_chat_history, save_message
from app.service.salesmen_service import handle_salesman_task, get_today_task_for_salesman
from app.utils.chat_state import MANAGER_TASK_MODE, SALESMAN_LOCATION_MODE
from app.service.manager_services import handle_manager_task, save_daily_task
from app.ai.chat_responder import narrate_salesman_response
from app.service.sell_plan_service import sell_plan_service
from app.ai.person_intent_detector import detect_person_intent


def unified_chat_service(db, user, message: str):
    msg = message.strip()

    intent_data = detect_person_intent(message)
    intent = intent_data.get("intent")

    # -------------------------------------------------
    # 1️⃣ MANAGER: ENTER TASK MODE (LLM-INTENT BASED)
    # -------------------------------------------------
    if user["role"] == "MANAGER" and intent == "manager_update_task":
        MANAGER_TASK_MODE.add(user["id"])
        return handle_manager_task(db, user)

    # -------------------------------------------------
    # 2️⃣ MANAGER: PROVIDE TASK DETAILS
    # -------------------------------------------------
    if user["role"] == "MANAGER" and user["id"] in MANAGER_TASK_MODE:
        try:
            parts = [p.strip() for p in message.split(",")]
            if len(parts) != 3:
                raise ValueError

            product_name = parts[0]
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
                    "Use:\n"
                    "Product name, total quantity, target per person\n\n"
                    "Example:\n"
                    "Iphone 15, 100, 10"
                )
            }

    # -------------------------------------------------
    # 3️⃣ SALESMAN: LOCATION FOLLOW-UP
    # -------------------------------------------------
    if user["role"] == "TEAM_MEMBER" and user["id"] in SALESMAN_LOCATION_MODE:
        SALESMAN_LOCATION_MODE.remove(user["id"])
        return sell_plan_service(db=db, user=user, address=message)

    # -------------------------------------------------
    # 4️⃣ SALESMAN: VIEW TODAY'S TASK (LLM-INTENT)
    # -------------------------------------------------
    if user["role"] == "TEAM_MEMBER" and intent == "salesman_view_task":
        task = get_today_task_for_salesman(db, user)
        SALESMAN_LOCATION_MODE.add(user["id"])

        return {
            "message": (
                narrate_salesman_response(task)
                + "\n\n📍 Please share your current location "
                  "(address or lat,lng) to find nearby shops."
            )
        }

    # -------------------------------------------------
    # 5️⃣ SALESMAN: FIND SHOPS DIRECTLY
    # -------------------------------------------------
    if user["role"] == "TEAM_MEMBER" and intent == "salesman_find_shops":
        SALESMAN_LOCATION_MODE.add(user["id"])
        return {
            "message": "📍 Please share your current location or address."
        }

    # -------------------------------------------------
    # 6️⃣ NORMAL CHAT (WITH MEMORY)
    # -------------------------------------------------
    history = load_chat_history(db, user["id"])
    messages = history + [{"role": "user", "content": message}]
    reply = llm.invoke(messages).content

    save_message(db, user["id"], "user", message)
    save_message(db, user["id"], "assistant", reply)

    return {"message": reply}
