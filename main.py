import telebot as tb
from telebot import types
from random import choice
from os import environ
import matplotlib

from objects.user import User
from objects.ecode import ECode
from data_structures import Composition, Photo, Graph
from responders.ecode_resp import ECodeResponder
from responders.premium_resp import PremiumResponder
from responders.additive_resp import AdditiveResponder
from data.config import DESCRIPTION1, DESCRIPTION2, \
    ADMINS, PREMIUMTERMS, PREMIUM, BLACKLIST, FEEDBACK, \
    FEEDBACKTEXT, QUEST1, QUEST2, ECODEDEGREES


class Admin(tb.SimpleCustomFilter):
    key = 'is_admin'
    @staticmethod
    def check(message: tb.types.Message):
        return message.chat.id in ADMINS


bot = tb.TeleBot(environ.get('TG_TOKEN'), parse_mode='HTML')  # initializing bot
bot.add_custom_filter(Admin())
matplotlib.use('agg')  # Setting not interactive backend


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
    DESCRIPTION1.format(user_name=message.from_user.first_name), reply_markup=markup)
    bot.send_message(message.chat.id, DESCRIPTION2)


######################## Admin handlers #########################


@bot.message_handler(commands=['distribute'], is_admin=True)
def distribute_news(message):
    mes = bot.send_message(message.chat.id, 'Пришлите текст рассылки.')
    bot.register_next_step_handler(mes, sending_news)

def sending_news(message):
    amount = 0
    for chat_id in User.get_chats_ids():
        try:
            bot.forward_message(chat_id, message.chat.id, message.id)
            amount += 1
        except:  # User has banned the bot
            pass

    bot.send_message(message.chat.id, 
    f'Количество рассылок: {amount}')


@bot.message_handler(commands=['stats'], is_admin=True)
def get_statistics(message):
    graph = Graph(
        User.get_creating_dates()
        )
    bot.send_photo(message.chat.id, graph.get_image(), 
        f'Всего пользователей: {graph.res}')


@bot.message_handler(commands=['logs'], is_admin=True)
def get_logs(message):
    with open('hello.log', encoding='utf-8') as file:
        if message.text[-1].isdigit():
            lines = int(message.text[6:])
            last_logs = file.readlines()[-lines:]
            bot.send_message(message.chat.id, ''.join(last_logs))
        else:
            bot.send_document(message.chat.id, file)


####################### Message handlers ########################


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
            bot.send_message(message.chat.id, FEEDBACKTEXT)
            bot.send_message(message.chat.id, QUEST1)
            mes = bot.send_message(message.chat.id, QUEST2)
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

    bot.send_message(chat_id, f'Пользователь @{message.from_user.username} оставил отзыв:')
    bot.forward_message(chat_id, message.chat.id, message.id)
    # Maybe add reply from admin in the future

    bot.send_message(message.chat.id, 'Спасибо за отзыв❤️')
    # To user


def composition_analyzer(message, text, user):  # Composition analyzing
    comp = Composition(text)
    comp.set_user(user)
    markup = types.InlineKeyboardMarkup(row_width=1)

    ecode_list = [(el, ECode.get_harm_degree(el)) for el in comp.ecodes]
    ecode_list.sort(key=lambda x: x[1], reverse=True)
    for el, _ in ecode_list:
        markup.add(types.InlineKeyboardButton(
            el + f' ({ECODEDEGREES[ECode.get_harm_degree(el)]})', 
            callback_data=el))  # Creating buttons with short description of ecodes
    
    bot.send_message(message.chat.id, comp.get_evaluation(), reply_markup=markup)


@bot.callback_query_handler(func=lambda c: True)
def inline_buttons_handler(call):  # Inline buttons handling
    if call.message:
        responders = [
            AdditiveResponder(bot),
            ECodeResponder(bot),
            PremiumResponder(bot)
        ]

        for responder in responders:
            if responder.handle(call):
                break


bot.infinity_polling()  # Running
