import hashlib
import random
import string

def generate_temp_password():
    length = random.randint(6,8)
    letters = string.ascii_letters
    pwd = ''.join(random.choice(letters) for i in range(length))
    return pwd
