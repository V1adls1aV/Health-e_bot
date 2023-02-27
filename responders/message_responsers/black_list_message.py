from responders.responder import Responder
from data.config import BLACKLIST

from datetime import datetime
from telebot import TeleBot
from telebot import types


class BlackListMessage(Responder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)
    
    def handle(self, message: types.Message) -> bool:
        if message.text == BLACKLIST:
            print(f'{datetime.now()} --- BLACKLIST message from {message.chat.id}')
            markup = types.InlineKeyboardMarkup(row_width=1)

            markup.add(
                types.InlineKeyboardButton('Получить список', 
                callback_data='get'),
                types.InlineKeyboardButton('Добавить элементы', 
                callback_data='add'),
                types.InlineKeyboardButton('Удалить элементы', 
                callback_data='del')
                )

            self.bot.send_message(message.chat.id, 'Выбери действие:', 
                reply_markup=markup)
            return True
        return False
