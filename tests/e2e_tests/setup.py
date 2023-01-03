import pytest_asyncio
from telethon import TelegramClient
from os import environ


@pytest_asyncio.fixture
async def client() -> TelegramClient:
    return TelegramClient('testing', 
    environ.get('API_ID'), 
    environ.get('API_HASH'))
