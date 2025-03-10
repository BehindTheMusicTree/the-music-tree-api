import argparse
import secrets

import django
from django.conf import settings
from django.contrib.auth.hashers import PBKDF2PasswordHasher


settings.configure(
    PASSWORD_HASHERS=[
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    ]
)

django.setup()


def hash_password(raw_password, algorithm, iterations, salt):
    hasher = PBKDF2PasswordHasher()
    new_hash = hasher.encode(raw_password, salt, int(iterations))
    return new_hash


def generate_random_salt(length=16):
    return secrets.token_urlsafe(length)


def hash_password_with_random_salt(raw_password):
    algorithm = 'pbkdf2_sha256'
    iterations = '720000'
    salt = generate_random_salt()
    hashed_password = hash_password(raw_password, algorithm, iterations, salt)
    return hashed_password, salt


def main():
    parser = argparse.ArgumentParser(description='Hash a password with a random salt.')
    parser.add_argument('password', type=str, help='The password to hash')
    args = parser.parse_args()
    hashed_password, salt = hash_password_with_random_salt(args.password)
    print(f"Hashed Password: {hashed_password}")
    print(f"Salt used: {salt}")


if __name__ == "__main__":
    main()
