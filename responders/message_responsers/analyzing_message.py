from chat_structures.product_evaluation import ProductEvaluation
from data_structures.product import Product
from responders.responder import Responder
from objects.user import User
from data.config import OOPSMESSAGE

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

            degree = ProductEvaluation(self.bot, message.text)    
            degree.send_to_user(
                User.get_current_user(message.chat.id))
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

            degree = ProductEvaluation(self.bot, 
                product.extract_text() + ', ' + product.received_text)    
            degree.send_to_user(user)

            product.send_to_OFF()
            self.bot.send_message(
                message.chat.id,
                'Обновил запись в базе данных, спасибо!'
            )

        # Auto suggesting for OFF
        elif product.is_text and product.barcode:
            self.bot.send_message(
                message.chat.id,
                'Такого продукта нет в Open Food Facts, я добавлю!'
            )
            degree = ProductEvaluation(self.bot, product.extract_text())    
            degree.send_to_user(user)
            product.send_to_OFF()

        # Text from image
        elif product.is_text:
            self.bot.send_message(
                message.chat.id,
                'Проверяю состав на фото...'
            )
            degree = ProductEvaluation(self.bot, product.extract_text())    
            degree.send_to_user(user)
        
        # Text from OFF
        elif product.received_text:
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton(
                    'Хочу сделать фото!',
                    callback_data=json.dumps({
                        'type': 'barcode',
                        'barcode': product.barcode})
            ))

            self.bot.send_message(
                message.chat.id,
                'Нашел продукт в Open Food Facts, проверяю!'
            )
            degree = ProductEvaluation(self.bot, product.received_text)    
            degree.send_to_user(user)

            self.bot.send_message(
                message.chat.id,
                'Хочешь обновить данные об этом продукте?',
                reply_markup=markup
            )

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
