from configs.rmq_config import rmq_link
from aio_pika.patterns import RPC
import aio_pika
import logging
import json



async def rmq_send_message(
    method_name: str,
    body: dict | None = None
) -> dict | None:
    """
    Функция отправляет в очередь сообщение
    """
    connection = await aio_pika.connect(rmq_link)
    
    async with connection:
        channel = await connection.channel()

        rpc = await RPC.create(channel)

        logging.warning(f"Вызов RPC метода '{method_name}' с данными: {body}")

        try:
            result = await rpc.call(
                method_name, 
                kwargs = {
                    'data': body
                }
            )

            logging.warning(f"результат: \n{result}")
            
            return result

        except Exception as e:
            logging.error(f"Ошибка при вызове RPC: {e}")
            return {
                "status_code": 500,
                "text": str(e)
            }
        


