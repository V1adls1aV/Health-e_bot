from objects.user import User
from objects.ecode import ECode
from data_structures.photo import Photo
from data_structures.composition import Composition
from responders.responder import Responder
from data.config import ECODEDEGREES

from datetime import datetime
from telebot import TeleBot
from telebot import types


class AnalyzingMessage(Responder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)

    def handle(self, message: types.Message) -> bool:
        if message.content_type == 'text':  # Getting evalution of text
            print(f'{datetime.now()} --- TEXT analyzer from {message.chat.id}')

            user = User.get_current_user(message.chat.id)
            self._composition_analyzer(message, message.text, user)
            return True

        elif message.content_type == 'photo':  # AI
            print(f'{datetime.now()} --- PHOTO analyzer from {message.chat.id}')
            user = User.get_current_user(message.chat.id)
            image = Photo(self.bot, message)

            if image.is_text():
                text = image.get_text()
                self._composition_analyzer(message, text, user)
            else:
                self.bot.send_message(message.chat.id,
                    'Не могу разглядеть состав('
                    )
            return True
        return False


    def _composition_analyzer(self, message: types.Message, text: str, user: User):
        comp = Composition(text)
        comp.set_user(user)
        markup = types.InlineKeyboardMarkup(row_width=1)

        ecode_list = [(el, ECode.get_harm_degree(el)) for el in comp.ecodes]
        ecode_list.sort(key=lambda x: x[1], reverse=True)
        for el, _ in ecode_list:
            markup.add(types.InlineKeyboardButton(
                el + f' ({ECODEDEGREES[ECode.get_harm_degree(el)]})', 
                callback_data=el))  # Creating buttons with short description of ecodes
        
        self.bot.send_message(message.chat.id, 
            comp.get_evaluation(), reply_markup=markup)
