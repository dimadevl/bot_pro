from aiogram.filters import Filter
from aiogram import Router, types, Bot
from string import punctuation
from filters.chat_types_filter import ChatTypeFilter
from aiogram.filters import Command


groop_router = Router()
groop_router.message.filter(ChatTypeFilter(['group', 'supergroup']))
groop_router.edited_message(ChatTypeFilter(['group', 'supergroup']))

restricted_words = {'пиздятина','пидар','хуйло','секс','анал','хуй','пизда','пиздец','ебал','хуйли','сука','уебок','тварь','мразь','писюн','долбаеб','гнида','овца','дятел','тормоз','лох','блядь'}






@groop_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    #просмотреть все данные и свойства полученных объектов
    #print(admins_list)
    # Код ниже это генератор списка, как и этот x = [i for i in range(10)]
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.myadmins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()
    #print(admins_list)













def clean_text(text:str):
    return text.translate(str.maketrans('','', punctuation))


@groop_router.message()
async def mat_handler(message:types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f'{message.from_user.username}, не ругайся матом як криса')
        await message.delete()