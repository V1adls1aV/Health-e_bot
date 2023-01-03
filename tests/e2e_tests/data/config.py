BOT_NAME = 'health_e_bot'
IMAGES_PATH = 'tests/e2e_tests/data/images/'

MESDELAY = 1
TEXT1 = 'something, test.., нут,греча '
TEXTRES1 = 'All is good!'
TEXT2 = 'е123, е410, ...'
TEXTRES2 = [
    'Е-добавки:',
    'е123 (Очень высокая)',
    'е410 (Нулевая)'
]
TEXT3 = 'молоко,сахар,   е510, .smth else ,е507'
TEXTRES3 = [
    'Из твоего чёрного списка:\nмолоко, сахар\n\nЕ-добавки:',
    'е510 (Средняя)',
    'е507 (Низкая)'
]


OCRDELAY = 5
OCRRES1 = 'Из твоего чёрного списка:\nсахар'
OCRRES2 = [
    'Из твоего чёрного списка:\nмолоко, сахар\n\nЕ-добавки:',
    'е407 (Нулевая)',
    'е410 (Нулевая)'
]
OCRRES3 = [
    'Из твоего чёрного списка:\nмолоко\n\nЕ-добавки:',
    'е211 (Высокая)',
    'е509 (Низкая)',
    'е322 (Очень низкая)',
    'е160a (Очень низкая)',
    'е290 (Очень низкая)',
    'е306 (Нулевая)',
]


BLDELAY = 1
BLRES1 = 'Твой чёрный список:\nсахар, молоко.'
BL2 = 'Молоко, кешью'
BLRES2 = [
    'Элемент "молоко" уже есть в списке',
    'Элемент "кешью" успешно добавлен',
    'Твой чёрный список:\nсахар, молоко, кешью.'
]
BL3 = 'Фундук, кешью'
BLRES3 = [ 
    'Элемент "фундук" был удалён ранее',
    'Элемент "кешью" успешно удалён',
    'Твой чёрный список:\nсахар, молоко.'
]