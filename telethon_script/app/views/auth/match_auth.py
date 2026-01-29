from utils.rmq_comm.rmq_response import rmq_respond
from configs.telethon_config import client
from configs.redis_config import redis_auth_client
from utils.redis_requests.auth_data import set_auth_data, retreive_auth_data
from telethon.errors import SessionPasswordNeededError
import asyncio
import logging
import json
import os



async def auth_connection(
    *args,
    **kwargs
) -> dict:
    """ Функция для установки соединения с сервером телеграмм. """
    response = {
        "status_code": 400,
        "text": "something was wrong with the request"
    }

    try: 
        if not client.is_connected():
            await client.connect()
            response = {
                "status_code": 200,
                "text": "user was successfully connected"
            }

    except Exception as e:
        logging.warning(e)

    return response


async def auth_disconnect(
    *args,
    **kwargs
) -> dict:
    """ Функция для разрыва соединения с сервером телеграмм. """
    response = {
        "status_code": 400,
        "text": "something was wrong with the request"
    }

    if client.is_connected():
        try:
            await client.disconnect()
            response["status_code"] = 200
            response["text"] = "user was disconnected successfully"
        except Exception as e:
            logging.warning(e)
    else:
        response["text"] = "client is not connected"
    
    return response



async def auth_send_code_request(
    data: str
) -> dict:
    """ Отправка запроса на получение кода для авторизации в телеграмм """

    response = {
        "status_code": 400,
        "text": "something was wrong with the request"
    }

    data = await retreive_auth_data()

    if not data.get("phone"):
        response["status_code"] = 406
        response["text"] = "no phone number"

        return response

    if client.is_connected():
        if not await client.is_user_authorized():
            try:
                code_request = await client.send_code_request(
                    data.get("phone")
                )
                await set_auth_data(
                    data = {
                        "phone": data.get("phone"),
                        "phone_code_hash": code_request.phone_code_hash
                    }
                )

                response["status_code"] = 200
                response["text"] = "OK"

            except Exception as e:
                logging.warning(e)
                response["status_code"] = 500
        else:
            response["text"] = "you are already authorized"
    else:
        response["status_code"] = 403
        response["text"] = "user was not connected"
    
    return response


async def auth_set_password(
    data: str
) -> dict:
    """ Отправка пароля для установки в кэш """
    response = {
        "status_code": 400,
        "text": "something was wrong with the request"
    }
    logging.warning(data)

    if data:
        await set_auth_data(
            {
                "password": data
            }
        )
        response["status_code"] = 200
        response["text"] = "OK"
    
    else:
        response["text"] = "No password was provided"

    return response


async def auth_set_phone(
    data: dict
) -> dict:
    response = {
        "status_code": 400,
        "text": "something was wrong with the request"
    }

    if data:
        await set_auth_data(
            {
                "phone": data
            }
        )

        response["status_code"] = 200
        response["text"] = "OK"

    else:
        response["status_code"] = 406
        response["text"] = "no phone number was provided"
    
    return response


async def auth_sign_in(
    data: str
) -> dict:
    response = {
        "status_code": 400,
        "text": "something was wrong with the request"
    }

    if data:
        try:
            auth_data = await retreive_auth_data()
            
            await client.sign_in(
                phone=auth_data.get('phone'),
                phone_code_hash=auth_data.get('phone_code_hash'),
                code=data
            )
        
            response["status_code"] = 200
            response["text"] = "signed in"

        except SessionPasswordNeededError:
            if auth_data.get('password'):
                await client.sign_in(password=auth_data.get('password'))

                response["status_code"] = 200
                response["text"] = "signed in (2fa)"

        except Exception as e:
            logging.warning(e)
    else:
        response["text"] = "no code passed"

    return response


    





# async def telethon_auth(
#     data: dict,
#     # message: aio_pika.abc.AbstractIncomingMessage
# ):
#     """Функция для авторизации"""
#     await asyncio.sleep(1)

#     response = {
#         "status_code": 200,
#         "text": None,
#         "user_id": data.get("sender_id")
#     }

#     match data.get("bot_action", ""):
#         case "connect":
#             if not client.is_connected():
#                 # await message.ack()
#                 logging.warning("connecting...")
#                 await client.connect()
#                 response["text"] = "connected"

#         case "disconnect":
#             if client.is_connected():
#                 # await message.ack()
#                 logging.warning("disconnecting...")
#                 await client.disconnect()
#                 response["text"] = "disconnected"
            
#         case "authorize":
#             logging.warning("authorization...")
#             if not await client.is_user_authorized():
#                 await client.send_code_request(
#                     phone = os.getenv("PHONE_NUMBER")
#                 )
#                 response["text"] = "authorized"
#                 logging.warning("code was sent, supposedly")
#             else:
#                 response["text"] = "something went wrong: possibly, incorrect or insufficient data was passed"
#                 response["status_code"] = 400
#                 logging.warning("the user is authorized")

#         case "enter_code":
#             if client.is_connected() and not await client.is_user_authorized():
#                 # await message.ack()
#                 logging.warning("code entering...")
#                 if not await client.is_user_authorized():
#                     await client.sign_in(
#                         phone = os.getenv("PHONE_NUMBER"),
#                         code = data.get("auth_code"),
#                         password=os.getenv("TG_PSW")
#                     )
#                     response["text"] = "authorized successfully!"
#                 else:
#                     response["text"] = "the user was already authorized"

#         case _:
#             logging.warning("COULD NOT MATCH THE MESSAGE")
#             response = {
#                 "status_code": 400,
#                 "text": json.loads(
#                     data
#                 )
#             }

#     return response

#     # await rmq_respond(
#     #     data = response,
#     #     message = message
#     # )