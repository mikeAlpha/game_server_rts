import socket
import struct
from _thread import *
import threading
from Database import *
from enum import Enum
from Packet import *
import asyncio
import keyboard

class RequestID(Enum):
    SYNC = 1
    BUILD = 2
    UPGRADE = 3
    UPGRADE_COMP = 4
    UPDATE_BUILD_POS = 5
    ADD_BUILDING = 6
    ADD_BUILDING_COMP = 7

 #threading (Note: use Threadmanager for that)
_lock = threading.Lock()

#Server details
host = "127.0.0.1"
port = 56632
sckt = None

def check_data(id,data,c):
    if id == int(RequestID.SYNC.value):
        val = str(id)+'_'+syncplayerdata(data[4:].decode())
        send_dat = bytes(val,'utf-8')
        buffer = bytearray()
        buffer.extend(send_dat)
        print(len(buffer))
        c.send(buffer)
    
    # if id == int(RequestID.SYNC.value):
    #     send_dat = bytes(syncplayerdata(data[4:].decode()),'utf-8')
    #     c.send(send_dat)
    
    elif id == int(RequestID.BUILD.value):
        print("Building")

    elif id == int(RequestID.UPGRADE.value):
        print("Upgrading")
        print(len(data))
        buildingType = struct.unpack('<i',data[4:8])[0]
        childIndex = struct.unpack('<i',data[8:12])[0]
        user_id = data[12:].decode()
        asyncio.run(upgrade_building(user_id,buildingType,childIndex,c))
    
    elif id == int(RequestID.UPGRADE_COMP.value):
        print("Update build details")
        print(len(data))
        buildingType = struct.unpack('<i',data[4:8])[0]
        childIndex = struct.unpack('<i',data[8:12])[0]
        user_id = data[12:].decode()
        asyncio.run(update_building_details(user_id,buildingType,childIndex,c))
    
    elif id == int(RequestID.UPDATE_BUILD_POS.value):
        print("Update build Position")
        print(len(data))
        buildingType = struct.unpack('<i',data[4:8])[0]
        childIndex = struct.unpack('<i',data[8:12])[0]
        x = struct.unpack('<i',data[12:16])[0]
        y = struct.unpack('<i',data[16:20])[0]
        z = struct.unpack('<i',data[20:24])[0]
        user_id = data[24:].decode()
        asyncio.run(update_build_position(user_id,buildingType,childIndex,x,y,z,c))
    
 
 
def StartServer():
    global sckt
    global host,port

    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sckt.bind((host, port))
    print("socket binded to port", port)

    sckt.listen(5)
    print("socket is listening")

    while True:
        c, addr = sckt.accept()

        _lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        while True:
            data = c.recv(1024)
            if not data:
                print('Bye')
                _lock.release()
                c.close()
                break
            id = struct.unpack('<i',data[:4])[0]
            check_data(id,data,c)
    sckt.close()

        # if keyboard.is_pressed("c"):
        #     print("Closing server....")
        #     _lock.release()
        #     sckt.close()
        #     c.close()
        #     break

    # while True:

        # c, addr = sckt.accept()

        # print_lock.acquire()
        # print('Connected to :', addr[0], ':', addr[1])

        # start_new_thread(threaded, (c,))
    # s.close()
 
 
# if __name__ == '__main__':
#     Main()