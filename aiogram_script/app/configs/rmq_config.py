from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)
from aio_pika import robust_connection


class RabbitMQSettings(BaseSettings):

    RMQ_HOST: str
    RMQ_PORT: int
    RMQ_USER: str
    RMQ_PSW: str

    @property
    def url(self):
        rmq_link = "amqp://"
        rmq_link += self.RMQ_USER
        rmq_link += ":"
        rmq_link += self.RMQ_PSW
        rmq_link += "@"
        rmq_link += self.RMQ_HOST
        rmq_link += ":"
        rmq_link += str(self.RMQ_PORT)
        rmq_link += "/"

        return rmq_link 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


rmq_link = RabbitMQSettings().url





