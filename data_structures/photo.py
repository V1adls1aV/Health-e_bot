from telebot import TeleBot
from telebot.types import Message
from pytesseract import image_to_string
from datetime import datetime
from io import BytesIO
from PIL import Image

from tf_models.text_model import TextModel
from data.config import TESS_CONFIG


class Photo:
    def __init__(self, bot: TeleBot, message: Message) -> None:
        self.bot = bot
        self.message = message
        self.image = self._get_image()

    def _get_image(self) -> Image:  # Get image from server
        print(f'{datetime.now()} --- Getting image from server')
        image_id = self.message.photo[-1].file_id
        image_bytes = self.bot.download_file(
            self.bot.get_file(image_id).file_path
            )
        with BytesIO(image_bytes) as stream:
            return Image.open(stream).convert('RGB')

    def is_text(self) -> bool:
        model = TextModel()
        prediction = model.predict(self.image)
        print(f'{datetime.now()} --- Is text checking {prediction}')

        if prediction > 0.8:
            return True
        return False

    def get_text(self):
        print(f'{datetime.now()} --- Getting text from image')
        text = image_to_string(self.image, lang='rus', config=TESS_CONFIG)
        print('__________________________________')
        print('Recognized text:')
        print(text)
        print('__________________________________')
        return text
