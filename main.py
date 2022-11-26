import telebot as tb
from telebot import types
from pytesseract import image_to_string
from PIL.Image import open as open_image
from random import choice
from io import BytesIO

from objects.additive import Additive
from objects.eadditive import EAdditive
from objects.user import User, GetCurrentUser
from text_objects import AdditiveList, Composition
from data.config import TOKEN, DESCRIPTION, ADMINS, TESS_CONFIG, PREMIUMTERMS


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
        types.KeyboardButton('Проверить состав ✅'),
        types.KeyboardButton('Чёрный список ❌'),
        types.KeyboardButton('Премиум 👑')
        )

    GetCurrentUser(message)
    
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
    if message.text == 'Проверить состав ✅':
        mes = bot.send_message(message.chat.id, 
        'Пришлите фоторграфию или текст состава.')

        bot.register_next_step_handler(mes, get_composition)

    elif message.text == 'Чёрный список ❌':
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

    elif message.text == 'Премиум 👑':
        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton('Отправить заявку', 
            callback_data='premium'),
            types.InlineKeyboardButton('Задать вопрос', 
            callback_data='question'),
            )

        bot.send_message(message.chat.id, PREMIUMTERMS, reply_markup=markup)


##################### Composition analyzing #####################


def get_composition(message):
    if message.content_type == 'text':  # Getting evalution of text
        user = GetCurrentUser(message)
        composition_analyzer(message, message.text, user)

    elif message.content_type == 'photo':  # AI
        user = GetCurrentUser(message)

        if user.premium:
            image = get_image_from_message(message)
            text = image_to_string(image, lang='rus', config=TESS_CONFIG)
            print('_________________')
            print('Text recognition:')
            print(text)
            print('_________________')
            composition_analyzer(message, text, user)

        else:
            bot.send_message(message.chat.id, 
            'This function will be avaliable if you buy the premium version.')


def get_image_from_message(message):  # Get image from server
    image_id = message.photo[-1].file_id
    image_bytes = bot.download_file(
        bot.get_file(image_id).file_path
        )
    with BytesIO(image_bytes) as stream:
        return open_image(stream).convert('RGBA')


def composition_analyzer(message, text, user):
    comp = Composition(
        user,
        text)

    markup = types.InlineKeyboardMarkup()
    for el in comp.e_additives:
        markup.add(types.InlineKeyboardButton(el, callback_data=el))
    bot.send_message(message.chat.id, comp.get_evaluation(), reply_markup=markup)


########################### Callbacks ###########################


@bot.callback_query_handler(func=lambda c: True)
def inline_buttons_handler(call):
    if call.message:
        if call.data == 'get':  # Getting all exceptions
            user = GetCurrentUser(call.message)
            additives = user.get_additives_names()

            if additives:
                bot.edit_message_text(
                    'Ваш чёрный список:\n' + ', '.join(additives) + '.',
                    call.message.chat.id, call.message.id)
            else:
                bot.edit_message_text(
                    'У вас пока нет чёрного списка.', 
                    call.message.chat.id, call.message.id)

        elif call.data == 'add':  # Adding a connection/additive
            mes = bot.edit_message_text(
                'Пришлите названия элементов через запятую.', 
                call.message.chat.id, call.message.id
                )
            bot.register_next_step_handler(mes, add_item)

        elif call.data == 'del':  # Deleting connection/addititve
            mes = bot.edit_message_text(
                'Пришлите названия элементов через запятую.', 
                call.message.chat.id, call.message.id
                )
            bot.register_next_step_handler(mes, del_item)

        elif call.data[0] == 'е':
            bot.send_message(
                call.message.chat.id,
                EAdditive(call.data).get_description()
                )
        
        elif call.data == 'premium':
            admin_chat_id = choice(ADMINS)  # Getting random admin
            user = GetCurrentUser(call.message)
            
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton('✅', 
                callback_data=f'set_premium{call.message.chat.id}'),  # This is awful...
                types.InlineKeyboardButton('❌', 
                callback_data=f'del_premium{call.message.chat.id}')
                )  # How to put chat_id to Inline handler
            
            bot.send_message(admin_chat_id, f'''
                Пользователь @{call.message.chat.username} запрашивает premuim.
                Premium status: {user.premium}''',
                reply_markup=markup)  # Sending message to admin

            bot.send_message(call.message.chat.id, 
                'Заявка отправлена, спасибо!')  # Message to user

        elif call.data == 'question':
            mes = bot.send_message(call.message.chat.id, 'Задайте вопрос:')
            bot.register_next_step_handler(mes, send_question)

        elif call.data[:12] == 'set_premium':  # This is awful...
            user = GetCurrentUser(int(call.data[12:]))
            user.premium = True

        elif call.data[:12] == 'del_premium':  # This is awful...
            user = GetCurrentUser(int(call.data[12:]))
            user.premium = False


def add_item(message):
    user = GetCurrentUser(message)
    names = user.get_additives_names()
    for additive_name in AdditiveList(message.text):
        if additive_name in names:
            bot.send_message(message.chat.id, 
            f'Элемент "{additive_name}" уже есть в списке.')
        elif additive_name == 'чёрный список ✅' or additive_name == 'проверить состав ❌':
            buttons_handler(message)
        else:
            additive = Additive(additive_name)
            user.add_additive(additive)

            bot.send_message(message.chat.id, 
            f'Элемент "{additive_name}" успешно добавлен.')


def del_item(message):
    user = GetCurrentUser(message)
    names = user.get_additives_names()
    for additive_name in AdditiveList(message.text):
        if additive_name in names:
            additive = Additive(additive_name)
            user.del_additive(additive)
            
            bot.send_message(message.chat.id,
            f'Элемент "{additive_name}" успешно удалён.')
        elif additive_name == 'чёрный список ✅' or additive_name == 'проверить состав ❌':
            buttons_handler(message)
        else:
            bot.send_message(message.chat.id, 
            f'Элемента "{additive_name}" не существует.')


def send_question(message):
    chat_id = choice(ADMINS)  # Getting random admin
    bot.send_message(chat_id, f'''
        Пользователь @{message.from_user.username} задал вопрос:
        {message.text}'''
        )  # Maybe add reply for admin in the future


bot.infinity_polling()  # Running
