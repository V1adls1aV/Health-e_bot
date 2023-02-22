from telebot.types import CallbackQuery, Message
from telebot import TeleBot
from datetime import datetime

from objects.user import User
from objects.additive import Additive
from data_structures.additive_list import AdditiveList
from responders.responder import Responder
from data.config import BLACKLISTOVERFLOW1, BLACKLISTOVERFLOW2, \
    FEEDBACK, BLACKLIST, PREMIUM


class BlackListButton(Responder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)

    def handle(self, call: CallbackQuery) -> bool:
        if call.data == 'get':
            print(f'{datetime.now()} --- GET button from {call.message.chat.id}')
            self._get_call(call.message)
            return True

        elif call.data == 'add':
            print(f'{datetime.now()} --- ADD button from {call.message.chat.id}')
            self._add_call(call.message)
            return True
        
        elif call.data == 'del':
            print(f'{datetime.now()} --- DEL button from {call.message.chat.id}')
            self._del_call(call.message)
            return True
        return False


    def _get_call(self, message: Message):  # Getting all additives
        user = User.get_current_user(message.chat.id)
        additives = user.get_additives_names()

        if additives:
            response = 'Твой чёрный список:\n' + ', '.join(additives) + '.'
        else:
            response = 'У тебя нет чёрного списка...'

        self.bot.edit_message_text(
            response, 
            message.chat.id, message.id)

    def _current_additive_list(self, message: Message):
        user = User.get_current_user(message.chat.id)
        additives = user.get_additives_names()

        if additives:
            response = 'Твой чёрный список:\n' + ', '.join(additives) + '.'
        else:
            response = 'У тебя нет чёрного списка('
        
        self.bot.send_message(message.chat.id, response)
    

    def _add_call(self, message: Message):  # Adding a connection/additive
        user = User.get_current_user(message.chat.id)
        if user.is_adding_avaliable():
            mes = self.bot.edit_message_text(
                'Пришли названия элементов через запятую', 
                message.chat.id, message.id
                )
            self.bot.register_next_step_handler(mes, self._add_item)

        else:
            self.bot.edit_message_text(
                BLACKLISTOVERFLOW1, 
                message.chat.id, message.id
                )
            self.bot.send_message(message.chat.id, 
            BLACKLISTOVERFLOW2)

    def _add_item(self, message: Message):
        if message.text in (FEEDBACK, BLACKLIST, PREMIUM):
            return
        user = User.get_current_user(message.chat.id)
        names = user.get_additives_names()

        for additive_name in AdditiveList(message.text):
            if additive_name in names:
                self.bot.send_message(message.chat.id, 
                f'Элемент "{additive_name}" уже есть в списке')
            
            else:
                if user.is_adding_avaliable():
                    additive = Additive(additive_name)
                    user.add_additive(additive)

                    self.bot.send_message(message.chat.id, 
                    f'Элемент "{additive_name}" успешно добавлен')
                
                else:
                    self.bot.send_message(message.chat.id, 
                    BLACKLISTOVERFLOW1)
                    self.bot.send_message(message.chat.id, 
                    BLACKLISTOVERFLOW2)
                    break

        self._current_additive_list(message)
        # Info about current black list


    def _del_call(self, message: Message):  # Deleting connection/addititve
        mes = self.bot.edit_message_text(
            'Пришли названия элементов через запятую', 
            message.chat.id, message.id
            )
        self.bot.register_next_step_handler(mes, self._del_item)

    def _del_item(self, message: Message):
        if message.text in (FEEDBACK, BLACKLIST, PREMIUM):
            return
        user = User.get_current_user(message.chat.id)
        names = user.get_additives_names()

        for additive_name in AdditiveList(message.text):
            if additive_name in names:
                additive = Additive(additive_name)
                user.del_additive(additive)
                
                response = f'Элемент "{additive_name}" успешно удалён'
            else:
                response = f'Элемент "{additive_name}" был удалён ранее'

            self.bot.send_message(message.chat.id, response)

        self._current_additive_list(message)
        # Info about current black list
