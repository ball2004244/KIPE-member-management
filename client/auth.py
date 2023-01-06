import hashlib
from api import database
from typing import Tuple


def hash_password(password):
    # sha256_hash = hashlib.sha256()
    # encoded_password = sha256_hash.update(password.encode('utf-8'))
    password_hash = hashlib.sha256(password).hexdigest()
    return password_hash


def compare_hashes(password_hash1, password_hash2):
    return password_hash1 == password_hash2


def login(email: str, password: str) -> Tuple[bool, dict]:
    if not (len(email) and len(password)):
        print('You must fill in both fields')
        return False, None

    # check if account already in database
    all_user_data = database.get_all_user()
    if all_user_data:
        for user in all_user_data:
            if email == user['email']:
                # check if password matched
                if compare_hashes(hash_password(password.encode('utf-8')), user['password']):
                    user_data = {'id': user['id'], 'email': user['email'],
                                 'first_name': user['first_name'], 'last_name': user['last_name']}
                    return True, user_data
    return False, None


if __name__ == '__main__':
    password1 = b'password'
    password2 = b'password'

    password_hash1 = hash_password(password1)
    password_hash2 = hash_password(password2)

    if compare_hashes(password_hash1, password_hash2):
        print('The passwords match')
    else:
        print('The passwords do not match')
