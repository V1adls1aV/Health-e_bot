from tests.unit_tests.setup import UserMock
from objects.user import User
from objects.ecode import ECode
from data.config import TESS_CONFIG
from datetime import datetime

from matplotlib import pyplot as plt
from pytesseract import image_to_string
from PIL.Image import open as open_image
from io import BytesIO


class Photo:
    def __init__(self, bot, message) -> None:
        self.bot = bot
        self.message = message
        self.image = self._get_image()

    def _get_image(self):  # Get image from server
        print(f'{datetime.now()} --- Getting image from server')
        image_id = self.message.photo[-1].file_id
        image_bytes = self.bot.download_file(
            self.bot.get_file(image_id).file_path
            )
        with BytesIO(image_bytes) as stream:
            return open_image(stream).convert('RGBA')

    def get_text(self):
        print(f'{datetime.now()} --- Getting text from image')
        text = image_to_string(self.image, lang='rus', config=TESS_CONFIG)
        print('__________________________________')
        print('Recognized text:')
        print(text)
        print('__________________________________')
        return text


class Graph:
    def __init__(self, dates) -> None:
        self.x = dates
        self.res = len(dates)
        self.y = list(range(1, self.res + 1))
    
    def get_image(self) -> None:
        print(f'{datetime.now()} --- Getting image from graph')
        stream = BytesIO()
        
        plt.title('Количество пользователей')
        plt.xticks(rotation=20)
        plt.plot_date(self.x, self.y, ls='-', fmt='.', color='green')
        
        plt.savefig(stream, format='png')
        plt.clf()
        return open_image(stream)


class AdditiveList(list):
    def __init__(self, text: str) -> None:
        self.raw_text = text
        self.text = self._filter_text()
        super().__init__(self.text)

    def _filter_text(self) -> list[str]:  # Filter the text
        print(f'{datetime.now()} --- Filtering the text')
        res = []
        for word in self.raw_text.split(','):
            if word:
                name = ''
                for letter in word.strip().lower():
                    if letter.isalpha() or letter.isalnum() or letter in ' -':
                        name += letter
                if name:
                    res.append(name.strip())
        print(f'{datetime.now()} --- Filtered text: {res}')
        return res


class Composition(AdditiveList):
    def __init__(self, text: str) -> None:
        super().__init__(text)  # Getting self.text and self.raw_text
        self.user_ecodes = ECode.get_ecodes()
        self.user_additives = None
        self.additives = None
        self.ecodes = None
        self.user_id = None

    def _find_additives(self) -> list[str] or None:
        ad, eco = set(), set()
        for el in self.text:
            if el[0] == 'e' and len(el) > 1:
                el = 'е' + el[1:]  # Solving problem with russian and english E letter

            for a in self.user_additives:  # Black list
                if a in el:
                    ad.add(a)
            for e in self.user_ecodes.values():  # E-codes
                if e in el:
                    eco.add(e)
            for n in self.user_ecodes.keys():  # E-names
                if n in el:
                    eco.add(self.user_ecodes[n])
        return list(ad), list(eco)

    def set_user(self, user: UserMock):
        self.chat_id = user.chat_id
        self.user_additives = user.get_additives_names()
        self.additives, self.ecodes = self._find_additives()

    def get_evaluation(self) -> str:
        print(f'{datetime.now()} --- Getting evalution for {self.chat_id}')
        text = ''
        if self.additives:
            text += 'Из твоего чёрного списка:\n' + ', '.join(self.additives)
        if self.ecodes:
            text += '\n\nЕ-добавки:'

        if not text:
            text = 'All is good!'
        return text
