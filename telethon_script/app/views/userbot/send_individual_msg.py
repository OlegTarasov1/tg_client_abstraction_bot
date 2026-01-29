from utils.telethon_utils.send_message import send_message_to_user
import aio_pika 


async def parse_and_dispatch(
    data: dict
) -> None:
    """
    Функция для парсинга dict и отправки сообщений пользователям.
    (полезно для расширения)
    """

    for i in data.get("ids"):
        await send_message_to_user(
            message_text = data.get("text", " "),
            message_receiver = i
        )