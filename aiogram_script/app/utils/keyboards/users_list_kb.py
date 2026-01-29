from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.pydantic.user_schema import UserTemplate
from schemas.callbacks.user_cb import UserCallback



# Клавиатура с пользователями

async def assemble_kb_listing_users(
    users: list[UserTemplate],
    offset: int = 0,
    limit: int = 8
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    start = offset * limit
    finish = start + limit

    for i, value in enumerate(users[start:finish]):
        if value.is_sent_to:
            pass
        else:
            kb.add(
                InlineKeyboardButton(
                    text = f"{i + 1 + start}. {value.name} ({value.username})",
                    callback_data = UserCallback(
                        action = "send",
                        user_id = value.id,
                        limit = limit,
                        offset = offset,
                    ).pack()
                )
            )

    kb.adjust(1)

    nav = []

    if start > 0:
        
        nav.append(
            InlineKeyboardButton(
                text = "Назад",
                callback_data = UserCallback(
                    limit = limit,
                    offset = offset - 1
                ).pack()
            )
        )

    if finish < len(users):
        nav.append(
            text = "Вперёд",
            callback_data = UserCallback(
                    limit = limit,
                    offset = offset + 1
                ).pack()
        )
    
    kb.row(*nav)

    kb.row(
        InlineKeyboardButton(
            text = "Меню",
            callback_data = "edit_menu"
        )
    )
    
    return kb.as_markup()
