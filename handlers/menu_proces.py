from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from databae.orm_query import (
    orm_add_to_cart,
    orm_delete_from_cart,
    orm_get_banner,
    orm_get_categories,
    orm_get_products,
    orm_get_user_carts,
    orm_reduce_product_in_cart,
)
from kblin.inline import (
    get_products_btns,
    get_user_cart,
    get_user_catalog_btns,
    get_user_main_btns,
)

from databae.utils import Paginator








async def main_menu(session, level, menu_name, user_id):
    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)
    
    kbds = get_user_main_btns(level=level)

    return image, kbds










async def catalog(session, level, menu_name, user_id):
    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)
    carts = await orm_get_user_carts(session, user_id)
    
        
    categories = await orm_get_categories(session)
    kbds = get_user_catalog_btns(level=level,carta=carts, categories=categories)

    return image, kbds



def pages(paginator: Paginator):
    btns = dict()
    if paginator.has_previous():
        btns["◀ Попер."] = "previous"

    if paginator.has_next():
        btns["Слід. ▶"] = "next"

    return btns


async def products(session, level,menu_name, category, page, user_id):
    products = await orm_get_products(session, category_id=category)

    paginator = Paginator(products, page=page)
    product = paginator.get_page()[0]
    image = InputMediaPhoto(
    media=product.image,
    caption=f"<strong>{product.name}\
        </strong>\n{product.description}\nВартість: {round(product.price, 2)}\n\
            <strong>Товар {paginator.page} из {paginator.pages}</strong>",
            )
    carts = await orm_get_user_carts(session, user_id)
    pagination_btns = pages(paginator)
    kbds = get_products_btns(
            level=level,
            category=category,
            page=page,
            pagination_btns=pagination_btns,
            product_id=product.id,
            carta = carts)
   
        
    return image, kbds


async def carts(session, level, menu_name, page, user_id, product_id):
    if menu_name == "delete":
        await orm_delete_from_cart(session, user_id, product_id)
        if page > 1:
            page -= 1
    elif menu_name == "decrement":
        is_cart = await orm_reduce_product_in_cart(session, user_id, product_id)
        if page > 1 and not is_cart:
            page -= 1
    elif menu_name == "increment":
        await orm_add_to_cart(session, user_id, product_id)

    carts = await orm_get_user_carts(session, user_id)

    if not carts:
        banner = await orm_get_banner(session, "cart")
        image = InputMediaPhoto(
            media=banner.image, caption=f"<strong>{banner.description}</strong>"
        )

        kbds = get_user_cart(
            level=level,
            page=None,
            pagination_btns=None,
            product_id=None,
        )

    else:
        paginator = Paginator(carts, page=page)

        cart = paginator.get_page()[0]

        cart_price = round(cart.quantity * cart.product.price, 2)
        total_price = round(
            sum(cart.quantity * cart.product.price for cart in carts), 2
        )
        image = InputMediaPhoto(
            media=cart.product.image,
            caption=f"<strong>{cart.product.name}</strong>\n{cart.product.price}$ x {cart.quantity} = {cart_price}$\
                    \nТовар {paginator.page} з {paginator.pages} у кошику.\nЗагальна вартість товару {total_price}",
        )

        pagination_btns = pages(paginator)

        kbds = get_user_cart(
            level=level,
            page=page,
            pagination_btns=pagination_btns,
            product_id=cart.product.id,
        )

    return image, kbds

async def get_menu_content(
    session: AsyncSession,
    level: int,
    menu_name: str,
    category: int | None = None,
    page: int | None = None,
    product_id: int | None = None,
    user_id: int | None = None,
    ):
    if level == 0:
        return await main_menu(session, level,menu_name, user_id)
    elif level == 1:
        return await catalog(session, level, menu_name, user_id)
    elif level == 2:
        return await products(session, level,menu_name, category, page, user_id)
    elif level == 3:
        return await carts(session, level, menu_name, page, user_id, product_id)