from telebot import TeleBot
from telebot.types import Message
from datetime import datetime
import openfoodfacts as off
from pyzbar import pyzbar
import pytesseract

from data.config import TESS_CONFIG
from tf_models.text_model import TextModel
from data_structures.photo import Photo


class Product(Photo):
    def __init__(self, bot: TeleBot, message: Message) -> None:
        super().__init__(bot, message)  # getting self.image and others
        self.barcode = self._extract_barcode()
        self.received_text = self._receive_text()
        self.is_text = self._is_text()
        self.recognized_text = None
        

    def _extract_barcode(self) -> str or None:
        print(f'{datetime.now()} --- Extracting barcode from image')
        res = pyzbar.decode(self.image)
        if res:
            return res[0].data.decode()
        return None


    def _is_text(self) -> bool:
        print(f'{datetime.now()} --- Is text checking for {self.message.chat.id}')
        
        model = TextModel()
        prediction = model.predict(self.image)
        print(f'{datetime.now()} --- Is text {prediction}')

        is_text = False
        if prediction >= 0.5:
            is_text = True
        return is_text


    def _receive_text(self) -> str or None:
        try:
            return off.products.get_product(
                self.barcode)['product']['ingredients_text'] 
        except:
            return None  # There is no product text available
    
        
    def extract_text(self) -> str:
        print(f'{datetime.now()} --- Extracting text from image')
        self.recognized_text = pytesseract.image_to_string(
            self.image, lang='rus', config=TESS_CONFIG
            )
        print('__________________________________')
        print('Recognized text:')
        print(self.recognized_text)
        print('__________________________________')
        return self.recognized_text
