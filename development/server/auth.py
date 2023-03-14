import hashlib
def verify_login(password: str, hashed_password: str):
    try:
        if compare_hashes(password, hashed_password):
            return True
    except:
        print('Some error occur')
    return False

def compare_hashes(password_hash1, password_hash2):
    return password_hash1 == password_hash2

def hash_password(password):
    # sha256_hash = hashlib.sha256()
    # encoded_password = sha256_hash.update(password.encode('utf-8'))
    encoded_password = password.encode('utf-8')
    hashed_password = hashlib.sha256(encoded_password).hexdigest()
    return hashed_password

if __name__ == '__main__':
    print(hash_password('testmember'))