from configs.telethon_config import client
import logging


async def list_users(
    *args,
    **kwargs
):

    if await client.is_user_authorized(): 
        logging.warning("authorized")
        users = []
        async for dialog in client.iter_dialogs():
            
            
            if dialog.is_user:
                user = dialog.entity
                if not user.bot and not user.is_self:
                    users.append({
                        'id': user.id,
                        'name': f"{user.first_name or ''} {user.last_name or ''}".strip(),
                        'username': user.username
                    })
    
        return users
    else:
        return {
            "status_code": 400,
            "text": "Not auth"
        }