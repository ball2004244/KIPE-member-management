import hashlib

def hash_password(password):
    # sha256_hash = hashlib.sha256()
    # encoded_password = sha256_hash.update(password.encode('utf-8'))
    encoded_password = password.encode('utf-8')
    hashed_password = hashlib.sha256(encoded_password).hexdigest()
    return hashed_password
