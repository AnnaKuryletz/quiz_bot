from redis_connect import connect_to_db

redis_db = connect_to_db()


def save_question(user_id: int, question: str):
    redis_db.set(f"user:{user_id}:question", question)


def get_question(user_id: int):
    return redis_db.get(f"user:{user_id}:question")
