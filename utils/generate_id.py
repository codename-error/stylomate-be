from cachetools import TTLCache

cache = TTLCache(maxsize=10000, ttl=120)

def generateNewID(uid: str):
    if uid in cache:
        cache[uid] = cache.get(uid) + 1
    else:
        cache[uid] = 1

    return cache.get(uid)