def is_salesman_task_query(msg: str) -> bool:
    keywords = [
        "task for today",
        "today task",
        "today's task",
        "whats the task",
        "what is the task",
        "whats the task for today"
    ]
    return any(k in msg for k in keywords)
