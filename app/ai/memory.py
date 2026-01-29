from app.ai.vector_store import conversation_collection

def save_conversation(user_id: int, role: str, message: str, embedding: list):
    conversation_collection.add(
        documents=[message],
        metadatas=[{"user_id": user_id, "role": role}],
        embeddings=[embedding],
        ids=[f"{user_id}-{hash(message)}"]
    )
