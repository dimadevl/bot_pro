import asyncio
import os
from aiogram import Bot, Dispatcher, types

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from handlers.user_privat import user_private_router
from handlers.user_groop import groop_router
from handlers.admin_private import admin_router
from handlers.contact_router import contact_router

from aiogram.enums import ParseMode
from databae.engine import create_db, drop_db, session_maker
from middleweres.db import DataBaseSession


bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
bot.myadmins_list = []
dp = Dispatcher()


dp.include_router(user_private_router)
dp.include_router(groop_router)
dp.include_router(admin_router)
dp.include_router(contact_router)

async def on_startup(bot):
    await drop_db()
    await create_db()
    
async def on_shutdown(bot):
    print('бот лег')
    
    


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
   # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    # await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    
asyncio.run(main())



