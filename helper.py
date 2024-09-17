from hashlib import sha256


def hash(msg):
    m=sha256()
    m.update(msg.encode())
    return m.hexdigest()

