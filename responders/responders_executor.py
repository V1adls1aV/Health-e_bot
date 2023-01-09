from telebot.types import Message, CallbackQuery
from responders.responder import Responder


class RespondersExecutor:
    def __init__(self, responsers: list[Responder]) -> None:
        self.responders = responsers

    def execute(self, request: Message or CallbackQuery):
        for responder in self.responders:
            if responder.handle(request):
                break
