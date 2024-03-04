import asyncio
from config import API_ID, API_HASH
from telegram import TelegramAPI


async def main():
    telegram_api = TelegramAPI(API_ID, API_HASH)
    await telegram_api.auth()
    all_info_about_chat_raw = await telegram_api.get_channel_data_from_link('https://t.me/Python_parsing_chat')
    all_messages_in_chat_raw = await telegram_api.get_messages(all_info_about_chat_raw.id)
    for message in all_messages_in_chat_raw:
        print(message)

    # Получение пользователей из чата
    all_users_in_chat_raw = await telegram_api.get_users(all_info_about_chat_raw.id)


    # Обновление информации о чате


    # Остановка клиента TelegramClient
    await telegram_api.stop()


# Запуск основного кода в асинхронной среде
asyncio.run(main())
