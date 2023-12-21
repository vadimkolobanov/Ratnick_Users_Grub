import asyncio
import asyncpg
from tqdm.asyncio import tqdm_asyncio

from general_file import DATABASE_URL

async def get_chat_participants(client, channel):
    try:
        async with asyncpg.create_pool(DATABASE_URL) as pool:
            async with pool.acquire() as conn:
                async for participant in tqdm_asyncio(
                    client.iter_participants(channel),
                    desc=f'Сбор пользователей {channel.title}',
                ):
                    first_name = participant.first_name if participant.first_name else 'Не указано'
                    username = participant.username if participant.username else 'Не указано'
                    last_name = participant.last_name if participant.last_name else 'Не указано'
                    phone = participant.phone if participant.phone else 'Not'
                    sql = """INSERT INTO general_users (user_id, first_name, last_name, username, phone, channel_id_id)
                            VALUES ($1, $2, $3, $4, $5, $6)
                            ON CONFLICT DO NOTHING;"""
                    await conn.execute(
                        sql,
                        participant.id,
                        first_name,
                        last_name,
                        username,
                        phone,
                        channel.id,
                    )
    except Exception as e:
        print(e)