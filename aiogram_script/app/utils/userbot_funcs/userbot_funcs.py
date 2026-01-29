from utils.userbot_funcs.userbot_manip import send_message


# отправка сообщений списку пользователей

async def send_messages_to_a_list_of_users(
    users: list[dict | str | int],
    message: str
):
    for i in users:
        await send_message(
            # id = i,
            # message = message
        )