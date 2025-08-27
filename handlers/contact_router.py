from aiogram import Bot, Router,types, F
from aiogram.types import Message, ReplyKeyboardRemove
from databae.orm_query import orm_update_users, orm_get_user_carts, orm_user_info, orm_delete_cart
from sqlalchemy.ext.asyncio import AsyncSession
import os
from dotenv import find_dotenv, load_dotenv
from handlers.matem_text import text_caption

contact_router = Router()


MANAGER=os.getenv("MANAGER")

























@contact_router.message(F.contact)
















@contact_router.message((F.contact) | (F.text))
async def user_contact(message:types.Message, session:AsyncSession, bot:Bot):
    name =message.from_user.full_name
    chat_id = message.from_user.id
    user_id = message.from_user.id
    phone = message.contact.phone_number
    await orm_update_users(session, user_id=user_id, phone=phone)
    await message.answer("Реєстрація пройшла успішно",reply_markup=ReplyKeyboardRemove())  
    cart = await orm_get_user_carts(session, user_id=chat_id)
    user = await orm_user_info(session, chat_id=chat_id)
    for car in cart:
        cart_price = round(car.quantity * car.product.price, 2)
        total_price = round(
        sum(car.quantity * car.product.price for car in cart), 2)
            
            
        text = f"Замовник: {name} Номер телефону: {user.phone}: Назва: {car.product.name}{car.quantity}*{car.product.price} ={cart_price} {car.product.description}, Загальна вартість товарів {total_price}"
        await bot.send_message(chat_id=MANAGER, text=text)
        await orm_delete_cart(session, user_id=user_id)
            
                 
        
