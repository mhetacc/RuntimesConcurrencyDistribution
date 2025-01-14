import asyncio

async def coloop():
    while True:
        await asyncio.sleep(1)
        print('coloop')


async def coprint():
    await asyncio.sleep(3)
    print('coprint')


async def main():
    await asyncio.gather(coloop(), coprint())


asyncio.run(main())  