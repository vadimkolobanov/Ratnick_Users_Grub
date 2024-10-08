import asyncio
import json
import logging

import requests

from config import API_ID, API_HASH, POSTGRES_DBNAME, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
from database import Database
from push_data_in_database import process_messages, process_users, process_channels
from telegram_factory import TelegramAPI


async def main():
    telegram_api = TelegramAPI(API_ID, API_HASH)
    db = Database(db_name=POSTGRES_DBNAME, user=POSTGRES_USER, passwd=POSTGRES_PASSWORD, host=POSTGRES_HOST,
                  port=POSTGRES_PORT)

    await telegram_api.auth()
    while True:
        db.connect()
        # db.create_tables()
        target_new = db.get_target()
        if target_new is None:
            target = db.get_channel_for_update_raw()
        else:
            target = target_new
            db.close_target(target)


        chat_https_link = target
        all_info_about_chat_raw = await telegram_api.get_channel_data_from_link(chat_https_link)
        all_messages_in_chat_raw = await telegram_api.get_messages(all_info_about_chat_raw.id)
        all_users_in_chat_raw = await telegram_api.get_users(all_info_about_chat_raw.id)
        process_channels(all_info_about_chat_raw, db, chat_https_link)
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post('http://localhost:8080/insert-users', headers=headers, data=json.dumps(all_users_in_chat_raw))
            if response.status_code == 200:
                print("Data sent successfully")
            else:
                print(f"Failed to send data: {response.status_code}, {response.text}")
        except requests.exceptions.ConnectionError as e:
            logging.warning('Not connected')

        # process_users(all_users_in_chat_raw, all_info_about_chat_raw, db)
        # process_messages(all_messages_in_chat_raw, db, all_info_about_chat_raw)

        db.close()
    await telegram_api.stop()


asyncio.run(main())
