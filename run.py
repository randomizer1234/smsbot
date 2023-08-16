from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, ConversationHandler

import random
import time

TOKEN = '6324154556:AAHm6c1F-i8lYcT8t4PLETxUbnmyZkZatWk'

CHOOSING, INPUT_AMOUNT = range(2)

def start(update: Update, context: CallbackContext) -> int:
    welcome_message = "Welcome homie to the Crypt0TDS randomization bot"
    keyboard = [
        ['NAME', 'AMOUNT'],
        ['TIME', 'USER INPUT'],
        ['REF']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text(welcome_message, reply_markup=reply_markup)
    return CHOOSING

def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    button_name = query.data
    
    if button_name == 'NAME':
        names = generate_random_names(20)
        query.message.reply_text('\n'.join(names))
    elif button_name == 'AMOUNT':
        context.user_data['selected_button'] = 'AMOUNT'
        query.message.reply_text("Please enter an amount:")
    elif button_name == 'TIME':
        times = generate_random_times(20)
        query.message.reply_text('\n'.join(times))
    elif button_name == 'REF':
        refs = generate_random_refs(20)
        query.message.reply_text('\n'.join(refs))
    elif button_name == 'USER INPUT':
        query.message.reply_text("What do you want to randomize?")
        return INPUT_AMOUNT

def user_input(update: Update, context: CallbackContext) -> int:
    context.user_data['selected_button'] = 'USER INPUT'
    context.user_data['input_type'] = update.message.text
    update.message.reply_text("Please provide more details on how you want to randomize:")
    return INPUT_AMOUNT

# Rest of the code remains the same...

if __name__ == '__main__':
    main()
