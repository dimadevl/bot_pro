from databae.orm_query import orm_get_user_carts
from sqlalchemy.ext.asyncio import AsyncSession

async def text_caption(session:AsyncSession, user_id, user_text):
    products = await orm_get_user_carts(session, user_id)
    if products:
        text = f"<b>{user_text}</b>"
        product = quantity = count  =  0
        for product, quantity in products:
            count +=1
            product +=1
            quantity +=1
            text += f"{count} {product}\n Колличество: {quantity}\n Стоимсоть: \n\n"
            text += f"Общее количество продуктов: {products}\n Общая стоистость корзины " 
            
            context = (count, text, product)           
            print(text)