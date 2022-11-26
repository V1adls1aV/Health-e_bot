from objects.user import User
from objects.eadditive import EAdditive


class AdditiveList(list):
    def __init__(self, text: str) -> None:
        self.raw_text = text
        self.text = self._filter_text()
        super().__init__(self.text)

    def _filter_text(self) -> list[str]:  # Filter the text
        res = []
        for word in self.raw_text.split(','):
            if word:
                name = ''
                for letter in word.strip().lower():
                    if letter.isalpha() or letter.isalnum() or letter in ' -':
                        name += letter
                if name:
                    res.append(name)
        return res


class Composition(AdditiveList):
    def __init__(self, user: User, text: str) -> None:
        super().__init__(text)  # Getting self.text and self.raw_text
        self.user_additives = user.get_additives_names()
        self.user_e_additives = EAdditive.get_e_numbers()
        self.user_e_additives += EAdditive.get_e_names()
        self.additives, self.e_additives = self._find_additives()

    def _find_additives(self) -> list[str]:
        ad, ead = set(), set()
        for el in self.text:
            if el[0] == 'e' and len(el) > 1:
                el = 'е' + el[1:]  # Solving problem with russian and english E letter

            for a in self.user_additives:
                if a in el:
                    ad.add(a)
            for e in self.user_e_additives:
                if e in el:
                    ead.add(e)
        return list(ad), list(ead)

    def get_evaluation(self) -> str:
        text = ''
        if self.additives:
            text += 'Из вашего чёрного списка:\n' + ', '.join(self.additives)
        if self.e_additives:
            text += '\n\nЕ-добавки:\n' + ', '.join(self.e_additives)
        if not text:
            text = 'All is good!'
        return text
