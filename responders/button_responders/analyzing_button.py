from telebot import TeleBot
from telebot import types
from datetime import datetime
import json

from data_structures.composition import Composition
from data_structures.product import Product
from responders.responder import Responder
from objects.ecode import ECode
from objects.user import User
from data.config import ECODEDEGREES


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
            self.bot.clear_step_handler(call.message)
            return True

        try:
            req = json.loads(call.data)
            if req['type'] == 'barcode':
                message = self.bot.send_message(
                    call.message.chat.id,
                    'Жду фото состава продукта...'
                )
                self.barcode = req['barcode']
                self.bot.register_next_step_handler(
                    message, self._send_product
                )
                return True
            return False
        except:
            return False


    def _send_product(self, message: types.Message):
        print(f'{datetime.now()} --- Sending product handler for {message.chat.id}')
        product = Product(self.bot, message)

        if product.is_text and (not product.barcode or \
                product.barcode == self.barcode):
            self.bot.send_message(
                message.chat.id,
                'Спасибо за вклад в общее дело ❤️'
            )
            product.barcode = self.barcode
            self._composition_analyzer(
                product.extract_text(),
                User.get_current_user(message.chat.id)
            )
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


    # There is problem with same function in two classes...
    # They should be the same class maybe, but how?
    # Or I have to create a new class...
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
