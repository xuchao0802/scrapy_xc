#task
import time
import asyncio

async def do_some_work(x):
    print("waiting:",x)
    await asyncio.sleep(1)
    #return "Done after {}s".format(x)

def callback(future):
    print("callback:",future.result())


coroutine = do_some_work(2)

loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coroutine)#future对象

task.add_done_callback(callback)#对future对象添加callback函数

loop.run_until_complete(task)

