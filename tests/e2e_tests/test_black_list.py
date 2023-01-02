import asyncio
from telethon import TelegramClient

from tests.e2e_tests.setup import client  # importing fixture
from tests.e2e_tests.data.config import API_ID, API_HASH, BOT_NAME, \
    BLRES1, BL2, BLRES2, BL3, BLRES3, BLDELAY


async def test_getting(client: TelegramClient):
    # User have to have black list with 'сахар', 'молоко'
    async with client:
        await client.send_message(BOT_NAME, 'Чёрный список')
        await asyncio.sleep(BLDELAY)

        message = (await client.get_messages(BOT_NAME))[0]
        await message.click(0)  # Clicking getting button
        await asyncio.sleep(BLDELAY)

        message = (await client.get_messages(BOT_NAME))[0]
        assert message.text == BLRES1


async def test_adding(client: TelegramClient):
    # User have to have black list with 'сахар', 'молоко'
    async with client:
        await client.send_message(BOT_NAME, 'Чёрный список')
        await asyncio.sleep(BLDELAY)

        message = (await client.get_messages(BOT_NAME))[0]
        await message.click(1)  # Clicking adding button
        await asyncio.sleep(BLDELAY)

        message = (await client.get_messages(BOT_NAME))[0]
        assert message.text == 'Пришли названия элементов через запятую'

        await client.send_message(BOT_NAME, BL2)
        await asyncio.sleep(BLDELAY)

        message = await client.get_messages(BOT_NAME, limit=3)
        assert [message[2 - i].text for i in range(3)] == BLRES2


async def test_deleting(client: TelegramClient):
    # User have to have black list with 'сахар', 'молоко', 'фундук'
    async with client:
        await client.send_message(BOT_NAME, 'Чёрный список')
        await asyncio.sleep(BLDELAY)

        message = (await client.get_messages(BOT_NAME))[0]
        await message.click(2)  # Clicking deleting button
        await asyncio.sleep(BLDELAY)

        message = (await client.get_messages(BOT_NAME))[0]
        assert message.text == 'Пришли названия элементов через запятую'

        await client.send_message(BOT_NAME, BL3)
        await asyncio.sleep(BLDELAY)

        message = await client.get_messages(BOT_NAME, limit=3)
        assert [message[2 - i].text for i in range(3)] == BLRES3


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        test_adding(
            TelegramClient('testing', API_ID, API_HASH).start()
            )
        )
