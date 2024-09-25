import random
import string
from typing import Optional


def generate_token(length: Optional[int] = 12) -> str:
    chars = string.ascii_letters + string.digits
    token = ''.join(random.choice(chars) for _ in range(length))
    return token
