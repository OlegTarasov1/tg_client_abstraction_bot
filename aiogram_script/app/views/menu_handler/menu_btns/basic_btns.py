from utils.helpful.rmq_send_message import rmq_send_message
from aiogram.fsm.context import FSMContext
from schemas.callbacks.user_cb import UserCallback
from schemas.pydantic.user_schema import UserTemplate
from configs.redis_config import redis_auth_client
from utils.keyboards.users_list_kb import assemble_kb_listing_users
from utils.redis_requests.message_text import get_message_text, set_message_text
from aiogram.types import CallbackQuery, Message
from utils.redis_requests.get_users import list_users
from aiogram import Router, F
from schemas.fsm_schemas.fsm_set_message import SetNewMessageFSM
import logging


basic_btns = Router()


# Обработка выдачи списка пользователей, которым можно отправлять сообщения

@basic_btns.callback_query(UserCallback.filter(F.action == "list"))
async def users_to_send_messages_to(
    cb: CallbackQuery,
    callback_data: UserCallback
):
    logging.warning("listing...")

    users_list = await list_users()
    
    if callback_data.renew_data or not users_list:
        users_list = await rmq_send_message(
            method_name = "list_users",
            body = None
        )
        logging.warning(users_list[0])
        logging.warning(type(users_list[0]))
        # if not users_list.get('text') == "Not auth":
        if not type(users_list) == dict:

            users_list = [
                UserTemplate.model_validate(i)
                for i in users_list
            ]
            logging.warning("well, we passed that!")
        else:
            await cb.answer("сперва авторизуйтесь")
            return None


    await cb.message.edit_text(
        text = "отправка сообщений:",
        reply_markup = await assemble_kb_listing_users(
            users = users_list,
            offset = callback_data.offset,
            limit = callback_data.limit
        )
    )


# Отправка сообщения пользователю от нажатия на кнопку

@basic_btns.callback_query(UserCallback.filter(F.action == "send"))
async def send_message_by_btn(
    cb: CallbackQuery,
    callback_data: UserCallback
):
    text_message = await get_message_text()

    await rmq_send_message(
        method_name = "send",
        body = {
            "ids": [callback_data.user_id,],
            "text": text_message
        }
    )





# Функция для установки сообщения для рассылки

@basic_btns.callback_query(F.data == "change_message")
async def set_new_message_for_spam(
    cb: CallbackQuery,
    state: FSMContext
):
    await cb.answer()

    await state.set_state(SetNewMessageFSM.new_message_text)
    
    await cb.message.answer(
        text = "Отправьте новый текст сообщения"
    )

# Получение нового сообщения для рассылки и его установка 

@basic_btns.message(SetNewMessageFSM.new_message_text)
async def set_new_message_for_spam(
    msg: Message,
    state: FSMContext
):
    await state.clear()

    await set_message_text(
        new_message = msg.text
    )

    await msg.answer("Новое сообщение установлено")