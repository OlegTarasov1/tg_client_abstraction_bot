from .menu_handler.handle_menu import menu_router
from .helpful.menu import menu_edit_router
from aiogram import Router


master_router = Router()

master_router.include_router(menu_router)
master_router.include_router(menu_edit_router)


