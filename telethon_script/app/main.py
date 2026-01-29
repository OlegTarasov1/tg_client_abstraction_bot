from views.userbot.send_individual_msg import parse_and_dispatch
# from views.auth.match_auth import telethon_auth
from views.auth.match_auth import (
    auth_sign_in,
    auth_connection,
    auth_disconnect,
    auth_send_code_request,
    auth_set_password,
    auth_set_phone
)
from views.userbot.list_users import list_users
from configs.telethon_config import client
from configs.rmq_config import rmq_link
from aio_pika.patterns import RPC
import aio_pika
import asyncio
import os


async def main():
    connection = await aio_pika.connect_robust(rmq_link)
    
    async with connection:
        channel = await connection.channel()
        # await client.connect()

        await channel.set_qos(prefetch_count = 1)
        rpc = await RPC.create(channel)

        # await rpc.register("auth", telethon_auth)

        # блок авторизации
        await rpc.register("auth_connection", auth_connection) 
        await rpc.register("auth_disconnect", auth_disconnect)
        await rpc.register("auth_sign_in", auth_sign_in)
        await rpc.register("auth_set_phone", auth_set_phone)
        await rpc.register("auth_set_password", auth_set_password)
        await rpc.register("auth_send_code_request", auth_send_code_request)

        # Блок работы с сообщениями
        await rpc.register("send", parse_and_dispatch)
        await rpc.register("list_users", list_users)

        await asyncio.Future() 


if __name__ == "__main__":
    asyncio.run(
        main()
    )