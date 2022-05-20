import pickle
import time


def load_history() -> dict:
    """
    从数据文件加载历史聊天记录
    :return: 聊天记录，dict类型
    """
    try:
        return pickle.load(open('history.dat', 'rb'))
    except FileNotFoundError:
        return {}


def __get_key(history: dict, u1, u2):
    """
    聊天记录是双向的，所以在存储时(u1, u2)与(u2, u1)等价，从u1或u2任意一方都能获取所有记录
    :param history: history: 聊天记录，外部调用load_history获得
    :param u1:
    :param u2:
    :return:
    """
    return (u1, u2) if (u2, u1) not in history.keys() else (u2, u1)


def append_history(history: dict, sender, receiver, msg: str):
    """
    保存一条聊天记录
    :param history: 聊天记录，外部调用load_history获得
    :param sender: 发送方
    :param receiver: 接收方
    :param msg: 信息
    :return:
    """
    if receiver == '':  # 没有接收方，即聊天室聊天
        key = ('', '')
    else:
        key = __get_key(history, sender, receiver)
    if key not in history.keys():
        history[key] = []  # 创建一条记录
    history[key].append((sender, time.strftime('%Y/%m/%d %H:%M', time.localtime(time.time())), msg))  # 追加一个新记录
    save_history(history)


def get_history(history: dict, sender, receiver) -> list:
    """
    获取一条聊天记录
    :param history: 聊天记录，外部调用load_history获得
    :param sender: 发送方
    :param receiver: 接收方
    :return: 所有的记录数组
    """
    if receiver == '':
        key = ('', '')
    else:
        key = __get_key(history, sender, receiver)
    return history[key] if key in history.keys() else []


def save_history(history: dict):
    """
    持久化数据
    :return:
    """
    pickle.dump(history, open('history.dat', 'wb'))
