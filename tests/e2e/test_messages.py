import asyncio
from telethon import TelegramClient

from tests.e2e.setup import client  # importing fixture
from tests.e2e.data.config import BOT_NAME, CLICKDELAY, \
    TEXT1, TEXTRES1, TEXT2, TEXTRES2, TEXT3, TEXTRES3


async def test_message1(client: TelegramClient):
    async with client:
        await client.send_message(BOT_NAME, TEXT1)
        await asyncio.sleep(CLICKDELAY)

        message = (await client.get_messages(BOT_NAME))[0]
        assert message.text == TEXTRES1


async def test_message2(client: TelegramClient):
    async with client:
        await client.send_message(BOT_NAME, TEXT2)
        await asyncio.sleep(CLICKDELAY)

        message = (await client.get_messages(BOT_NAME))[0]
        result = {
            *[el.buttons[0].text for el in message.reply_markup.rows]  # ECodes
        }
        assert result == TEXTRES2


async def test_message3(client: TelegramClient):
    async with client:
        await client.send_message(BOT_NAME, TEXT3)
        await asyncio.sleep(CLICKDELAY)
        message = (await client.get_messages(BOT_NAME))[0]

        result = {
            *message.text.split('\n')[1].split(', '),  # BL elements
            *[el.buttons[0].text for el in message.reply_markup.rows]  # ECodes
        }
        assert result == TEXTRES3
