from Crypto.Cipher import AES
from Crypto import Random
import struct
import json

key = b'fdj27pFJ992FkHQb'
max_buff_size = 1024


def __encrypt(data: bytes) -> bytes:
    """
    数据加密
    :param data: 待加密数据
    :return: 加密后的数据
    """
    code = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, code)
    return code + cipher.encrypt(data)


def __decrypt(data: bytes) -> bytes:
    """
    数据解密
    :param data: 待解密数据
    :return: 解密后的数据
    """
    return AES.new(key, AES.MODE_CFB, data[:16]).decrypt(data[16:])


def __pack(data: bytes) -> bytes:
    """
    在数据首都加上一个二字节的整数表示此次数据的大小
    :param data: 待发送的数据
    :return: 格式化后的数据
    """
    return struct.pack('>H', len(data)) + data


def recv(socket) -> dict:
    """
    接受传输的的数据并解密
    :param socket: socket对象
    :return: 接受的数据
    """
    data = b''
    r = socket.recv(2)
    surplus = struct.unpack('>H', r)[0]  # 解析出此次数据的大小
    socket.settimeout(5)

    while surplus:  # 表示此次有数据传输
        recv_data = socket.recv(max_buff_size if surplus > max_buff_size else surplus)
        data += recv_data
        surplus -= len(recv_data)
    socket.settimeout(None)
    return json.loads(__decrypt(data))


def send(socket, data_dict: dict):
    """
    将数据序列化为json对象并加密后传输
    :param socket: socket对象
    :param data_dict: 待传输数据
    :return:
    """
    socket.send(__pack(__encrypt(json.dumps(data_dict).encode('utf-8'))))
