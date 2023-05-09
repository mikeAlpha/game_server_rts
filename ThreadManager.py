import threading

lock = threading.Lock()

executeOnMainThread = []
executeCopiedOnMainThread = []
actionToExecuteOnMainThread = False

@staticmethod
def ExecuteOnMainThread(_action):
        
   global executeOnMainThread
   global actionToExecuteOnMainThread
   global executeCopiedOnMainThread

   if _action is None:
      print("No action to execute on main thread!")
      return
   lock.acquire()
   executeOnMainThread.append(_action)
   actionToExecuteOnMainThread = True
   lock.release()

@staticmethod
def UpdateMain():

   global executeOnMainThread
   global actionToExecuteOnMainThread
   global executeCopiedOnMainThread
   
   if actionToExecuteOnMainThread is True:
      executeCopiedOnMainThread.clear()
      lock.acquire()
      executeCopiedOnMainThread.extend(executeOnMainThread)
      executeOnMainThread.clear()
      actionToExecuteOnMainThread = False
      lock.release()
      for i in range(len(executeCopiedOnMainThread)):
         executeCopiedOnMainThread[i]()