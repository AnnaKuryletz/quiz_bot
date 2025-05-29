import os

from dotenv import load_dotenv
import redis


def connect_to_db():
    load_dotenv()
    db = redis.Redis(
        host=os.getenv("REDIS_DATABASE_URL"),
        port=int(os.getenv("REDIS_PORT")),
        decode_responses=True,
        username="default",
        password=os.getenv("REDIS_PASSWORD"),
    )
    return db
