from redis.asyncio import Redis
from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    
    REDIS_HOST: str
    REDIS_PORT: int
    # REDIS_USER: str
    # REDIS_PSW: str
    REDIS_V_DB: int = 0

    def __init__(
        self,
        v_db: int = 0,
        *args,
        **kwargs
    ):
        super().__init__()
        self.REDIS_V_DB = v_db

    @property
    def url(self):
        redis_link = {
            "host": self.REDIS_HOST,
            "port": self.REDIS_PORT,
            "db": self.REDIS_V_DB
            # "username": self.REDIS_USER,
            # "password": self.REDIS_PSW
        }

        return redis_link
    

redis_link_auth = RedisConfig().url



# Клиент редис для авторизации

redis_auth_client = Redis(**redis_link_auth)