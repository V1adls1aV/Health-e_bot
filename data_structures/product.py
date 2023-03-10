from telebot import TeleBot
from telebot.types import Message
from datetime import datetime
import openfoodfacts as off
from pyzbar import pyzbar
import pytesseract
import requests

from data.config import TESS_CONFIG, OFF_USERNAME, OFF_PASSWORD
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
            for el in res:
                if el.type != 'QRCODE':
                    return el.data.decode()
            return None
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
        print(f'{datetime.now()} --- Receiving text from OFF')
        try:
            return off.products.get_product(
                self.barcode)['product']['ingredients_text_ru'] 
        except:
            return None  # There is no product composition available


    def extract_text(self) -> str:
        if self.recognized_text:
            raise Exception('Text has already extracted')

        print(f'{datetime.now()} --- Extracting text from image')
        self.recognized_text = pytesseract.image_to_string(
            self.image, lang='rus', config=TESS_CONFIG
            )
        return self.recognized_text


    def send_to_OFF(self):
        if not (self.barcode and self.recognized_text):
            raise ValueError('There is lack of product info.')

        print(f'{datetime.now()} --- Senging product ({self.barcode}) to OFF')
        url = off.utils.build_url(
        geography='world',
        service='cgi',
        resource_type='product_jqm2.pl')

        status = requests.post(
            url, data={
            'code': self.barcode,
            'user_id': OFF_USERNAME,
            'password': OFF_PASSWORD,
            'lang': 'rus',
            'ingredients_text_ru': self.recognized_text
        })
        print(f'{datetime.now()} --- Sending status: {status}')
