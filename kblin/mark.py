from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_keyboard(
    *btns: str,
    placeholder:str = None,
    request_contact:int = None,
    request_location:int = None,
    sizes: tuple [int] = (2,2),
    
):


  keybord = ReplyKeyboardBuilder()

  for index, text in enumerate(btns, start=0):
      if request_contact and request_contact == index:
          keybord.add(KeyboardButton(text=text, request_contact=True))
      elif request_location and request_location == index:
          keybord.add(KeyboardButton(text=text, request_location=True))
      else:
          keybord.add(KeyboardButton(text=text))
  return keybord.adjust(*sizes).as_markup(
      resize_keyboard=True, input_placeholder = placeholder
  )

def order_btns():
    keyboard = ReplyKeyboardBuilder()
    
    keyboard.add(KeyboardButton(text="Поделитись контактом", request_contact=True))
    
    return keyboard.as_markup(resize_keyboard=True)










start_kb = ReplyKeyboardMarkup(
    keyboard=[[
         KeyboardButton(text='Меню🥙'),
    KeyboardButton(text='Корзина🛒'),
    KeyboardButton(text='Акції⭐'),
    KeyboardButton(text='Про нас'),
        
    ]],
    resize_keyboard=True,
    input_field_placeholder="Шо вас цікавить?"
)

start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(
    KeyboardButton(text='Меню🥙'),
    KeyboardButton(text='Кошик🛒'),
    KeyboardButton(text='Акції⭐'),
    KeyboardButton(text='Про нас😍'),
)
start_kb2.adjust(2, 1, 1)

start_kb3 = ReplyKeyboardBuilder()
start_kb3.attach(start_kb2),
start_kb3.row(KeyboardButton(text='Сайт💻'),)\
    
    
order_text = ('Замовлення: # %s\n\n'
              'Статус: #\n\n'
              'Сума замовлення: #\n\n'
              'Склад замволення: #\n\n ')

def batton_cart() -> ReplyKeyboardMarkup:
    keyboars = ReplyKeyboardBuilder()
    keyboars.button(text="◀️Назад"),
    keyboars.button(text="👎Зменшити"),
    keyboars.button(text="👍Збільшити"),
    keyboars.button(text="➖Видалити"),
    return keyboars.as_markup(resize_keyboard=True)

def shoddaun_phone():
    
    keyboard = ReplyKeyboardBuilder()
    
    keyboard.button(text='Поделиться контактом📞', request_contact=True)
    
    return keyboard.as_markup(resize_keyboard=True)