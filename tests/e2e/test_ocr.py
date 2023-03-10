import asyncio
from telethon import TelegramClient

from tests.e2e.setup import client  # importing fixture
from tests.e2e.data.config import BOT_NAME, IMAGES_PATH, \
    OCRRES1, OCRRES2, OCRRES3, OOPSMESSAGE, \
    OCRDELAY, CLICKDELAY, E450, E211, E306


async def test_ocr1(client: TelegramClient):
    async with client:
        await client.send_file(BOT_NAME, 
            open(IMAGES_PATH + 'im1.jpg', 'rb'))
        await asyncio.sleep(OCRDELAY)

        message = (await client.get_messages(BOT_NAME))[0]
        result = {
            *message.text.split('\n')[1].split(', ')
        }
        assert result == OCRRES1



async def test_ocr2(client: TelegramClient):
    async with client:
        await client.send_file(BOT_NAME, 
            open(IMAGES_PATH + 'im2.jpg', 'rb'))
        await asyncio.sleep(OCRDELAY)

        message = (await client.get_messages(BOT_NAME, limit=2))[1]
        print(await client.get_messages(BOT_NAME, limit=2))
        result = {
            *message.text.split('\n')[1].split(', '),
            *[el.buttons[0].text for el in message.reply_markup.rows]
        }
        assert result == OCRRES2

        await message.click(0)  # Clicking e450 button
        await asyncio.sleep(CLICKDELAY)
        message = (await client.get_messages(BOT_NAME))[0]
        assert message.text == E450



async def test_ocr3(client: TelegramClient):
    async with client:
        await client.send_file(BOT_NAME, 
            open(IMAGES_PATH + 'im3.jpg', 'rb'))
        await asyncio.sleep(OCRDELAY)

        message = (await client.get_messages(BOT_NAME, limit=2))[1]
        result = {
            *message.text.split('\n')[1].split(', '),
            *[el.buttons[0].text for el in message.reply_markup.rows]
        }
        assert result == OCRRES3

        await message.click(0)  # Clicking e211 button
        await asyncio.sleep(CLICKDELAY)
        mes = (await client.get_messages(BOT_NAME))[0]
        assert mes.text == E211

        await message.click(6)  # Clicking e306 button
        await asyncio.sleep(CLICKDELAY)        
        mes = (await client.get_messages(BOT_NAME))[0]
        assert mes.text == E306



async def test_ocr4(client: TelegramClient):
    async with client:
        await client.send_file(BOT_NAME, 
            open(IMAGES_PATH + 'im4.jpg', 'rb'))
        await asyncio.sleep(CLICKDELAY)

        message = (await client.get_messages(BOT_NAME))[0]
        assert message.text in OOPSMESSAGE



async def test_ocr5(client: TelegramClient):
    async with client:
        await client.send_file(BOT_NAME, 
            open(IMAGES_PATH + 'im5.jpg', 'rb'))
        await asyncio.sleep(CLICKDELAY)

        message = (await client.get_messages(BOT_NAME))[0]
        assert message.text in OOPSMESSAGE
