from aiogram import F, types, Router, Bot
from aiogram.filters import CommandStart

from sqlalchemy.ext.asyncio import AsyncSession
from databae.orm_query import (
    orm_add_to_cart,
    orm_add_user,
    orm_get_user_carts,
    orm_user_info,
    orm_delete_cart,
    orm_finally_add,
    Final
)
from aiogram.types import ReplyKeyboardRemove
from filters.chat_types_filter import ChatTypeFilter
from handlers.menu_proces import get_menu_content
from kblin.inline import MenuCallBack, get_callback_btns
import os
from dotenv import find_dotenv, load_dotenv
from kblin.mark import shoddaun_phone
load_dotenv(find_dotenv())
from aiogram.types import InputMediaPhoto


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))

MANAGER=os.getenv("MANAGER")

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    
    
     
 
 
    media, reply_markup = await get_menu_content(session, level=0, menu_name="main")
    
    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)
    

async def add_to_cart(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
    user = callback.from_user
    await orm_add_user(
        session,
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=None,
    )
    await orm_add_to_cart(session, user_id=user.id, product_id=callback_data.product_id)
    await callback.answer("Товар добавлен у кошик.")


@user_private_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession, bot:Bot):
    if callback_data.menu_name == "order":
        name = callback.from_user.full_name
        chat_id=callback.from_user.id
        message_id = callback.message.message_id
        await bot.delete_message(chat_id = chat_id,message_id=message_id)
       
        user = await orm_user_info(session, chat_id=chat_id)
        if user.phone:
            cart = await orm_get_user_carts(session, user_id=chat_id)
            for car in cart:
                cart_price = round(car.quantity * car.product.price, 2)
                total_price = round(
                sum(car.quantity * car.product.price for car in cart), 2)
            
            
                text = f"Замовник: {name} Номер телефону: {user.phone}: Назва: {car.product.name} Кількість: {car.quantity}*{car.product.price} ={cart_price} {car.product.description}, Загальна вартість товарів {total_price}"
                await bot.send_message(chat_id=MANAGER, text=text)
                await callback.answer()
            await bot.send_message(chat_id=chat_id, text = "Очікуйте зв'язок з оператором - для зворотнього зв'язку 0992220180")
            await orm_delete_cart(session, user_id=chat_id)
            await bot.send_message(chat_id=chat_id, text='Для того шоб розпочати спочатку натисніть команду /start')
        else:
            await bot.send_message(chat_id=chat_id, text='Нажмите на кнопку поделиться контактом для дальнейших манипуляций', reply_markup=shoddaun_phone())
                    
        return    
    
            
        
    if callback_data.menu_name == "add_to_cart":
        await add_to_cart(callback, callback_data, session)
        return

    media, reply_markup = await get_menu_content(
        session,
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        category=callback_data.category,
        page=callback_data.page,
        product_id=callback_data.product_id,
        user_id=callback.from_user.id,
    )

    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()