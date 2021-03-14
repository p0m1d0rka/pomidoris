import socket
import re

HOST = '127.0.0.1'
PORT = 65432
global_data = {}


def set_data(key:str, value:str) -> bool:
    global_data[key] = value
    return True


def get_data(key:str) -> bytes:
    if key in global_data:
        return global_data[key].encode()
    else:
        return f"Key not found {key}".encode()


def split_input_data(data: bytes) -> tuple:
    """
    Split raw socket input into tuple.
    ex:
        b'get key' -> ('get', key', '')
        b'set key some value' -> ('set', 'key', 'some value')
        b'blalbalba' -> ('error', "error text', '')
    :param data:
    :return: (action:str, key:str, [value:str])
    """
    data_decoded = data.decode()
    m = re.match(r"(\w+)\s(\w+)\s*(.*)", data_decoded)
    if m is None:
        return "error", "value", "Error while split data_decoded"
    else:
        return m.group(1, 2, 3)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listen {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            action, key, value = split_input_data(data)
            if action == "get":
                conn.sendall(get_data(key))
            elif action == "set":
                if set_data(key, value):
                    conn.sendall(b"OK")
                else:
                    conn.sendall(b"Error while setting data")
            elif action == "error":
                conn.sendall(value.encode())
            else:
                conn.sendall(b"Unhandled error")



