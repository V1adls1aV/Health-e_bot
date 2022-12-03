from telebot import TeleBot
from telebot import types
from random import choice
import json

from objects.user import User
from objects.ecode import ECode
from objects.additive import Additive
from data_structures import AdditiveList
from data.config import BLACKLIST, CHECKCOMP, PREMIUM, \
    ADMINS, BLACKLISTOVERFLOW, FEEDBACK


class InlineResponder:
    def __init__(self, bot: TeleBot) -> None:
        self.bot = bot
    
    def handle(self, call) -> bool:
        return False


class AdditivesResponder(InlineResponder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)

    def handle(self, call) -> bool:
        if call.data == 'get':  # Getting all additives
            user = User.get_current_user(call.message.chat.id)
            additives = user.get_additives_names()

            if additives:
                self.bot.edit_message_text(
                    'Ваш чёрный список:\n' + ', '.join(additives) + '.',
                    call.message.chat.id, call.message.id)
            else:
                self.bot.edit_message_text(
                    'У вас пока нет чёрного списка.', 
                    call.message.chat.id, call.message.id)
            return True

        elif call.data == 'add':  # Adding a connection/additive
            user = User.get_current_user(call.message.chat.id)
            if user.is_adding_avaliable():
                mes = self.bot.edit_message_text(
                    'Пришлите названия элементов через запятую.', 
                    call.message.chat.id, call.message.id
                    )
                self.bot.register_next_step_handler(mes, self.add_item)
            else:
                self.bot.edit_message_text(
                    BLACKLISTOVERFLOW, 
                    call.message.chat.id, call.message.id
                    )
            return True
        
        elif call.data == 'del':  # Deleting connection/addititve
            mes = self.bot.edit_message_text(
                'Пришлите названия элементов через запятую.', 
                call.message.chat.id, call.message.id
                )
            self.bot.register_next_step_handler(mes, self.del_item)
            return True
        return False

    def add_item(self, message):
        user = User.get_current_user(message.chat.id)
        names = user.get_additives_names()
        for additive_name in AdditiveList(message.text):
            if additive_name in names:
                self.bot.send_message(message.chat.id, 
                f'Элемент "{additive_name}" уже есть в списке.')
            elif additive_name.capitalize() not in (BLACKLIST, CHECKCOMP, PREMIUM):
                if user.is_adding_avaliable():
                    additive = Additive(additive_name)
                    user.add_additive(additive)

                    self.bot.send_message(message.chat.id, 
                    f'Элемент "{additive_name}" успешно добавлен.')
                else:
                    self.bot.send_message(message.chat.id, BLACKLISTOVERFLOW)
                    break


    def del_item(self, message):
        user = User.get_current_user(message.chat.id)
        names = user.get_additives_names()
        for additive_name in AdditiveList(message.text):
            if additive_name in names:
                additive = Additive(additive_name)
                user.del_additive(additive)
                
                self.bot.send_message(message.chat.id,
                f'Элемент "{additive_name}" успешно удалён.')
            elif additive_name.capitalize() not in (BLACKLIST, CHECKCOMP, PREMIUM):
                self.bot.send_message(message.chat.id, 
                f'Элемента "{additive_name}" не существует.')


class ECodeResponder(InlineResponder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)

    def handle(self, call) -> bool:
        if call.data[0] == 'е':
            self.bot.send_message(
                call.message.chat.id,
                ECode(call.data).get_description()
                )
            return True
        return False


class PremiumResponder(InlineResponder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)
    
    def handle(self, call) -> bool:
        if call.data == 'premium':
            admin_chat_id = choice(ADMINS)  # Getting random admin
            user = User.get_current_user(call.message.chat.id)

            set_p = json.dumps({'type': 'set', 'chat_id': str(call.message.chat.id)})
            del_p = json.dumps({'type': 'del', 'chat_id': str(call.message.chat.id)})
            
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton('✅', 
                callback_data=set_p),
                types.InlineKeyboardButton('❌', 
                callback_data=del_p)
                )
            
            self.bot.send_message(admin_chat_id, f'''
                Пользователь @{call.message.chat.username} запрашивает premuim.\nPremium status: {user.premium}''',
                reply_markup=markup)  # Sending message to admin

            self.bot.send_message(call.message.chat.id, 
                'Заявка отправлена, спасибо!')  # Message to user
            return True
        
        elif call.data == 'feedback':
            mes = self.bot.send_message(call.message.chat.id, FEEDBACK)
            self.bot.register_next_step_handler(mes, self.send_feedback)
            return True

        elif json.loads(call.data)['type'] == 'set':
            user = User.get_current_user(json.loads(call.data)['chat_id'])
            if not user.premium:
                user.premium = True
                self.bot.edit_message_text(
                    call.message.text.replace('False', 'True'),
                    call.message.chat.id, call.message.id, 
                    reply_markup=call.message.reply_markup)
            return True

        elif json.loads(call.data)['type'] == 'del':
            user = User.get_current_user(json.loads(call.data)['chat_id'])
            if user.premium:
                user.premium = False
                self.bot.edit_message_text(
                    call.message.text.replace('True', 'False'),
                    call.message.chat.id, call.message.id, 
                    reply_markup=call.message.reply_markup)
            return True
        return False


    def send_feedback(self, message):
        if message.text not in (BLACKLIST, CHECKCOMP, PREMIUM):       
            chat_id = choice(ADMINS)  # Getting random admin
            self.bot.send_message(chat_id, f'''
                Пользователь @{message.from_user.username} оставил отзыв:\n{message.text}'''
                )  # Maybe add reply for admin in the future
