# import asyncio


# class Timer:
#     def __init__(self, timeout, callback):
#         self._timeout = timeout
#         self._callback = callback
#         self._task = asyncio.ensure_future(self._job())

#     async def _job(self):
#         await asyncio.sleep(self._timeout)
#         await self._callback()

#     def cancel(self):
#         self._task.cancel()


# async def timeout_callback():
#     await asyncio.sleep(0.1)
#     print('echo!')


# async def main():
#     print('\nfirst example:')
#     timer = Timer(2, timeout_callback)  # set timer for two seconds
#     await asyncio.sleep(2.5)  # wait to see timer works

#     print('\nsecond example:')
#     timer = Timer(2, timeout_callback)  # set timer for two seconds
#     await asyncio.sleep(1)
#     timer.cancel()  # cancel it
#     await asyncio.sleep(1.5)  # and wait to see it won't call callback


# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# try:
#     loop.run_until_complete(main())
# finally:
#     loop.run_until_complete(loop.shutdown_asyncgens())
#     loop.close()

import asyncio
from datetime import datetime, timedelta
# from pymongo import MongoClient
time = datetime.utcnow() + timedelta(seconds=60)
print(time)

# # set up the MongoDB client
# # client = MongoClient('mongodb://localhost:27017/')
# # db = client['mydatabase']
# # collection = db['mycollection']

# async def update_document():
#     # wait for 5 seconds
#     await asyncio.sleep(0.1)

#     # update the document
#     # query = {'_id': 12345}  # replace with your query
#     # update = {'$set': {'status': 'done'}}  # replace with your update
#     # result = collection.update_one(query, update)
#     print(f"Document updated")

# async def main():
#     # set up the timer
#     timer = datetime.now() + timedelta(seconds=5)

#     # start the timer
#     count = 0
#     while datetime.now() < timer:
#         count += 1
#         print(count)
#         await asyncio.sleep(1)

#     # timer has expired, update the document
#     await update_document()

# # run the main function
# asyncio.run(main())