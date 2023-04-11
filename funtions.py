from buttons import *
from database import *

state_phone = 1
state_taom_tanlash = 2
state_lavash_last = 3
state_add_savat = 4
state_confirm_savat = 5
state_zakaz_location = 6


def start(update, context):
    bol = user_check(update.effective_user.id)
    if bol:
        update.message.reply_text("Botimizdan foydalanishingiz mumkin", reply_markup=ReplyKeyboardRemove())
        update.message.reply_photo(photo=open('Images/main.jpg', 'rb'),
                                   caption="Yetkazib berish bo'limi Toshkent shaxrida soat 10:00 dan 3:00 gacha ishlaydi.")
        update.message.reply_text('Buyurtmani birga joylashtiramizmi? 😜😜😜', reply_markup=main_button())
        return state_taom_tanlash
    else:
        update.message.reply_text(
            'Assalomu alaykum botimizga xush kelibsiz ITC FAST FOOD botidan foydalanish uchun  telefon raqamingizni yuborishingiz kerak ',
            reply_markup=phone_number())
        return state_phone


def command_phone(update, context):
    contact = update.effective_message.contact
    phone = contact.phone_number
    id = update.effective_user.id
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    create_users(first_name, last_name, phone, id)
    update.message.reply_text("Botimizdan foydalanishingiz mumkin", reply_markup=ReplyKeyboardRemove())
    update.message.reply_photo(photo=open('Images/main.jpg', 'rb'),
                               caption="Yetkazib berish bo'limi Toshkent shaxrida soat 10:00 dan 3:00 gacha ishlaydi.")
    update.message.reply_text('Buyurtmani birga joylashtiramizmi? 😜😜😜', reply_markup=main_button())
    return state_taom_tanlash


def command_taom_tanlash(update, context):
    query = update.callback_query
    callback = query.data
    if callback == 'savatcha':
        user_id = ret_user_id(update.effective_user.id)[0]
        data = savatcha_user_data(user_id)
        xabar = '<b>Sizning Savatchangiz</b>\n'
        sanoq = 1
        summa = 0
        for i in data:
            mahsulot = one_mahsulot_dat(i[1])[0]
            xabar += f'{sanoq}.<b>{mahsulot[1]}</b>  {i[3]}x{mahsulot[2]} = {i[3] * mahsulot[2]}\n'
            summa += i[3] * mahsulot[2]
            sanoq += 1
        xabar+=f'<b>Jami Summa</b> {summa}'
        query.message.reply_html(xabar, reply_markup=conf_savat_button())
        return state_confirm_savat
    data = mahsulot_turlari_dat(int(callback))
    query.message.delete()
    query.message.reply_photo(open("Images/lavash.jpg", 'rb'), caption=f"Bo'lim: 🌯 {callback}",
                              reply_markup=taom_turi_button(data))
    return state_lavash_last


def command_taom_soni(update, context):
    query = update.callback_query
    callback = query.data
    query.message.delete()
    if callback == 'back':
        query.message.reply_text('Buyurtmani birga joylashtiramizmi? 😜😜😜', reply_markup=main_button())
        return state_taom_tanlash
    data = one_mahsulot_dat(int(callback))[0]
    context.user_data['mahsulot_id'] = data[0]
    if data[-1]:
        query.message.reply_photo(photo=open(data[-1], mode='rb'), caption=f"""Siz tanladingiz: {data[1]} 
Narx: {data[2]} so'm
-----
Iltimos, kerakli bo’lgan miqdorni kiriting!""", reply_markup=back())
    else:
        query.message.reply_text(f"""Siz tanladingiz: {data[1]} 
    Narx: {data[2]} so'm
    -----
    Iltimos, kerakli bo’lgan miqdorni kiriting!""", reply_markup=back())
    return state_lavash_last


