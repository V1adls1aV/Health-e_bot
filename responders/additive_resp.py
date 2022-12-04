from telebot import TeleBot

from objects.user import User
from objects.additive import Additive
from data_structures import AdditiveList
from responders.inline_resp import InlineResponder
from data.config import BLACKLIST, CHECKCOMP, PREMIUM, BLACKLISTOVERFLOW


class AdditivesResponder(InlineResponder):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)

    def handle(self, call) -> bool:
        if call.data == 'get':
            self._get_call(call.message)
            return True

        elif call.data == 'add':
            self._add_call(call.message)
            return True
        
        elif call.data == 'del':
            self._del_call(call.message)
            return True
        return False


    def _get_call(self, message):  # Getting all additives
        user = User.get_current_user(message.chat.id)
        additives = user.get_additives_names()

        if additives:
            self.bot.edit_message_text(
                'Ваш чёрный список:\n' + ', '.join(additives) + '.',
                message.chat.id, message.id)
        else:
            self.bot.edit_message_text(
                'У вас пока нет чёрного списка.', 
                message.chat.id, message.id)
    
    def _add_call(self, message):  # Adding a connection/additive
        user = User.get_current_user(message.chat.id)
        if user.is_adding_avaliable():
            mes = self.bot.edit_message_text(
                'Пришлите названия элементов через запятую.', 
                message.chat.id, message.id
                )
            self.bot.register_next_step_handler(mes, self._add_item)
        else:
            self.bot.edit_message_text(
                BLACKLISTOVERFLOW, 
                message.chat.id, message.id
                )

    def _add_item(self, message):
        user = User.get_current_user(message.chat.id)
        names = user.get_additives_names()
        for additive_name in AdditiveList(message.text):
            if additive_name in names:
                self.bot.send_message(message.chat.id, 
                f'Элемент "{additive_name}" уже есть в списке.')
            elif additive_name.capitalize() not in (BLACKLIST, CHECKCOMP, PREMIUM):
                if user.is_adding_avaliable():
                    additive = Additive(additive_name)
                    user.add_additive(additive)

                    self.bot.send_message(message.chat.id, 
                    f'Элемент "{additive_name}" успешно добавлен.')
                else:
                    self.bot.send_message(message.chat.id, BLACKLISTOVERFLOW)
                    break


    def _del_call(self, message):  # Deleting connection/addititve
        mes = self.bot.edit_message_text(
            'Пришлите названия элементов через запятую.', 
            message.chat.id, message.id
            )
        self.bot.register_next_step_handler(mes, self._del_item)


    def _del_item(self, message):
        user = User.get_current_user(message.chat.id)
        names = user.get_additives_names()
        for additive_name in AdditiveList(message.text):
            if additive_name in names:
                additive = Additive(additive_name)
                user.del_additive(additive)
                
                self.bot.send_message(message.chat.id,
                f'Элемент "{additive_name}" успешно удалён.')
            elif additive_name.capitalize() not in (BLACKLIST, CHECKCOMP, PREMIUM):
                self.bot.send_message(message.chat.id, 
                f'Элемента "{additive_name}" не существует.')
