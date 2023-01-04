from data.config import TESS_CONFIG
from pytesseract import image_to_string
from PIL.Image import open as open_image
from datetime import datetime
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
