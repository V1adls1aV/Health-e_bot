import asyncio
from telethon import TelegramClient

from tests.e2e_tests.setup import client  # importing fixture
from tests.e2e_tests.data.config import API_ID, API_HASH, BOT_NAME, MESDELAY, \
    TEXT1, TEXTRES1, TEXT2, TEXTRES2, TEXT3, TEXTRES3


async def test_message1(client: TelegramClient):
    async with client:
        await client.send_message(BOT_NAME, TEXT1)
        await asyncio.sleep(MESDELAY)

        message = (await client.get_messages(BOT_NAME))[0]
        assert message.text == TEXTRES1


async def test_message2(client: TelegramClient):
    async with client:
        await client.send_message(BOT_NAME, TEXT2)
        await asyncio.sleep(MESDELAY)

        message = (await client.get_messages(BOT_NAME))[0]
        result = [
            message.text,
            *[el.buttons[0].text for el in message.reply_markup.rows]
        ]
        assert result == TEXTRES2


async def test_message3(client: TelegramClient):
    async with client:
        await client.send_message(BOT_NAME, TEXT3)
        await asyncio.sleep(MESDELAY)
        message = (await client.get_messages(BOT_NAME))[0]

        result = [
            message.text,
            *[el.buttons[0].text for el in message.reply_markup.rows]
        ]
        assert result == TEXTRES3


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        test_message3(
            TelegramClient('testing', API_ID, API_HASH).start()
            )
        )
