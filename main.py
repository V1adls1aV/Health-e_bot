import telebot as tb
from telebot import types
from data.config import TOKEN, DESCRIPTION, ADMINNAME


bot = tb.TeleBot(TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton('Проверить состав'),
        types.KeyboardButton('Чёрный список')
    )

    # if message.from_user.username not in db: ...  (Add user)
    
    bot.send_message(message.chat.id, 
    DESCRIPTION.format(message.from_user.username), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def buttons_handler(message):
    if message.text == 'Проверить состав':
        bot.send_message(message.chat.id,
        'Пришлите фоторграфию или текст состава.')

    elif message.text == 'Чёрный список':
        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton('Получить список', callback_data='get'),
            types.InlineKeyboardButton('Добавить элемент', callback_data='add'),
            types.InlineKeyboardButton('Удалить элемент', callback_data='del')
        )

        bot.send_message(message.chat.id, 'Выберете действие:', reply_markup=markup)


@bot.message_handler(content_types=['text', 'image'])
def structure_analyser(message):
    if message.content_type == 'text':  # Call text analyser (with all user exceptions)
        pass
    elif message.content_type == 'image':  # AI
        pass


@bot.callback_query_handler(func=lambda c: True)
def database_handler(call):
    if call.message:
        if call.data == 'get':  # Get all exceptions
            pass
        elif call.data == 'add':  # Add a connection/excepiton
            pass
        elif call.data == 'del':  # Delete connection/exception
            pass


@bot.message_handler(commands=['distribute'])
def distribute_news(message):
    pass
    """
    if message.from_user == ADMINNAME:
        for user in users:
            try:
                bot.send_message(user, message.text)
            except:
                remove_user()
    """


bot.infinity_polling()  # Running
