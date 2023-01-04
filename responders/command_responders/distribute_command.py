from responders.responder import Responder
from objects.user import User

from telebot import TeleBot
from telebot.types import Message
from datetime import datetime


class DistributeCommand(Responder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)
        
    def handle(self, message: Message):
        if message.text.startswith('/distribute'):
            print(f'{datetime.now()} --- DISTRIBUTE command from {message.chat.id}')
            mes = self.bot.send_message(message.chat.id, 'Пришли текст рассылки')
            self.bot.register_next_step_handler(mes, self._distribute_message)
            return True
        return False

    def _distribute_message(self, message: Message):
        if message.text == 'cancel':
            self.bot.send_message(message.chat.id, 'Рассылка отменена')
            return

        for chat_id in User.get_chats_ids():
            amount = 0
            try:
                self.bot.forward_message(chat_id, message.chat.id, message.id)
                amount += 1
            except:  # User has banned the bot
                pass
        
        self.bot.send_message(f'Всего рассылок: {amount}')
