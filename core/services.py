import secrets
import string


def make_random_password():
    character = string.ascii_letters + string.digits
    password = "".join(secrets.choice(character) for _ in range(15))
    return password
