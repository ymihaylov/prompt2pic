import redis


class RedisService:

    def __init__(self, redis_url: str):
        try:
            self.client = redis.from_url(redis_url)
            self.client.ping()
        except redis.ConnectionError as e:
            raise RuntimeError(f"Failed to connect to Redis at {redis_url}: {e}")

    def get_client(self) -> redis.Redis:
        return self.client

    def health_check(self) -> bool:
        try:
            return self.client.ping()
        except:
            return False

    def close(self):
        if self.client:
            self.client.close()
