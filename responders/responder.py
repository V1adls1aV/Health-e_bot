from telebot import TeleBot
from telebot.types import Message, CallbackQuery


class Responder:
    def __init__(self, bot: TeleBot) -> None:
        self.bot = bot
    
    def handle(self, request: Message or CallbackQuery) -> bool:
        return False
