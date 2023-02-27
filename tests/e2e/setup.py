import pytest_asyncio
from telethon import TelegramClient
from tests.e2e.data.config import API_ID, API_HASH


@pytest_asyncio.fixture
async def client() -> TelegramClient:
    return TelegramClient('testing', API_ID, API_HASH)
