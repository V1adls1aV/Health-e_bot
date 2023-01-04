from telebot import TeleBot
from telebot import types
from random import choice
from datetime import datetime
import json

from objects.user import User
from responders.responder import Responder
from data.config import ADMINS


class PremiumButton(Responder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)
    
    def handle(self, call: types.CallbackQuery) -> bool:
        if call.data == 'premium':
            print(f'{datetime.now()} --- PREMIUM button from {call.message.chat.id}')
            self._premium_call(call.message)
            return True

        elif json.loads(call.data)['type'] == 'set':
            chat_id = json.loads(call.data)['chat_id']
            print(f'{datetime.now()} --- SET PREMIUM button from {chat_id}')

            self._set_premium(call.message, chat_id)
            return True

        elif json.loads(call.data)['type'] == 'del':
            chat_id = json.loads(call.data)['chat_id']
            print(f'{datetime.now()} --- DEL PREMIUM button from {chat_id}')

            self._del_premium(call.message, chat_id)
            return True
        return False


    def _premium_call(self, message: types.Message):
            admin_chat_id = choice(ADMINS)  # Getting random admin
            user = User.get_current_user(message.chat.id)

            set_p = json.dumps({'type': 'set', 'chat_id': str(message.chat.id)})
            del_p = json.dumps({'type': 'del', 'chat_id': str(message.chat.id)})
            
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton('✅', 
                callback_data=set_p),
                types.InlineKeyboardButton('❌', 
                callback_data=del_p)
                )
            
            self.bot.send_message(admin_chat_id, f'''
                Пользователь @{message.chat.username} запрашивает premuim.\nPremium status: {user.premium}''',
                reply_markup=markup)  # Sending message to admin

            # Message to user
            self.bot.send_message(message.chat.id, 'Заявка отправлена, скоро ответим!')


    def _set_premium(self, message: types.Message, chat_id: int):
        user = User.get_current_user(chat_id)
        if not user.premium:
            user.premium = True
            self.bot.edit_message_text(
                message.text.replace('False', 'True'),
                message.chat.id, message.id, 
                reply_markup=message.reply_markup)
            self.bot.send_message(chat_id, 'Теперь у тебя есть premium!')
            

    def _del_premium(self, message: types.Message, chat_id: int):
        user = User.get_current_user(chat_id)
        if user.premium:
            user.premium = False
            self.bot.edit_message_text(
                message.text.replace('True', 'False'),
                message.chat.id, message.id, 
                reply_markup=message.reply_markup)
            self.bot.send_message(chat_id, 'Теперь у тебя нет premium(')
