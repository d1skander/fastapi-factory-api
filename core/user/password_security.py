import bcrypt


def password_hash(password: str) -> bytes:
    try:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed
    except TypeError as e:
        raise e


def password_check(password: str, hashed: str) -> bool:
    try:
        if bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8")):
            return True
        else:
            return False
    except TypeError as e:
        raise e