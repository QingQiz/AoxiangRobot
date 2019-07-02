import getpass


def get(is_input=True):
    if is_input:
        user_name = input("UserName:__________\b\b\b\b\b\b\b\b\b\b")
        password = getpass.getpass('Password:')
    else:
        try:
            user_name, password = open('.info').read().split('\n')
        except FileNotFoundError:
            return prepare()
    return user_name, password


def prepare():
    userName, password = get(is_input=True)
    with open('.info', 'w') as f:
        f.write(userName + '\n' + password)
        return userName, password
