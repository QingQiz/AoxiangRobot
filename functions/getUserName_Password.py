import getpass


def get(default=True):
    if not default:
        user_name = input("UserName:__________\b\b\b\b\b\b\b\b\b\b")
        password = getpass.getpass('Password:')
    else:
        user_name = '2017302344'
        password = open('.password').read().strip('\n')
    return user_name, password
