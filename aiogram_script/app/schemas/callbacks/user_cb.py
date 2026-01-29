from aiogram.filters.callback_data import CallbackData


class UserCallback(CallbackData, prefix = "user"):
    action: str = "list"
    offset: int = 0
    limit: int = 8
    renew_data: bool = False
    user_id: int | None = None