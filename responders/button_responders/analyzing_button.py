from telebot import TeleBot
from telebot import types
from datetime import datetime
from random import choice
import json

from chat_structures.product_evaluation import ProductEvaluation
from data_structures.product import Product
from responders.responder import Responder
from objects.user import User
from data.config import THANKSMESSAGE


class AnalyzingButton(Responder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)
        self.barcode = None

    def handle(self, call: types.CallbackQuery) -> bool:
        if call.data == 'pass':
            self.bot.send_message(
                call.message.chat.id,
                'Эх...\nЯ в печали 😢'
            )
            self.bot.edit_message_reply_markup(
                call.message.chat.id,
                call.message.id,
                reply_markup=None)
            self.bot.clear_step_handler(call.message)
            return True

        try:
            req = json.loads(call.data)
            if req['type'] == 'barcode':
                message = self.bot.send_message(
                    call.message.chat.id,
                    'Жду фото состава продукта...'
                )
                self.bot.edit_message_reply_markup(
                    call.message.chat.id,
                    call.message.id,
                    reply_markup=None)
                
                self.barcode = req['barcode']
                self.bot.register_next_step_handler(
                    message, self._send_product
                )
                return True
            return False
        except:
            print(f'{datetime.now()} --- Exception: request is not JSON')
            return False


    def _send_product(self, message: types.Message):
        print(f'{datetime.now()} --- Sending product handler for {message.chat.id}')
        product = Product(self.bot, message)

        if product.is_text and (not product.barcode or \
                product.barcode == self.barcode):
            self.bot.send_message(
                message.chat.id,
                choice(THANKSMESSAGE)
            )
            
            degree = ProductEvaluation(self.bot, product.extract_text())    
            degree.send_to_user(User.get_current_user(message.chat.id))
            
            product.barcode = self.barcode
            product.send_to_OFF()

        # Someone is cheating...
        elif product.barcode != self.barcode and \
                product.barcode is not None:
            self.bot.send_message(
                message.chat.id,
                'Фу себя так вести!\nПочему штрих коды разные!?'
            )

        else:  # There is no text on image
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton(
                    'Не хочу, не буду(',
                    callback_data='pass')
            )

            message = self.bot.send_message(
                message.chat.id,
                'Не вижу состава...\nCделай другое фото, ну пожалуйста)',
                reply_markup=markup
            )

            self.bot.register_next_step_handler(
                message, self._send_product)
