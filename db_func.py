import asyncpg
from general_file import DATABASE_URL


async def select_target():
    pool = await asyncpg.create_pool(DATABASE_URL)
    try:
        async with pool.acquire() as conn:
            s = "SELECT link, id FROM general_targetsource WHERE completed = false LIMIT 1"
            record = await conn.fetchrow(s)
            return record
    except Exception as e:
        print(e)
    finally:
        # Закрываем пул соединений
        await pool.close()


async def select_data_from_db():
    pool = await asyncpg.create_pool(DATABASE_URL)
    try:
        # Создаем пул соединений с базой данных

        async with pool.acquire() as conn:
            # Ваш SELECT-запрос
            sql = "SELECT * FROM scrap_app_sessions"
            # Выполняем запрос с параметрами
            result = await conn.fetch(sql)

            return result  # Возвращаем результат запроса
    except Exception as e:
        print(e)
    finally:
        # Закрываем пул соединений
        await pool.close()


async def update_target_completed_by_link(link):
    pool = await asyncpg.create_pool(DATABASE_URL)
    try:
        # Создаем пул соединений с базой данных

        async with pool.acquire() as conn:
            s = "UPDATE general_targetsource SET completed = true WHERE link = $1 AND completed = false"
            record = await conn.fetchval(s, link)
            return record
    except Exception as e:
        print(e)
    finally:
        # Закрываем пул соединений
        await pool.close()


async def get_channels():
    pool = await asyncpg.create_pool(DATABASE_URL)
    try:
        # Создаем пул соединений с базой данных

        async with pool.acquire() as conn:
            s = "SELECT * FROM general_channels"
            records = await conn.fetch(s)

            return records
    except Exception as e:
        print(e)
    finally:
        # Закрываем пул соединений
        await pool.close()


async def insert_channel(channel, link):
    pool = await asyncpg.create_pool(DATABASE_URL)
    try:
        # Создаем пул соединений с базой данных
        async with pool.acquire() as conn:
            s = "INSERT INTO general_channels (id_channel, title, link,chat_id) VALUES ($1, $2, $3, $4) ON CONFLICT (id_channel) DO NOTHING"
            record = await conn.fetchval(s, channel.id, channel.title, link,1)
            return record
    except Exception as e:
        print(e)
    finally:
        # Закрываем пул соединений
        await pool.close()
