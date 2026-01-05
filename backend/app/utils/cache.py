import json
from typing import Any
import redis

# Connect to Redis 
redis_client = redis.Redis(
    host="redis",  
    port=6379,
    db=0,
    decode_responses=True  
)


def get_cache(key: str) -> Any | None:
    """
    Get a value from cache.
    Returns None if not found or expired.
    """
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception:
        return None


def set_cache(key: str, value: Any, expire: int = 300) -> None:
    """
    Save a value to cache.
    
    Args:
        key: Cache key (e.g., "user:123:assignments")
        value: Any JSON-serializable value
        expire: Seconds until cache expires (default: 5 minutes)
    """
    try:
        redis_client.setex(
            key,
            expire,
            json.dumps(value, default=str)  
        )
    except Exception:
        pass  


def delete_cache(key: str) -> None:
    """
    Delete a key from cache (invalidation).
    """
    try:
        redis_client.delete(key)
    except Exception:
        pass
