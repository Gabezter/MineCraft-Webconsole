import random
import string
import hashlib
import re

from flask import current_app


def generate_temp_password():
    length = random.randint(6, 8)
    letters = string.ascii_letters
    pwd = ''.join(random.choice(letters) for i in range(length))
    return pwd


def hashify(pwd):
    return hashlib.blake2b(pwd.encode('utf8'), salt=current_app.config['PASSWORD_SALT'].encode('utf8')).hexdigest()


def get_password_type():
    type = str(current_app.config['PASSWORD_STRENGTH']).lower
    if type == 'loose':
        loose = True
        strict = False
        tight = False
    elif type == 'tight':
        loose = False
        strict = False
        tight = True
    elif type == 'strict':
        loose = False
        strict = True
        tight = False
    else:
        loose = False
        strict = True
        tight = False
    return (loose, tight, strict)


def check_password_strength(password):
    password_type = get_password_type()
    if password_type[0]:
        length_error = len(password) > 6
    else:
        length_error = len(password) > 8

    if password_type[1] or password_type[2]:
        digit_error = re.search(r"\d", password) is not None
    else:
        digit_error = True

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is not None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is not None

    # searching for symbols
    if password_type[2]:
        symbol_error = re.search(
            r"[ ?!#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is not None
    else:
        symbol_error = True

    return length_error and digit_error and uppercase_error and lowercase_error and symbol_error
