import redis


def connect_to_db():
    db = redis.Redis(
        host='redis-18067.c278.us-east-1-4.ec2.redns.redis-cloud.com',
        port=18067,
        decode_responses=True,
        username="default",
        password="IiRi8LBcDfYOho0qeFP6eJSA2hEXRLP6",
    )
    return db
