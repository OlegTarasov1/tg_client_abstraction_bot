from utils.helpful.rmq_send_message import rmq_send_message
from schemas.fsm_schemas.fsm_auth import AuthorizationFSM
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from schemas.callbacks.auth_cb import AuthCB
from aiogram import Router, F
from utils.keyboards.auth_menu_kb import auth_kb
import logging


auth_handler = Router()


# получение меню авторизации

@auth_handler.callback_query(F.data == "authorization")
async def give_auth_menu(
    cb: CallbackQuery
):
    await cb.message.edit_text(
        text = "Меню авторизации:",
        reply_markup = auth_kb
    )


# Обработка колбэка из меню авторизации

@auth_handler.callback_query(AuthCB.filter())
async def handle_auth_cb(
    cb: CallbackQuery,
    callback_data: AuthCB,
    state: FSMContext
):
    await cb.answer()

    if callback_data.requires_data:
        await state.update_data(data_type = callback_data.data_type)
        await state.set_state(AuthorizationFSM.data)
        await cb.message.answer("\"отмена\" - для отмены ввода.\nОтправляйте номер/код...: ")

    else:
        
        response = await rmq_send_message(
            method_name = callback_data.data_type
        )

        if response.get("status_code") == 200:
            await cb.message.answer("отработало.")
        else:
            await cb.message.answer(f"что-то пошло не так: {response.get('text', 'unknown error')}")



# Обработка обновления данных для авторизации

@auth_handler.message(AuthorizationFSM.data)
async def handle_auth_cb(
    msg: CallbackQuery,
    state: FSMContext
):
    if msg.text.lower().strip() == "отмена":
        await state.clear()
        return None
    
    try:
        data = await state.get_data()

        text = msg.text.strip()
        method = data.get("data_type")
        match method:
            case "auth_set_phone":
                payload = {
                    "phone_number": text
                }
            case "auth_set_password":
                payload = {
                    "password": text
                }
            case "auth_sign_in":
                payload = {
                    "code": text
                }


        response = await rmq_send_message(
            method_name = method,
            body = msg.text.strip()
        )
        await msg.answer(
            text = response["text"]
        )
        await state.clear()
        

    except Exception as e:
        logging.error(e)














# # Начало авторизации

# @auth_handler.callback_query(F.data == "authorization")
# async def start_authorization(
#     cb: CallbackQuery,
#     state: FSMContext
# ):
    # await state.set_state(AuthorizationFSM.number_code)
#     await cb.message.answer("если что не так, пишите: \"отмена\" ")
#     await cb.message.answer("Отправьте код:")

#     response = await rmq_send_message(
#         method_name = "auth",
#         body = {
#             "bot_action": "authorize"
#         }
#     )    


# # Получение кода и конец авторизации

# @auth_handler.message(AuthorizationFSM.number_code)
# async def authorization_code(
#     msg: Message,
#     state: FSMContext
# ):
#     if msg.text.lower().strip() == "отмена":
#         await state.clear()
#         await msg.answer("Ввод отменён")
#     else:
#         try:
#             phone_code = int(msg.text.strip())
#         except:
#             logging.warning(f"что-то не так с кодом: {phone_code}")
#             await msg.answer("Что-то не так с кодом... (видимо не верный: не число)")
#             return None

#         response = await rmq_send_message(
#             method_name = "auth",
#             body = {
#                 "bot_action": "enter_code",
#                 "auth_code": phone_code
#             }
#         )

#         if response.get("status_code") == 200:
#             await state.clear()
#             await msg.answer("Всё, авторизация прошла успешно")
#         else:
#             await msg.answer("видимо, код не правильный")

