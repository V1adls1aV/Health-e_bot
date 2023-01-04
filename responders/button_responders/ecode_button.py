from telebot.types import CallbackQuery
from telebot import TeleBot
from datetime import datetime

from objects.ecode import ECode
from responders.responder import Responder


class ECodeButton(Responder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)

    def handle(self, call: CallbackQuery) -> bool:
        if call.data[0] == 'е':
            print(f'{datetime.now()} --- ECODE button for {call.data}')
            self.bot.send_message(
                call.message.chat.id,
                ECode(call.data).get_description()
                )
            return True
        return False
