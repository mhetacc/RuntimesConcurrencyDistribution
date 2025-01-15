# create_tasks is the high level counterpart of ensure_future and tasks are, in fact, futures
# they can be directly awaited or be gathered to be executed concurrently 

import asyncio

async def coroutine(var):
    print(var)


async def main():
    print('fire with only gather')
    tasks = asyncio.gather(coroutine(1), coroutine(2))

    await tasks


    print('fire with tasks')
    task1 = asyncio.create_task(coroutine(3))
    task2 = asyncio.create_task(coroutine(4))
    tasks = asyncio.gather(task1,task2)

    await tasks


asyncio.run(main())
