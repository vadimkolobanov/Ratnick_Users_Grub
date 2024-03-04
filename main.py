import asyncio
from config import API_ID, API_HASH
from database import Database
from raw_telegram_data_sort import process_messages, process_users
from telegram_factory import TelegramAPI


async def main():
    telegram_api = TelegramAPI(API_ID, API_HASH)
    db = Database('mydatabase.db')
    db.connect()
    db.create_tables()
    db.close()
    await telegram_api.auth()
    all_info_about_chat_raw = await telegram_api.get_channel_data_from_link('https://t.me/Python_parsing_chat')
    all_messages_in_chat_raw = await telegram_api.get_messages(all_info_about_chat_raw.id)
    all_users_in_chat_raw = await telegram_api.get_users(all_info_about_chat_raw.id)
    process_messages(all_messages_in_chat_raw)
    process_users(all_users_in_chat_raw, all_info_about_chat_raw, db)

    # Обновление информации о чате

    # Остановка клиента TelegramClient
    await telegram_api.stop()


# Запуск основного кода в асинхронной среде
asyncio.run(main())
