from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.callbacks.user_cb import UserCallback


async def get_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.add(
        InlineKeyboardButton(
            text = "Отправка индивидуально сообщений",
            callback_data = UserCallback(
                action = "list",
                renew_data = True
            ).pack()
        )
    )

    kb.add(
        InlineKeyboardButton(
            text = "Смена сообщения",
            callback_data = "change_message"
        )
    )

    kb.add(
        InlineKeyboardButton(
            text = "Авторизация",
            callback_data = "authorization"
        )
    )
    kb.adjust(1)

    return kb.as_markup()