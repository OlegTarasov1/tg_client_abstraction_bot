from .menu_btns.basic_btns import basic_btns
from .menu_btns.authorization import auth_handler
from utils.keyboards.menu_kb import get_menu_kb
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router


menu_router = Router()

menu_router.include_router(auth_handler)
menu_router.include_router(basic_btns)

@menu_router.message(Command("start"))
async def get_menu(
    msg: Message
):
    await msg.answer(
        text = 'Меню',
        reply_markup = await get_menu_kb()
    )