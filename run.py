from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import random
import time

TOKEN = '6324154556:AAHm6c1F-i8lYcT8t4PLETxUbnmyZkZatWk'

# States for the conversation handler
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

def amount_input(update: Update, context: CallbackContext) -> None:
    input_type = context.user_data.get('input_type', 'UNKNOWN')
    if input_type == 'USER INPUT':
        update.message.reply_text("Please enter your request details:")
    else:
        amount = int(update.message.text)
        random_values = generate_random_values(input_type, 20, amount)
        update.message.reply_text('\n'.join(random_values))
    context.user_data.pop('selected_button', None)
    context.user_data.pop('input_type', None)
    return ConversationHandler.END

def generate_random_names(num_names):
    # Generate random 4-5 character names
    names = ["".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=random.randint(4, 5))) for _ in range(num_names)]
    return names

def generate_random_times(num_times):
    current_time = int(time.time())
    times = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(random.randint(current_time - 300, current_time))) for _ in range(num_times)]
    return times

def generate_random_refs(num_refs):
    # Generate random REF# values
    refs = [f"REF{i}#{random.randint(100, 999)}" for i in range(1, num_refs + 1)]
    return refs

def generate_random_values(input_type, num_values, amount=None):
    if input_type == 'AMOUNT' and amount is not None:
        return [f"£{round(random.uniform(amount, amount + 200), 2)}" for _ in range(num_values)]
    elif input_type == 'USER INPUT':
        # You can implement your own logic here based on user's input
        pass
    return []

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                CallbackQueryHandler(button_handler),
                MessageHandler(Filters.text & ~Filters.command, user_input),
            ],
            INPUT_AMOUNT: [
                MessageHandler(Filters.text & ~Filters.command, amount_input),
            ]
        },
        fallbacks=[],
    )
    
    dispatcher.add_handler(conversation_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
