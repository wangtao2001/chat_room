import pickle


def load_users() -> dict:
    """
    从数据文件中加载用户信息
    :return: 用户信息，dict类型
    """
    try:
        return pickle.load(open('users.dat', 'rb'))
    except FileNotFoundError:
        return {}


def register(users: dict, usr: str, pwd: str) -> bool:
    """
    注册用户， 返回注册成功/失败状态
    :param users: 用户信息，外部调用load_users函数的来
    :param usr: 用户名
    :param pwd: 密码
    :return: 注册成功为True，否则为False
    """
    if usr not in users.keys():
        users[usr] = pwd
        save_users(users)
        return True
    else:
        return False


def validate(users: dict, usr: str, pwd: str) -> bool:
    """
    用户密码验证
    :param users: 用户信息，外部调用load_users函数的来
    :param usr: 用户名
    :param pwd: 密码
    :return: 密码正确为True，否则为False
    """
    if usr in users.keys() and users[usr] == pwd:
        return True
    return False


def save_users(users: dict):
    """
    持久化数据
    :return:
    """
    pickle.dump(users, open('users.dat', 'wb'))
