from configs.redis_config import redis_auth_client
import logging
import json



async def set_auth_data(
    data: dict
) -> None:
    """ Установка данных для авторизации """
    try:
        already_existing_data = await retreive_auth_data()
        if not already_existing_data:
            already_existing_data = dict()
        data = json.dumps({**already_existing_data, **data}).encode("utf-8")
        logging.warning(data)
        await redis_auth_client.set(
            name = "auth_data",
            value = data
        )
        
    except Exception as e:
        logging.warning(e)
    
    return None


async def retreive_auth_data(
    *args, **kwargs
) -> dict:
    """ Получение уже внесённых данных для авторизации """
    try:
        data = await redis_auth_client.get(
            name = "auth_data"
        )
        if data:
            data = data.decode("utf-8")
            data = json.loads(data)
            logging.warning(data)
        else:
            data = dict()

    except Exception as e:
        logging.warning(e)
        data = None
    return data 


async def clear_auth_data(
    *args,
    **kwargs
) -> bool:
    """ Удаление данных для авторизации из кэша """
    try:
        await redis_auth_client.delete("auth_data")
        return True
    
    except Exception as e:
        logging.warning(e)
        return False