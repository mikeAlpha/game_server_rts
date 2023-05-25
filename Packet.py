BYTE_COUNT = 4
def send_msg(sock, msg):
    msg = add_msg_header(msg)
    sock.sendall(msg)
def recv_msg(sock):
    raw_msglen = recvall(sock, BYTE_COUNT)
    if not raw_msglen:
        return None
    msglen = len_frombytes(raw_msglen)
    return recvall(sock, msglen)
def recvall(sock, length):
    data = bytearray()
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data
def add_msg_header(msg):
    return len_inbytes(msg) + msg
def len_inbytes(msg):
    return len(msg).to_bytes(BYTE_COUNT, byteorder='big')
def len_frombytes(bmsg):
    return int.from_bytes(bmsg, byteorder='big')