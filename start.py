import asyncio
import logging
import random

from telethon import TelegramClient
import users
from db_func import *
from general_file import *

username, api_id, api_hash = USERNAME, API_ID, API_HASH

client = TelegramClient(username, api_id, api_hash)
client.start()


async def process_channel(client, channel_id):
    try:

        channel = await client.get_entity(channel_id)

        await insert_channel(channel=channel, link=channel_id)
        await users.get_chat_participants(channel=channel, client=client)
        await update_target_completed_by_link(channel_id)
        await insert_channel(channel=channel, link=channel_id)
    except Exception as e:
        logging.error(f"Error processing channel {channel_id}: {e}")
        await update_target_completed_by_link(channel_id)


async def main(client):
    while True:
        new_target = await select_target()
        if new_target:
            try:
                await asyncio.sleep(random.randint(2, 10))

                await process_channel(client, new_target[0])
            except Exception as e:
                logging.error(f"Error processing new target {new_target[0]}: {e}")
        else:

            try:
                await asyncio.sleep(random.randint(5, 10))
                channel_list = await get_channels()

                tasks = [process_channel(client, channel[2]) for channel in channel_list]
                await asyncio.gather(*tasks)
            except Exception as e:
                logging.error(f"Error processing channel list: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    with client:
        client.loop.run_until_complete(main(client))