def command_zakaz_soni(update, context):
    soni = update.message.text
    data = one_mahsulot_dat(int(context.user_data['mahsulot_id']))[0]

    if soni.isdigit():
        soni = int(soni)
        context.user_data['soni'] = soni
        update.message.reply_html(f"Siz tanlagan mahsulot <b>{data[1]}</b>\n"
                                  f"Narxi: {data[2]}x{soni}={data[2] * soni}\n"
                                  f"Mahsulotni buyurtma qilamizmi?\n"
                                  f"Zakazingizni Savatchaga qo'shing!!!", reply_markup=add_savat_button())
        return state_add_savat
    else:
        update.message.reply_html("Iltimos siz qayta raqamlar bilan kiritib ko'ring: misol uchun <b>12</b>")
        return state_lavash_last


def command_add_savatcha(update, context):
    query = update.callback_query
    callback = query.data
    if callback == 'cancel':
        query.edit_message_text('Buyurtmani birga joylashtiramizmi? 😜😜😜', reply_markup=main_button())
        return state_taom_tanlash
    elif callback == 'plus':
        context.user_data['soni'] += 1
        soni = context.user_data['soni']
        data = one_mahsulot_dat(context.user_data['mahsulot_id'])[0]
        query.edit_message_text(text=f"Siz tanlagan mahsulot <b>{data[1]}</b>\n"
                                     f"Narxi: {data[2]}x{soni}={data[2] * soni}\n"
                                     f"Mahsulotni buyurtma qilamizmi?\n"
                                     f"Zakazingizni Savatchaga qo'shing!!!", parse_mode="HTML",
                                reply_markup=add_savat_button())
        return state_add_savat
    elif callback == 'minus':
        context.user_data['soni'] -= 1
        soni = context.user_data['soni']
        data = one_mahsulot_dat(context.user_data['mahsulot_id'])[0]
        query.edit_message_text(text=f"Siz tanlagan mahsulot <b>{data[1]}</b>\n"
                                     f"Narxi: {data[2]}x{soni}={data[2] * soni}\n"
                                     f"Mahsulotni buyurtma qilamizmi?\n"
                                     f"Zakazingizni Savatchaga qo'shing!!!", parse_mode='HTML',
                                reply_markup=add_savat_button())
        return state_add_savat
    elif callback == 'add':
        soni = context.user_data['soni']
        mah_id = context.user_data['mahsulot_id']
        user_id = ret_user_id(update.effective_user.id)[0]
        add_savatcha(mah_id, user_id=user_id, soni=soni)
        query.edit_message_text('Buyurtmangiz savatchaga muaffaqiyatli qo\'shildi', reply_markup=main_button())
        return state_taom_tanlash


def command_confirm_savatcha(update, context):
    query = update.callback_query
    callback = query.data
    query.message.delete()

    if callback == 'confirm':
        query.message.reply_text("Sizning buyurtmangizni  yakunlash uchun Joylashuvingizni yuboring ", reply_markup=location_button())
        return state_zakaz_location
    elif callback == 'remove':
        user_id = ret_user_id(update.effective_user.id)[0]
        savatcha_user_remove(user_id)
        query.message.reply_text('Sizning savatchangiz muaffaqiyatli tozalandi:', reply_markup=main_button())
        return state_taom_tanlash
    elif callback == 'back':
        query.message.reply_text('Buyurtmani birga joylashtiramizmi? 😜😜😜',reply_markup=main_button())
        return state_taom_tanlash
def command_back(update, context):
    update.message.reply_text('Buyurtmani birga joylashtiramizmi? 😜😜😜',reply_markup=main_button())
    return state_taom_tanlash
from geopy.geocoders import Nominatim
from functools import partial
def command_location(update, context):
    location = update.effective_message.location
    geolocator = Nominatim(user_agent="ruzimurodovnodir66@gmail.com")
    geocode = partial(geolocator.geocode, language="es")
    reverse = partial(geolocator.reverse, language="es")
    manzil = reverse(f"{location['latitude']}, {location['longitude']}")
    update.message.reply_html("Zakaz qabul qilindi", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(f'Sizning manzilingiz: {manzil}\n Zakaz muaffaqiyatli qabul qilindi', reply_markup=main_button())
    return state_taom_tanlash

