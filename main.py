import telebot as tb
from telebot import types
from random import choice

from objects.user import User
from data_structures import Composition, Photo
from responders.ecode_resp import ECodeResponder
from responders.premium_resp import PremiumResponder
from responders.additive_resp import AdditivesResponder
from data.config import TOKEN, DESCRIPTION, ADMINS, \
    PREMIUMTERMS, PREMIUM, BLACKLIST, FEEDBACK, FEEDBACKTEXT


class Admin(tb.SimpleCustomFilter):
    key = 'is_admin'
    @staticmethod
    def check(message: tb.types.Message):
        return message.chat.id in ADMINS


bot = tb.TeleBot(TOKEN, parse_mode='Markdown')  # initializing bot
bot.add_custom_filter(Admin())


####################### Message handlers ########################


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton(FEEDBACK),
        types.KeyboardButton(BLACKLIST),
        types.KeyboardButton(PREMIUM)
        )

    User.get_current_user(message.chat.id)
    
    bot.send_message(message.chat.id, 
    DESCRIPTION.format(user_name=message.from_user.first_name), reply_markup=markup)


@bot.message_handler(commands=['distribute'], is_admin=True)
def distribute_news(message):
    mes = bot.send_message(message.chat.id, 'Пришлите текст рассылки.')
    bot.register_next_step_handler(mes, sending_news)


def sending_news(message):
    amount = 0
    for chat_id in User.get_chats_ids():
        try:
            bot.send_message(chat_id, message.text)
            amount += 1
        except:  # User has banned the bot
            pass

    bot.send_message(message.chat.id, 
    f'Количество рассылок: {amount}')


@bot.message_handler(commands=['statistics'], is_admin=True)
def get_statistics(message):
    bot.send_message(message.chat.id, 
    f'Количество пользователей: {len(User.get_chats_ids())}')


@bot.message_handler(content_types=['text', 'photo'])
def buttons_handler(message):
    if message.text == BLACKLIST:
        markup = types.InlineKeyboardMarkup(row_width=1)

        markup.add(
            types.InlineKeyboardButton('Получить список', 
            callback_data='get'),
            types.InlineKeyboardButton('Добавить элементы', 
            callback_data='add'),
            types.InlineKeyboardButton('Удалить элементы', 
            callback_data='del')
            )

        bot.send_message(message.chat.id, 'Выбери действие:', reply_markup=markup)

    elif message.text == PREMIUM:
        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton('Отправить заявку', 
            callback_data='premium')
            )

        bot.send_message(message.chat.id, PREMIUMTERMS, reply_markup=markup)

    elif message.text == FEEDBACK:
            mes = bot.send_message(message.chat.id, FEEDBACKTEXT)
            bot.register_next_step_handler(mes, send_feedback)

    elif message.content_type == 'text':  # Getting evalution of text
        if message.text in (FEEDBACK, BLACKLIST, PREMIUM):
            buttons_handler(message)
            return
        user = User.get_current_user(message.chat.id)
        composition_analyzer(message, message.text, user)

    elif message.content_type == 'photo':  # AI
        user = User.get_current_user(message.chat.id)
        image = Photo(bot, message)

        text = image.get_text()
        composition_analyzer(message, text, user)


def send_feedback(message):
    if message.text in (FEEDBACK, BLACKLIST, PREMIUM):
        buttons_handler(message)
        return
    chat_id = choice(ADMINS)  # Getting random admin
    
    if message.content_type == 'photo':
        image = Photo(bot, message)
        bot.send_photo(chat_id, image.image, 
        f'Пользователь @{message.from_user.username} оставил отзыв:\n{message.caption}')
    else:
        bot.send_message(chat_id, f'''
            Пользователь @{message.from_user.username} оставил отзыв:\n{message.text}'''
            )  # Maybe add reply for admin in the future


def composition_analyzer(message, text, user):  # Composition analyzing
    comp = Composition(text)
    comp.set_user(user)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for el in comp.ecodes:
        markup.add(types.InlineKeyboardButton(el, callback_data=el))
    
    bot.send_message(message.chat.id, comp.get_evaluation(), reply_markup=markup)


@bot.callback_query_handler(func=lambda c: True)
def inline_buttons_handler(call):  # Inline buttons handling
    if call.message:
        responders = [
            AdditivesResponder(bot),
            ECodeResponder(bot),
            PremiumResponder(bot)
        ]

        for responder in responders:
            if responder.handle(call):
                break


bot.infinity_polling()  # Running
