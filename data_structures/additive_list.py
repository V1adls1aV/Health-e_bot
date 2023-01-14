from datetime import datetime


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
                    if letter.isalpha() or letter.isalnum() or letter == ' ':
                        name += letter
                if name:
                    res.append(name.strip())
        print(f'{datetime.now()} --- Filtered text: {res}')
        return res
