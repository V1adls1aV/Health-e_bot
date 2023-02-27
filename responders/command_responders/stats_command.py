from responders.responder import Responder
from data_structures.graph import Graph
from objects.user import User

from telebot import TeleBot
from telebot.types import Message
from datetime import datetime


class StatsCommand(Responder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)

    def handle(self, message: Message) -> bool:
        if message.text.startswith('/stats'):
            print(f'{datetime.now()} --- STATS command from {message.chat.id}')
            graph = Graph(
                User.get_creating_dates()
            )
            self.bot.send_photo(message.chat.id, graph.get_image(), 
                f'Всего пользователей: {graph.res}')
            return True
        return False