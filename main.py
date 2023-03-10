import telebot as tb
from telebot import types
import matplotlib

from objects.user import User
from responders.responders_executor import RespondersExecutor
from responders.responders_importing import *  # Importing responders
from data.config import TOKEN, DESCRIPTION1, DESCRIPTION2, \
    ADMINS, PREMIUM, BLACKLIST, FEEDBACK


class Admin(tb.SimpleCustomFilter):
    key = 'is_admin'
    @staticmethod
    def check(message: tb.types.Message):
        return message.chat.id == ADMINS


# Initializing bot
bot = tb.TeleBot(TOKEN, parse_mode='HTML')
bot.add_custom_filter(Admin())
matplotlib.use('agg')  # Setting not interactive backend



# Saying hello
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: types.Message):
    # Adding user to DB if it is necessary
    User.get_current_user(message.chat.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton(FEEDBACK),
        types.KeyboardButton(BLACKLIST),
        types.KeyboardButton(PREMIUM)
    )

    bot.send_message(message.chat.id, 
        DESCRIPTION1.format(
            user_name=message.from_user.first_name),
        reply_markup=markup)
    bot.send_message(message.chat.id, DESCRIPTION2)



# Admin commands handling
@bot.message_handler(commands=['distribute', 'logs', 'stats'], is_admin=True)
def admin_commands_handling(message: types.Message):
    executor = RespondersExecutor([
        LogsCommand(bot),
        StatsCommand(bot),
        DistributeCommand(bot)
    ])
    executor.execute(message)



# Chat messages handling
@bot.message_handler(content_types=['text', 'photo'])
def messages_handling(message: types.Message):
    executor = RespondersExecutor([
        BlackListMessage(bot),
        FeedbackMessage(bot),
        PremiumMessage(bot),
        AnalyzingMessage(bot)
    ])
    executor.execute(message)



# Inline buttons handling
@bot.callback_query_handler(func=lambda call: True)
def inline_buttons_handling(call: types.CallbackQuery):
    executor = RespondersExecutor([
        BlackListButton(bot),
        ECodeButton(bot),
        PremiumButton(bot),
        AnalyzingButton(bot)
    ])
    executor.execute(call)



bot.infinity_polling()  # Running bot
