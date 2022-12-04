from telebot import TeleBot
from telebot import types
from random import choice
import json

from objects.user import User
from responders.inline_resp import InlineResponder
from data.config import BLACKLIST, CHECKCOMP, PREMIUM, ADMINS, FEEDBACK


class PremiumResponder(InlineResponder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)
    
    def handle(self, call) -> bool:
        if call.data == 'premium':
            self._premium_call(call.message)
            return True
        
        elif call.data == 'feedback':
            mes = self.bot.send_message(call.message.chat.id, FEEDBACK)
            self.bot.register_next_step_handler(mes, self._send_feedback)
            return True

        elif json.loads(call.data)['type'] == 'set':
            self._set_premium(call.message, 
                json.loads(call.data)['chat_id']
                )
            return True

        elif json.loads(call.data)['type'] == 'del':
            self._del_premium(call.message,
                json.loads(call.data)['chat_id']
                )
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

            self.bot.send_message(message.chat.id, 
                'Заявка отправлена, спасибо!')  # Message to user


    def _set_premium(self, message, chat_id):
        user = User.get_current_user(chat_id)
        if not user.premium:
            user.premium = True
            self.bot.edit_message_text(
                message.text.replace('False', 'True'),
                message.chat.id, message.id, 
                reply_markup=message.reply_markup)

    def _del_premium(self, message, chat_id):
        user = User.get_current_user(chat_id)
        if user.premium:
            user.premium = False
            self.bot.edit_message_text(
                message.text.replace('True', 'False'),
                message.chat.id, message.id, 
                reply_markup=message.reply_markup)


    def _send_feedback(self, message):
        if message.text not in (BLACKLIST, CHECKCOMP, PREMIUM):       
            chat_id = choice(ADMINS)  # Getting random admin
            self.bot.send_message(chat_id, f'''
                Пользователь @{message.from_user.username} оставил отзыв:\n{message.text}'''
                )  # Maybe add reply for admin in the future
