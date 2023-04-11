from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    KeyboardButton
from database import *


def phone_number():
    phone = [
        [KeyboardButton('telefon raqamini yuborish', request_contact=True)]
    ]

    return ReplyKeyboardMarkup(phone, resize_keyboard=True)


def main_button():
    mahsulot = mahsulotlar()
    main_buttons = []
    res = []
    for i in mahsulot:
        res.append(InlineKeyboardButton(f'{i[1]}', callback_data=f'{i[0]}'))
        if len(res) == 2:
            main_buttons.append(res)
            res = []
    if len(res) == 1:
        main_buttons.append(res)
    main_buttons.append(
        [InlineKeyboardButton('Buyurtmalar tarixi', callback_data='buyurtmalar')])
    main_buttons.append([InlineKeyboardButton('Savatchaga o\'tish', callback_data='savatcha')])
    main_buttons.append([InlineKeyboardButton('Karyera', callback_data='karyer')]
                        )

    return InlineKeyboardMarkup(main_buttons)


def taom_turi_button(data):
    buttons = []
    res = []
    for i in data:
        res.append(InlineKeyboardButton(f'{i[2]}', callback_data=f'{i[0]}'))
        if len(res) == 2:
            buttons.append(res)
            res = []
    if len(res):
        buttons.append(res)
    buttons.append([InlineKeyboardButton('Orqaga', callback_data='back')])
    return InlineKeyboardMarkup(buttons)


def back():
    button = [
        [InlineKeyboardButton('Orqaga ', callback_data='back')]
    ]
    return InlineKeyboardMarkup(button)


def add_savat_button():
    button = [
        [InlineKeyboardButton("➖", callback_data='minus'), InlineKeyboardButton("➕", callback_data = 'plus')],
        [InlineKeyboardButton("Savatchaga qo'shish", callback_data="add")],
        [InlineKeyboardButton("Bekor qilish", callback_data= 'cancel')]
    ]

    return InlineKeyboardMarkup(button)
def conf_savat_button():
    button = [
        [InlineKeyboardButton("Buyurtma berish", callback_data="confirm")],
        [InlineKeyboardButton("Savatchani tozalash", callback_data='remove'), InlineKeyboardButton("⏪ back", callback_data = 'back')]

    ]

    return InlineKeyboardMarkup(button)


def location_button():
    phone = [
        [KeyboardButton('Lokatsiyani yuborish', request_location=True)],
        ['Bekor qilish']
    ]

    return ReplyKeyboardMarkup(phone, resize_keyboard=True)