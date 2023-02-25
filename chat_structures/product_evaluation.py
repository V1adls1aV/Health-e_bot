from telebot import types, TeleBot

from data_structures.composition import Composition
from objects.ecode import ECode
from objects.user import User
from data.config import ECODEDEGREES


class ProductEvaluation:
    def __init__(self, bot: TeleBot, text: str):
        self.text = text
        self.bot = bot

    def send_to_user(self, user: User):
            comp = Composition(self.text)
            comp.set_user(user)
            markup = types.InlineKeyboardMarkup(row_width=1)

            ecode_list = [(el, ECode.get_harm_degree(el)) for el in comp.ecodes]
            ecode_list.sort(key=lambda x: x[1], reverse=True)
            for el, degree in ecode_list:
                markup.add(types.InlineKeyboardButton(
                    f'{el} ({ECODEDEGREES[degree]})', 
                    callback_data=el))  # Creating buttons with short description of ecodes

            self.bot.send_message(user.chat_id, 
                comp.get_evaluation(), reply_markup=markup)
