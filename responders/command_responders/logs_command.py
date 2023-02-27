from responders.responder import Responder

from telebot import TeleBot
from telebot.types import Message
from datetime import datetime


class LogsCommand(Responder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)

    def handle(self, message: Message) -> bool:
        if message.text.startswith('/logs'):
            print(f'{datetime.now()} --- LOGS command from {message.chat.id}')
            with open('hello.log', encoding='utf-8') as file:
                if len(message.text.split()) == 1:
                    self.bot.send_document(message.chat.id, file)
                else:
                    lines = int(message.text.split()[1])
                    last_logs = file.readlines()[-lines:]
                    self.bot.send_message(message.chat.id, ''.join(last_logs))
            return True
        return False
