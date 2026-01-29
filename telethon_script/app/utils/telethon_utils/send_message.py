from configs.telethon_config import client


async def send_message_to_user(
    message_text: str,
    message_receiver: str | int
) -> None:
    """Функция для отправки сообщения в тг одному пользователю."""

    await client.send_message(
        entity = message_receiver,
        message = message_text
    )
    