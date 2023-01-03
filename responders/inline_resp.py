from telebot import TeleBot


class InlineResponder:
    def __init__(self, bot: TeleBot) -> None:
        self.bot = bot
    
    def handle(self, call) -> bool:
        return False
