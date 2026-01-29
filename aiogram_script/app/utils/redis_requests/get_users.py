from configs.redis_config import redis_auth_client
from schemas.pydantic.user_schema import UserTemplate
import logging
import json


async def list_users() -> list[UserTemplate | None] | None:
    users = await redis_auth_client.get('list_users')
    if not users:
        logging.warning("users was None")
        return None
    else:
        users = json.loads(
            users.decode("utf-8")
        )
        response = [
            UserTemplate(**i)
            for i in users
        ]
        logging.warning(f"users: {users}")
        return response
