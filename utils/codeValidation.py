import random
from cachetools import TTLCache

cache = TTLCache(maxsize=1000, ttl=120)


def generateCode(email: str):
    verification_code_list = []

    for _ in range(1, 6):
        # Generate random 6-digit verification code
        verification_code = random.randint(1, 10)
        verification_code = str(verification_code)

        verification_code_list.append(verification_code)

    result_verification_code = "".join(verification_code_list)
    cache[email] = result_verification_code

    return result_verification_code

async def verifyCode(email: str, code: int):
    stored_code = cache.get(email)
    verification_code = str(code)
    if stored_code == verification_code:
        cache.pop(email, None)
        print("email berhasil veirify")
        return True
    else:
        return False