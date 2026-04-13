import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

# 如果没有配置Redis，使用内存缓存作为降级方案
class MemoryCache:
    def __init__(self):
        self.cache = {}
    
    def get(self, key):
        return self.cache.get(key)
    
    def setex(self, key, expire, value):
        self.cache[key] = value

# 初始化缓存
try:
    if REDIS_URL:
        cache = redis.from_url(REDIS_URL, decode_responses=True)
        cache.ping()
        print("Redis缓存已连接")
    else:
        cache = MemoryCache()
        print("使用内存缓存")
except Exception as e:
    print(f"Redis连接失败，使用内存缓存: {e}")
    cache = MemoryCache()

def get_cached_result(key: str):
    """获取缓存结果"""
    try:
        value = cache.get(key)
        if value:
            return json.loads(value)
        return None
    except:
        return None

def set_cached_result(key: str, value: dict, expire: int = 3600):
    """设置缓存结果"""
    try:
        cache.setex(key, expire, json.dumps(value, ensure_ascii=False))
    except:
        pass
