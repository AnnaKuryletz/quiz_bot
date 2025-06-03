import redis


def connect_to_db(host, port, username, password):
    return redis.Redis(
        host=host,
        port=port,
        username=username,
        password=password,
        decode_responses=True,
    )
