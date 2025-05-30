def save_question(redis_conn, user_id: int, question: str, platform_prefix: str):
    key = f"{platform_prefix}:user:{user_id}:question"
    redis_conn.set(key, question)


def get_question(redis_conn, user_id: int, platform_prefix: str):
    key = f"{platform_prefix}:user:{user_id}:question"
    return redis_conn.get(key)
