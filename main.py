from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler, \
    CallbackQueryHandler
from funtions import *

updater = Updater('5050084264:AAFUAvWpsk_SgALOhGKFHObhikkdRrswqzE')

conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', start)
    ],
    states={
        state_phone: [
            MessageHandler(Filters.contact, command_phone)
        ],
        state_taom_tanlash: [
            CallbackQueryHandler(command_taom_tanlash)
        ],
        state_lavash_last: [
            CallbackQueryHandler(command_taom_soni), 
            MessageHandler(Filters.text, command_zakaz_soni)
        ],
        state_add_savat: [
            CallbackQueryHandler(command_add_savatcha)
        ],
        5: [
            CallbackQueryHandler(command_confirm_savatcha)
        ],
        6: [
            MessageHandler(Filters.location, command_location),
            MessageHandler(Filters.regex('^(' + 'Bekor qilish' + ')$'), command_back )
        ]
    },
    fallbacks=[
        CommandHandler('start', start)
    ]
)

updater.dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()
