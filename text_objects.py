from objects.user import User
from objects.eadditive import EAdditive
from data.config import BADDEGREE, NORMALDEGREE, GOODDEGREE


class AdditiveList(list):
    def __init__(self, text: str) -> None:
        self.raw_text = text
        self.text = self._filter_text()
        super().__init__(self.text)

    def _filter_text(self) -> list[str]:  # Filter the text
        res = []
        for word in self.raw_text.split(','):
            if not word:
                continue
            res.append('')
            for letter in word.lower():
                if letter.isalpha() or letter.isalnum():
                    res[-1] += letter
        return res


class Composition(AdditiveList):
    def __init__(self, user: User, text: str) -> None:
        super().__init__(text)  # Getting self.text and self.raw_text
        self.user_additives = user.get_additives_names()
        self.user_additives += EAdditive.get_e_numbers()
        self.user_additives += EAdditive.get_e_names()
        self.additives = self._find_additives()

    def _find_additives(self) -> list[str]:
        res = []
        for el in self.text:
            if el[0] == 'e':  # Solving problem with russian and english E letter
                el = 'е' + el[1:]  # Remake this

            if el in self.user_additives:
                res.append(el)
        return res

    def get_additives_names(self) -> list[str]:
        return self.additives

    def get_evaluation(self) -> str:  # You should evalute with DEGREEs constants
        if self.additives:
            return ', '.join(self.additives)  # So, you have to add to db column with degrees (0, 1, 2...)
        else:  # It will be good to use EAdditive
            return 'All is good!'