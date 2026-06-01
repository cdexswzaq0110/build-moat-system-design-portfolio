import secrets
import string


TOKEN_ALPHABET = string.ascii_letters + string.digits


def generate_token(length: int = 8) -> str:
    if length < 4:
        raise ValueError("Token length must be at least 4")

    return "".join(secrets.choice(TOKEN_ALPHABET) for _ in range(length))
