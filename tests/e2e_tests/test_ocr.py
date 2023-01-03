import asyncio
from telethon import TelegramClient

from tests.e2e_tests.setup import client  # importing fixture
from tests.e2e_tests.data.config import BOT_NAME, IMAGES_PATH, \
    OCRRES1, OCRRES2, OCRRES3, OCRDELAY


async def test_ocr1(client: TelegramClient):
    async with client:
        await client.send_file(BOT_NAME, 
            open(IMAGES_PATH + 'im1.jpg', 'rb'))
        await asyncio.sleep(OCRDELAY)

        message = (await client.get_messages(BOT_NAME))[0]
        assert message.text == OCRRES1


async def test_ocr2(client: TelegramClient):
    async with client:
        await client.send_file(BOT_NAME, 
            open(IMAGES_PATH + 'im2.jpg', 'rb'))
        await asyncio.sleep(OCRDELAY)

        message = (await client.get_messages(BOT_NAME))[0]
        result = {
            *message.text.split('\n')[1].split(', '),
            *[el.buttons[0].text for el in message.reply_markup.rows]
        }
        assert result == OCRRES2


async def test_ocr3(client: TelegramClient):
    async with client:
        await client.send_file(BOT_NAME, 
            open(IMAGES_PATH + 'im3.jpg', 'rb'))
        await asyncio.sleep(OCRDELAY)

        message = (await client.get_messages(BOT_NAME))[0]
        result = {
            *message.text.split('\n')[1].split(', '),
            *[el.buttons[0].text for el in message.reply_markup.rows]
        }
        assert result == OCRRES3
