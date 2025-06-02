import os
from dotenv import load_dotenv
import redis


def connect_to_db():
    load_dotenv()

    db = redis.Redis(
        host=os.getenv("REDIS_PORT"),
        port=int(os.getenv("REDIS_PORT")),
        username=os.getenv("REDIS_USERNAME"),
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True,
    )
    return db
