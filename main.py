import telebot as tb
from telebot import types
from db_editors import UserEditor, ExceptionEditor
from data.config import TOKEN, DESCRIPTION, ADMINS


class Admin(tb.SimpleCustomFilter):
    key = 'is_admin'
    @staticmethod
    def check(message: tb.types.Message):
        return message.chat.id in ADMINS


bot = tb.TeleBot(TOKEN, parse_mode='HTML')  # initializing bot
bot.add_custom_filter(Admin())
user_ed = UserEditor()
exception_ed = ExceptionEditor()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton('Проверить состав'),
        types.KeyboardButton('Чёрный список')
    )

    if not user_ed.get_user_id(message.chat.id):
        user_ed.create_user(message.chat.id)  # Adding user
    
    bot.send_message(message.chat.id, 
    DESCRIPTION.format(message.from_user.first_name), reply_markup=markup)


@bot.message_handler(commands=['distribute'], is_admin=True)
def distribute_news(message):
    mes = bot.send_message(message.chat.id, 'Пришлите текст рассылки.')
    bot.register_next_step_handler(mes, sending_news)


def sending_news(message):
    amount = 0
    removements = 0
    for chat_id in user_ed.get_chats_ids():
        try:
            bot.send_message(chat_id, message.text)
            amount += 1
        except:
            us_id = user_ed.get_user_id(chat_id)
            exs = user_ed.get_user_exceptions(us_id)  # It will be good to return ex ids
            user_ed.remove_user(us_id)
            removements += 1

            for ex in exs:
                ex_id = exception_ed.get_exception_id(ex)
                if not exception_ed.get_exception_users(ex_id):
                    exception_ed.remove_exception(ex_id)

    bot.send_message(message.chat.id, 
    f'''
    Успешно.
    Количество рассылок: {str(amount)}.
    Удалённых пользователей: {str(removements)}.
    ''')


@bot.message_handler(commands=['stop'])
def remove_chat(message):
    us_id = user_ed.get_user_id(message.chat.id)
    exs = user_ed.get_user_exceptions(us_id)  # It will be good to return ex ids
    user_ed.remove_user(us_id)

    for ex in exs:
        ex_id = exception_ed.get_exception_id(ex)
        if not exception_ed.get_exception_users(ex_id):
            exception_ed.remove_exception(ex_id)
    

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
        )

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
            exceptions = user_ed.get_user_exceptions(
                        user_ed.get_user_id(call.message.chat.id)
            )
            if exceptions:
                bot.send_message(call.message.chat.id, 
                'Ваш чёрный список:\n' + ', '.join(exceptions))
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
    for ex in message.text.split(', '):
        ex_id = exception_ed.get_exception_id(ex.lower())
        if not ex_id:
            ex_id = exception_ed.create_exception(ex.lower())

        if ex in user_ed.get_user_exceptions(
            user_ed.get_user_id(message.chat.id)):  # Return ex ids 3/4(5) usings
            bot.send_message(message.chat.id, 
            f'Элемент "{ex}" уже есть в списке.')
        else:
            user_ed.create_connection(
                user_ed.get_user_id(message.chat.id),
                ex_id
            )

            bot.send_message(message.chat.id, 
            f'Элемент "{ex}" успешно добавлен.')


def del_item(message):
    for ex in message.text.split(', '):
        ex_id = exception_ed.get_exception_id(ex.lower())
        if ex_id:
            user_ed.remove_connection(
                user_ed.get_user_id(message.chat.id), ex_id)
            
            if not exception_ed.get_exception_users(ex_id):
                exception_ed.remove_exception(ex_id)

            bot.send_message(message.chat.id,
            f'Элемент "{ex}" успешно удалён.')
        else:
            bot.send_message(message.chat.id, 
            f'Элемента "{ex}" не существует.')


bot.infinity_polling()  # Running
