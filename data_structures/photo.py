from telebot import TeleBot
from telebot.types import Message
from datetime import datetime
from io import BytesIO
from PIL import Image


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
