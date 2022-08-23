import settings


def generate_password(password_string):
    # TODO: implement stronger password hashing
    return f'{password_string}{settings.SECRET_KEY}'


def check_password(password_string, hashed_password):
    # TODO: implement stronger password hashing
    if generate_password(password_string) == hashed_password:
        return True
    return False
