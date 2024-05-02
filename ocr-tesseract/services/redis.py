import json
from typing import Any, Optional, cast

import redis
import redis.asyncio as aioredis
from config import settings

HOUR_TTL = 60 * 60
DAY_TTL = HOUR_TTL * 24
WEEK_TTL = DAY_TTL * 7
MONTH_TTL = DAY_TTL * 30

_key_T = str
_value_T = str | bytes | dict[str, Any] | list[Any]


def prefix_key(key: _key_T) -> str:
    return f"{settings.BASE_DIR.name}:{settings.APP_VERSION}:{key}"


def is_json(value: str, *, return_json: bool = False) -> bool | dict[str, Any] | list[Any]:
    try:
        json_value = json.loads(value)

        if not isinstance(json_value, (dict, list)):
            raise ValueError

        if return_json:
            return json_value

        return True
    except ValueError:
        return False


class _Redis:
    """
    Singleton for Redis connection pool.

    So that pool should be initialized only once.

    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            pool = redis.ConnectionPool.from_url(str(settings.REDIS_URL), max_connections=10, decode_responses=True)
            cls._instance = redis.Redis(connection_pool=pool)
        return cls._instance


class _AsyncRedis:
    _instance = None  # type: ignore

    def __new__(cls):
        if cls._instance is None:
            pool = aioredis.ConnectionPool.from_url(str(settings.REDIS_URL), max_connections=10, decode_responses=True)
            cls._instance = aioredis.Redis(connection_pool=pool)
        return cls._instance


redis_client: redis.Redis = _Redis()  # type: ignore
redis_client_async: aioredis.Redis = _AsyncRedis()  # type: ignore


def set_key(key: _key_T, value: _value_T, *, ttl: Optional[int] = MONTH_TTL) -> None:
    key = prefix_key(key)
    if isinstance(value, (dict, list)):
        value = json.dumps(value, separators=(",", ":"))

    redis_client.set(key, value, ex=ttl)  # type: ignore


async def set_key_async(key: _key_T, value: _value_T, *, ttl: int = MONTH_TTL, is_transaction: bool = False) -> None:
    key = prefix_key(key)
    if isinstance(value, (dict, list)):
        value = json.dumps(value, separators=(",", ":"))

    async with redis_client_async.pipeline(transaction=is_transaction) as pipe:
        await pipe.set(key, value)
        if ttl:
            await pipe.expire(key, ttl)

        await pipe.execute()


def _returnable_value(value: Any) -> str | dict[str, Any] | list[Any] | None:
    if not value:
        return None

    if isinstance(value, bytes):
        value = value.decode("utf-8")

    value = cast(str, value)

    json_value = is_json(value, return_json=True)
    if json_value:
        return cast(dict[str, Any], json_value)

    return value


def get_key(key: _key_T) -> str | dict[str, Any] | list[Any] | None:
    key = prefix_key(key)
    value = redis_client.get(key)  # type: ignore
    return _returnable_value(value)


async def get_key_async(key: _key_T) -> str | dict[str, Any] | list[Any] | None:
    key = prefix_key(key)
    value = await redis_client_async.get(key)  # type: ignore
    return _returnable_value(value)


def delete_key(key: _key_T) -> None:
    key = prefix_key(key)
    redis_client.delete(key)  # type: ignore


async def delete_key_async(key: _key_T) -> None:
    key = prefix_key(key)
    await redis_client_async.delete(key)  # type: ignore


def flush() -> None:
    redis_client.flushall()  # type: ignore


def flush_async() -> None:
    redis_client_async.flushall()  # type: ignore
