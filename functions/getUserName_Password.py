import getpass
import os

cache_file_name = '.info'


def get(is_input=True):
    if is_input:
        user_name = input("UserName:__________\b\b\b\b\b\b\b\b\b\b")
        password = getpass.getpass('Password:')
    else:
        try:
            user_name, password = open(cache_file_name).read().split('\n')
        except FileNotFoundError:
            return prepare()
    return user_name, password


def prepare():
    userName, password = get(is_input=True)
    with open(cache_file_name, 'w') as f:
        f.write(userName + '\n' + password)
        return userName, password


def remove_cache():
    try:
        os.remove(cache_file_name)
    except FileNotFoundError:
        pass

