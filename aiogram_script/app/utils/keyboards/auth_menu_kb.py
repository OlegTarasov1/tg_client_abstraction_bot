from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.callbacks.auth_cb import AuthCB


auth_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text = "Установить соединение",
                callback_data = AuthCB(
                    data_type = "auth_connection",
                    requires_data = False
                ).pack()
            ),
            InlineKeyboardButton(
                text = "Разорвать соединение",
                callback_data = AuthCB(
                    data_type = "auth_disconnect",
                    requires_data = False
                ).pack()
            ),
            InlineKeyboardButton(
                text = "Запросить код",
                callback_data = AuthCB(
                    data_type = "auth_send_code_request",
                    requires_data = False
                ).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text = "Установить номер",
                callback_data = AuthCB(
                    data_type = "auth_set_phone",
                    requires_data = True
                ).pack()
            ),
            InlineKeyboardButton(
                text = "Установить пароль",
                callback_data = AuthCB(
                    data_type = "auth_set_password",
                    requires_data = True
                ).pack()
            ),
            InlineKeyboardButton(
                text = "Авторизация",
                callback_data = AuthCB(
                    data_type = "auth_sign_in",
                    requires_data = True
                ).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text = "Меню",
                callback_data = "edit_menu"
            )
        ],
    ]
)