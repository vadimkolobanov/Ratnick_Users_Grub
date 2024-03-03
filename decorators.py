import asyncio
import logging
import time
from functools import wraps

import asyncpg

from general_file import DATABASE_URL


def retry(max_retries=3, delay=1):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logging.error(f"Ошибка выполнения функции {func.__name__}: {e}")
                    retries += 1
                    await asyncio.sleep(delay)
            logging.error(f"Превышено максимальное количество попыток выполнения функции {func.__name__}")
        return wrapper
    return decorator


def rate_limit(max_calls=5, period=60):
    def decorator(func):
        last_called = 0
        calls = 0

        async def wrapper(*args, **kwargs):
            nonlocal last_called, calls

            now = time.time()
            if now - last_called > period:
                last_called = now
                calls = 1
            else:
                calls += 1
                if calls > max_calls:
                    wait_time = period - (now - last_called)
                    await asyncio.sleep(wait_time)
                    last_called = time.time()
                    calls = 1

            return await func(*args, **kwargs)
        return wrapper
    return decorator


def database_connection(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with asyncpg.create_pool(DATABASE_URL, max_size=10) as pool:
            async with pool.acquire() as conn:
                kwargs['conn'] = conn
                return await func(*args, **kwargs)
    return wrapper