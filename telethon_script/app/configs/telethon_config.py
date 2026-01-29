from configs.redis_config import redis_auth_client
from telethon import TelegramClient
import json
import os


payload = {
    "device_model": "PC 64bit",
    "system_version": "Windows 11",
    "app_version": "5.0.1",
    "lang_code": "ru",
    "system_lang_code": "ru-RU"
}


client = TelegramClient(
    ".session",
    int(os.getenv("API_ID")),
    os.getenv("API_HASH")
)

