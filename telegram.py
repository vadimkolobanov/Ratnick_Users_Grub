from telethon import TelegramClient


class TelegramAPI:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient('session', api_id, api_hash)

    async def auth(self):
        # Метод для авторизации клиента TelegramClient
        await self.client.start()

    async def get_messages(self, chat_id):
        return 'Ответ от get messages'


    async def get_users(self, chat_id):
        # Метод для получения пользователей из чата с заданным chat_id
        pass

    async def update_chat_info(self, chat_id):
        # Метод для обновления информации о чате (участники, сообщения и т.д.)
        pass

    async def stop(self):
        # Остановка клиента TelegramClient
        await self.client.disconnect()
