from responders.responder import Responder
from data.config import BLACKLIST, PREMIUM, FEEDBACK, \
    FEEDBACKTEXT, QUEST1, QUEST2, ADMINS

from datetime import datetime
from telebot import TeleBot
from telebot.types import Message


class FeedbackMessage(Responder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)
    
    def handle(self, message: Message) -> bool:
        if message.text == FEEDBACK:
            print(f'{datetime.now()} --- FEEDBACK message from {message.chat.id}')
            self.bot.send_message(message.chat.id, FEEDBACKTEXT)
            self.bot.send_message(message.chat.id, QUEST1)
            mes = self.bot.send_message(message.chat.id, QUEST2)
            self.bot.register_next_step_handler(mes, self._send_feedback)
            return True
        return False

    def _send_feedback(self, message: Message):
        if message.text in (FEEDBACK, BLACKLIST, PREMIUM):
            return

        self.bot.send_message(ADMINS, f'Пользователь @{message.from_user.username} оставил отзыв:')
        self.bot.forward_message(ADMINS, message.chat.id, message.id)
        # Maybe add reply from admin in the future

        self.bot.send_message(message.chat.id, 'Спасибо за отзыв❤️')
        # To user
