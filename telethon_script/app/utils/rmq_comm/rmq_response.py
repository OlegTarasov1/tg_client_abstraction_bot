import aio_pika
import json


async def rmq_respond(
    data: dict,
    message: aio_pika.abc.AbstractIncomingMessage,
    queue: str = "response_aiogram"
) -> None:
    
    channel = message.channel
    payload = json.dumps(data).encode("utf-8")
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=payload,
            content_type="application/json"
        ),
        routing_key = queue
    )
