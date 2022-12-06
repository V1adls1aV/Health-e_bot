from telebot import TeleBot

from objects.ecode import ECode
from responders.inline_resp import InlineResponder


class ECodeResponder(InlineResponder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)

    def handle(self, call) -> bool:
        if call.data[0] == 'е':
            print(f'ECODE handler for {call.data}')
            self.bot.send_message(
                call.message.chat.id,
                ECode(call.data).get_description()
                )
            return True
        return False
