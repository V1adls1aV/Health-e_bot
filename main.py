import telebot as tb
from telebot import types

from objects.user import User
from data_structures import Composition, Photo
from responders import AdditivesResponder, ECodeResponder, PremiumResponder
from data.config import TOKEN, DESCRIPTION, ADMINS, \
    PREMIUMTERMS, PREMIUM, CHECKCOMP, BLACKLIST


class Admin(tb.SimpleCustomFilter):
    key = 'is_admin'
    @staticmethod
    def check(message: tb.types.Message):
        return message.chat.id in ADMINS


bot = tb.TeleBot(TOKEN, parse_mode='HTML')  # initializing bot
bot.add_custom_filter(Admin())


####################### Message handlers ########################


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton(CHECKCOMP),
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
    f'''
    Успешно.
    Количество рассылок: {str(amount)}.
    ''')


@bot.message_handler(commands=['statistics'], is_admin=True)
def get_statistics(message):
    bot.send_message(message.chat.id, 
    f'Количество пользователей: {len(User.get_chats_ids())}')


@bot.message_handler(content_types=['text'])
def buttons_handler(message):
    if message.text == CHECKCOMP:
        mes = bot.send_message(message.chat.id, 
        'Пришлите фоторграфию или текст состава.')

        bot.register_next_step_handler(mes, get_composition)

    elif message.text == BLACKLIST:
        markup = types.InlineKeyboardMarkup(row_width=1)

        markup.add(
            types.InlineKeyboardButton('Получить список', 
            callback_data='get'),
            types.InlineKeyboardButton('Добавить элементы', 
            callback_data='add'),
            types.InlineKeyboardButton('Удалить элементы', 
            callback_data='del')
            )

        bot.send_message(message.chat.id, 'Выберете действие:', reply_markup=markup)

    elif message.text == PREMIUM:
        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton('Отправить заявку', 
            callback_data='premium'),
            types.InlineKeyboardButton('Оставить отзыв', 
            callback_data='feedback'),
            )

        bot.send_message(message.chat.id, PREMIUMTERMS, reply_markup=markup)


##################### Composition analyzing #####################


def get_composition(message):
    user = User.get_current_user(message.chat.id)
    if message.content_type == 'text':  # Getting evalution of text
        if message.text.capitalize() not in (BLACKLIST, CHECKCOMP, PREMIUM):
            composition_analyzer(message, message.text, user)

    elif message.content_type == 'photo':  # AI
        image = Photo(bot, message)
        text = image.get_text()
        composition_analyzer(message, text, user)


def composition_analyzer(message, text, user):
    comp = Composition(text)
    comp.set_user(user)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for el in comp.ecodes:
        markup.add(types.InlineKeyboardButton(el, callback_data=el))
    
    bot.send_message(message.chat.id, comp.get_evaluation(), reply_markup=markup)


#################################################################


@bot.callback_query_handler(func=lambda c: True)
def inline_buttons_handler(call):
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
