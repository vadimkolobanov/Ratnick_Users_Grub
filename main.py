import asyncio
from config import API_ID, API_HASH
from telegram import TelegramAPI


async def main():
    telegram_api = TelegramAPI(API_ID, API_HASH)

    # Авторизация
    await telegram_api.auth()

    # Получение сообщений из чата
    chat_id = 'your_chat_id'
    messages = await telegram_api.get_messages(chat_id)
    print(messages)

    # Получение пользователей из чата
    users = await telegram_api.get_users(chat_id)
    print(users)

    # Обновление информации о чате
    await telegram_api.update_chat_info(chat_id)

    # Остановка клиента TelegramClient
    await telegram_api.stop()


# Запуск основного кода в асинхронной среде
asyncio.run(main())
