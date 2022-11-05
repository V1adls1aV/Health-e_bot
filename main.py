import telebot as tb
from telebot import types
from db_objects import User, Additive
from data.config import TOKEN, DESCRIPTION, ADMINS


class Admin(tb.SimpleCustomFilter):
    key = 'is_admin'
    @staticmethod
    def check(message: tb.types.Message):
        return message.chat.id in ADMINS


bot = tb.TeleBot(TOKEN, parse_mode='HTML')  # initializing bot
bot.add_custom_filter(Admin())


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton('Проверить состав'),
        types.KeyboardButton('Чёрный список')
    )

    User(message.chat.id)
    
    bot.send_message(message.chat.id, 
    DESCRIPTION.format(message.from_user.first_name), reply_markup=markup)


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


@bot.message_handler(content_types=['text'])
def buttons_handler(message):
    if message.text == 'Проверить состав':
        mes = bot.send_message(message.chat.id, 
        'Пришлите фоторграфию или текст состава.')

        bot.register_next_step_handler(mes, structure_analyser)

    elif message.text == 'Чёрный список':
        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton('Получить список', 
            callback_data='get'),
            types.InlineKeyboardButton('Добавить элементы', 
            callback_data='add'),
            types.InlineKeyboardButton('Удалить элементы', 
            callback_data='del')
        )  # Maybe remove keyboard after pressing a button?

        bot.send_message(message.chat.id, 'Выберете действие:', reply_markup=markup)


def structure_analyser(message):
    if message.content_type == 'text':  # Call text analyser (with all user exceptions)
        bot.send_message(message.chat.id, 
        'It will be introduced some time later...')

    elif message.content_type == 'photo':  # AI
        bot.send_message(message.chat.id, 
        'This function will be avaliable if you buy the premium version.')


@bot.callback_query_handler(func=lambda c: True)
def inline_buttons_handler(call):
    if call.message:
        if call.data == 'get':  # Getting all exceptions
            user = User(call.message.chat.id)
            additives = user.get_additives()
            if additives:
                bot.send_message(call.message.chat.id, 
                'Ваш чёрный список:\n' + ', '.join(additives))
            else:
                bot.send_message(call.message.chat.id, 
                'У вас пока нет чёрного списка...')

        elif call.data == 'add':  # Adding a connection/excepiton
            mes = bot.send_message(call.message.chat.id,
            'Пришлите названия элементов.')
            bot.register_next_step_handler(mes, add_item)

        elif call.data == 'del':  # Deleting connection/exception
            mes = bot.send_message(call.message.chat.id,
            'Пришлите названия элементов.')
            bot.register_next_step_handler(mes, del_item)


def add_item(message):
    for additive_name in message.text.split(', '):  # Add filter later
        user = User(message.chat.id)

        if additive_name.lower() in user.get_additives():
            bot.send_message(message.chat.id, 
            f'Элемент "{additive_name}" уже есть в списке.')
        else:
            additive = Additive(additive_name.lower())
            user.add_additive(additive)

            bot.send_message(message.chat.id, 
            f'Элемент "{additive_name}" успешно добавлен.')


def del_item(message):
    for additive_name in message.text.split(', '):
        user = User(message.chat.id)
        if additive_name in user.get_additives():
            additive = Additive(additive_name)
            user.del_additive(additive)

            bot.send_message(message.chat.id,
            f'Элемент "{additive_name}" успешно удалён.')
        else:
            bot.send_message(message.chat.id, 
            f'Элемента "{additive_name}" не существует.')


bot.infinity_polling()  # Running
