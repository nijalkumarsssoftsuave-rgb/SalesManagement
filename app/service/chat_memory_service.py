from app.models.chat_history import ChatHistory

def save_message(db, user_id, role, message):
    db.add(ChatHistory(
        user_id=user_id,
        role=role,
        message=message
    ))
    db.commit()


def load_chat_history(db, user_id, limit=10):
    rows = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.desc())
        .limit(limit)
        .all()
    )

    return list(reversed([
        {"role": r.role, "content": r.message}
        for r in rows
    ]))
