import pytest_asyncio
from telethon import TelegramClient
from tests.e2e_tests.data.config import API_HASH, API_ID


@pytest_asyncio.fixture
async def client() -> TelegramClient:
    return TelegramClient('testing', API_ID, API_HASH)
