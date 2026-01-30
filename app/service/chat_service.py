

def unified_chat_service(db, user, message: str):
    state = {
        "message": message,
        "intent": None,
        "location": None,
        "response": None,
        "db": db,
        "user": user,
    }
    #
    # result = chat_graph.invoke(state)
    return "Hi"



# def unified_chat_service(
#     db: Session,
#     user: dict,
#     message: str
# ):
#     # 1️⃣ Detect intent silently
#     intent = detect_intent(message)
#
#     # 2️⃣ If selling intent → structured response
#     if intent.get("intent") == "find_sales_places":
#         return {
#             "parsed_intent": intent,
#             "message": (
#                 "Please share your current location. "
#                 "You can send latitude & longitude or your current address."
#             )
#         }
#
#     # 3️⃣ Otherwise → normal conversational response
#     # reply = normal_chat_response(message)
#     #
#     # return {
#     #     "message": reply
#     # }
#
#     reply = llm.invoke(message).content
#     return {"message": reply}

