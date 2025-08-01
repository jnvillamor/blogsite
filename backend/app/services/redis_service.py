from typing import Union
from datetime import timedelta
import redis

class RedisService:
  def __init__(self):
    self.redis = redis.Redis(
      host='redis',
      port=6379,
      db=0
    )
  
  def set(self, key: str, value: str, ex: Union[int, timedelta] = None):
    """Set a key-value pair in Redis with an optional expiration time."""
    try:
      self.redis.set(key, value, ex=ex)
    except redis.RedisError as e:
      raise Exception(f"Redis error: {str(e)}")
  
  def get(self, key: str) -> Union[str, None]:
    """Get a value by key from Redis."""
    try:
      value = self.redis.get(key)
      return value.decode('utf-8') if value else None
    except redis.RedisError as e:
      raise Exception(f"Redis error: {str(e)}")
  
  def delete(self, key: str):
    """Delete a key from Redis."""
    try:
      self.redis.delete(key)
    except redis.RedisError as e:
      raise Exception(f"Redis error: {str(e)}") 
  