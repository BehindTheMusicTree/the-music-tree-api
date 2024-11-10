import random
import string


def print_django(message):
    print(f"[Django] {message}")


def generate_short_uu(length: int):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def get_substring_after_last_slash(string: str):
    return string.split("/")[-1]


def get_file_extension_from_url(url: str):
    return url.split(".")[-1]
