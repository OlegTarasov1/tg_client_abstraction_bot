from aiogram.filters.callback_data import CallbackData


class AuthCB(CallbackData, prefix = "auth"):
    data_type: str
    requires_data: bool = False