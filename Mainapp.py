import threading
import time
from Server import *
from ThreadManager import *
from Database import *

is_running = False
UPDATE_PERIOD = 1000 / 30

def main():
    print("Server Console")
    global is_running
    is_running = True
    # _thread = threading.Thread(target=main_thread)
    # _thread.start()
    StartServer()
    # ExecuteOnMainThread(main_thread)

# def main_thread():
#     next_loop = time.time()
#     while is_running:
#         while next_loop < time.time():
#             UpdateMain()
#             print("Here")
#             next_loop += UPDATE_PERIOD / 1000
#             if next_loop > time.time():
#                 time.sleep(next_loop - time.time())

if __name__ == "__main__":
    main()
