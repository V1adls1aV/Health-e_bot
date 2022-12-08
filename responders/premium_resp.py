from telebot import TeleBot
from telebot import types
from random import choice
from datetime import datetime
import json

from objects.user import User
from responders.inline_resp import InlineResponder
from data.config import ADMINS, QUEST1, QUEST2, QUEST3


class PremiumResponder(InlineResponder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)
    
    def handle(self, call) -> bool:
        if call.data == 'premium':
            print(f'{datetime.now()} --- PREMIUM handler for {call.message.chat.id}')
            self._premium_call(call.message)
            return True

        elif json.loads(call.data)['type'] == 'set':
            chat_id = json.loads(call.data)['chat_id']
            print(f'{datetime.now()} --- SET PREMIUM handler for {chat_id}')

            self._set_premium(call.message, chat_id)
            return True

        elif json.loads(call.data)['type'] == 'del':
            chat_id = json.loads(call.data)['chat_id']
            print(f'{datetime.now()} --- DEL PREMIUM handler for {chat_id}')

            self._del_premium(call.message, chat_id)
            return True
        return False


    def _premium_call(self, message):
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
            self.bot.send_message(message.chat.id, QUEST1)
            self.bot.send_message(message.chat.id, QUEST2)
            self.bot.send_message(message.chat.id, QUEST3)


    def _set_premium(self, message, chat_id):
        user = User.get_current_user(chat_id)
        if not user.premium:
            user.premium = True
            self.bot.edit_message_text(
                message.text.replace('False', 'True'),
                message.chat.id, message.id, 
                reply_markup=message.reply_markup)
            self.bot.send_message(chat_id, 'Теперь у тебя есть premium!')
            

    def _del_premium(self, message, chat_id):
        user = User.get_current_user(chat_id)
        if user.premium:
            user.premium = False
            self.bot.edit_message_text(
                message.text.replace('True', 'False'),
                message.chat.id, message.id, 
                reply_markup=message.reply_markup)
            self.bot.send_message(chat_id, 'Теперь у тебя нет premium(')
