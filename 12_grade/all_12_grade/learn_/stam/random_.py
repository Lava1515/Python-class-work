import random
import string


def generate_random_string(length=50):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choices(characters, k=length))
    return random_string


random_string = generate_random_string()
print(random_string)
