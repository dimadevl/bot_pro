from aiogram.utils.formatting import Bold, as_list, as_marked_section


categories = ['Чипси', 'Ковбаси', 'Сири']

description_for_info_pages = {
    "main": "Бот ТМ.'🐗Дикий Кабан🐗' вітає вас💋!",
    "about": "Служба замовлень '🐗Дикий кабан🐗'.\nЧас праці 9.00 - 21.00",
    "payment": as_marked_section(
        Bold("Варіанти оплати:"),
        "Картой в боті",
        "При отриманні карта/кеш",
        marker="✅ ",
    ).as_html(),
    "shipping": as_list(
        as_marked_section(
            Bold("Варіанти доставки/замовлення:"),
            "Кур'ер (Мопед вже виїхав🛵)",
            "Самовивіз (Приїхать🚗)",
            "Нова пошта (Відправляю🚕))",
            marker="✅ ",
        ),
        as_marked_section(Bold("Не можна:"),"яхтами⛵","гвинтокрилами🚁","Голубами🐤", marker="❌ "),
        sep="\n----------------------\n",
    ).as_html(),
    'catalog': 'Категорії🐗:',
    'cart': 'В кошику нічого не має!'
}
