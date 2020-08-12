import random
import string
import hashlib

from flask import current_app

def generate_temp_password():
    length = random.randint(6,8)
    letters = string.ascii_letters
    pwd = ''.join(random.choice(letters) for i in range(length))
    return pwd

def hashify(pwd):
    return hashlib.blake2b(pwd.encode('utf8'), salt=current_app.config['PASSWORD_SALT'].encode('utf8')).hexdigest()