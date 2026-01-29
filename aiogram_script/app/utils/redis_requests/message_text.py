from configs.redis_config import redis_auth_client
import logging


# функция получения сообщения для разсылки

async def get_message_text() -> str | None:
    message_text = await redis_auth_client.get("message_text")

    logging.warning(f"type of message text: {type(message_text)}")

    if not message_text:
        message_text = "..."
    else:

        if type(message_text) == bytes:
            message_text = message_text.decode("utf-8")

    return message_text


# Функция установки нового сообщения для разсылки

async def set_message_text(
    new_message: str
) -> None:
    await redis_auth_client.set(
        "message_text",
        new_message.encode("utf-8")
    )
