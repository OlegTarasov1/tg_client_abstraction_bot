from utils.keyboards.menu_kb import get_menu_kb
from aiogram.types import CallbackQuery
from aiogram import Router, F


menu_edit_router = Router()


@menu_edit_router.callback_query(F.data == "edit_menu")
async def edit_menu(
    cb: CallbackQuery
):
    await cb.message.edit_text(
        text = "Меню:",
        reply_markup = await get_menu_kb()
    )