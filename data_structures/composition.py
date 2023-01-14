from data_structures.additive_list import AdditiveList
from objects.ecode import ECode
from objects.user import User
from datetime import datetime
from fuzzysearch import find_near_matches


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

            for item in self.user_additives:  # Black list
                if find_near_matches(item, el, max_l_dist=2):
                    ad.add(item)
            for item in self.user_ecodes.values():  # E-codes
                if item in el:
                    eco.add(item)
            for item in self.user_ecodes.keys():  # E-names
                if item in el:
                    eco.add(self.user_ecodes[item])
        return list(ad), list(eco)

    def set_user(self, user: User):
        self.chat_id = user.chat_id
        self.user_additives = user.get_additives_names()
        self.additives, self.ecodes = self._find_additives()

    def get_evaluation(self) -> str:
        print(f'{datetime.now()} --- Getting evalution for {self.chat_id}')
        text = ''
        if self.additives:
            text += 'Из твоего чёрного списка:\n' + ', '.join(self.additives)
        if self.ecodes:
            text += '\n\nЕ-добавки: (Вредность)'

        if not text:
            text = 'Возможно, это тебе подходит!'
        return text
