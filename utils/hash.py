import hashlib

def hash_password(password):
    hash_password = hashlib.sha256(password.encode()).hexdigest()
    return hash_password