import asyncio
import random
from threading import Thread

from api_layer import GetMethod, PostMethod
from backup_data import BackupDataManager
from db import ReactionsTable
from redis_adapter import RedisAdapter
from config import EMOTICON_TYPES, MAX_MATCHES, MAX_USER_NO


# initialising redis and DB table instance for the system once
# (Singleton design pattern)
redis_adapter = RedisAdapter()
redis_instance = redis_adapter.get_instance()
reactions_table = ReactionsTable()

get_method = GetMethod(redis_instance)
post_method = PostMethod(redis_instance)


# running the POST call in a different thread
def post_method_calls():
    while True:
        user_id = random.randint(1, MAX_USER_NO)
        match_id = random.randint(1, MAX_MATCHES)
        emoticon_type = random.choice(EMOTICON_TYPES)
        _ = post_method.post(user_id, match_id, emoticon_type)


get_thread = Thread(
    target=post_method_calls,
    args=[]
)
get_thread.start()


# running the get method call aync every 5 seconds
async def get_method_periodic():
    print('-------------------')
    print('Printing the get value...')
    match_id = random.randint(1, MAX_MATCHES)
    value = get_method.get(match_id)
    print(f'match_id - {str(match_id)}, emoticon_map - {value}')
    print('-------------------')
    await asyncio.sleep(5)


# running the data backup from redis to DB every 10 seconds
async def data_backup_periodic():
    print('-------------------')
    backup_data_manager = BackupDataManager(
        redis_instance, reactions_table)
    backup_data_manager.run()
    print('-------------------')
    await asyncio.sleep(10)


# running the get method and data backup functions together in async
async def run_two_func():
    while True:
        f1 = loop.create_task(get_method_periodic())
        f2 = loop.create_task(data_backup_periodic())
        await asyncio.wait([f1, f2])

loop = asyncio.get_event_loop()
loop.run_until_complete(run_two_func())
loop.close()
