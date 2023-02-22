from objects.user import User
from objects.ecode import ECode
from data_structures.product import Product
from data_structures.composition import Composition
from responders.responder import Responder
from data.config import ECODEDEGREES, OOPSMESSAGE

from random import choice
from datetime import datetime
from telebot import TeleBot
from telebot import types
import json


class AnalyzingMessage(Responder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)

    def handle(self, message: types.Message) -> bool:
        if message.content_type == 'text':  # Getting evalution of text
            print(f'{datetime.now()} --- TEXT analyzer from {message.chat.id}')

            user = User.get_current_user(message.chat.id)
            self._composition_analyzer(message.text, user)
            return True

        elif message.content_type == 'photo':  # AI
            print(f'{datetime.now()} --- PHOTO analyzer from {message.chat.id}')
            self._handle_photo(message)
            return True
        
        return False


    def _handle_photo(self, message: types.Message):
        user = User.get_current_user(message.chat.id)
        product = Product(self.bot, message)

        # Text from image and OFF
        if product.is_text and product.received_text:
            self.bot.send_message(
                message.chat.id,
                'Анализирую текст с фото и из базы данных...'
            )
            self._composition_analyzer(
                product.extract_text() + ', ' + product.received_text,
                user
            )

        # Auto suggesting for OFF
        elif product.is_text and product.barcode:
            self.bot.send_message(
                message.chat.id,
                'Такого продукта нет в Open Food Facts, я добавлю!'
            )
            self._composition_analyzer(product.extract_text(), user)
            product.send_to_OFF()

        # Text from image
        elif product.is_text:
            self.bot.send_message(
                message.chat.id,
                'Проверяю состав на фото...'
            )
            self._composition_analyzer(product.extract_text(), user)
        
        # Text from OFF
        elif product.received_text:
            self.bot.send_message(
                message.chat.id,
                'Нашел продукт в Open Food Facts, проверяю!'
            )
            self._composition_analyzer(product.received_text, user)

        # Proposal of OFF suggesting
        elif product.barcode:
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton(
                    'Сделать фото',
                    callback_data=json.dumps({
                        'type': 'barcode',
                        'barcode': product.barcode})
            ))

            self.bot.send_message(
                message.chat.id,
                'Продукта нет в базе данных, хочешь добавить?',
                reply_markup=markup)

        else:
            self.bot.send_message(message.chat.id,
                choice(OOPSMESSAGE)
            )


    def _composition_analyzer(self, text: str, user: User):
        comp = Composition(text)
        comp.set_user(user)
        markup = types.InlineKeyboardMarkup(row_width=1)

        ecode_list = [(el, ECode.get_harm_degree(el)) for el in comp.ecodes]
        ecode_list.sort(key=lambda x: x[1], reverse=True)
        for el, _ in ecode_list:
            markup.add(types.InlineKeyboardButton(
                el + f' ({ECODEDEGREES[ECode.get_harm_degree(el)]})', 
                callback_data=el))  # Creating buttons with short description of ecodes
        
        self.bot.send_message(user.chat_id, 
            comp.get_evaluation(), reply_markup=markup)
