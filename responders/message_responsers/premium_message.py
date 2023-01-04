from responders.responder import Responder
from data.config import PREMIUMTERMS, PREMIUM

from datetime import datetime
from telebot import TeleBot
from telebot import types


class PremiumMessage(Responder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)
    
    def handle(self, message: types.Message) -> bool:
        if message.text == PREMIUM:
            print(f'{datetime.now()} --- PREMIUM message from {message.chat.id}')
            markup = types.InlineKeyboardMarkup()

            markup.add(
                types.InlineKeyboardButton('Отправить заявку', 
                callback_data='premium')
                )

            self.bot.send_message(message.chat.id, PREMIUMTERMS, reply_markup=markup)
            return True
        return False
