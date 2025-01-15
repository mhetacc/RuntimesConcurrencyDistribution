import asyncio

class Timer:
    """
    Scheduling periodic callbacks using handler
    Using call_later ensure that jobs dont get cancelled after timer stop()
    """
    def __init__(self, timeout, callback, args=None, kwargs=None):
        self._timeout = timeout
        self._callback = callback
        self._args = args if args is not None else []
        self._kwargs = kwargs if kwargs is not None else {}
        self._loop = asyncio.get_event_loop()
        self._handler = None


    def _run(self):
        """Fire callback then restarts timer"""
        self._callback(*self._args, **self._kwargs)

        # call_later(timeout, callback)
        # calls callback after timeout runs out
        self._handler = self._loop.call_later(self._timeout, self._run)



    def start(self):
        self._handler = self._loop.call_later(self._timeout, self._run)

    def stop(self):
        self._handler.cancel()

    def reset(self):
        self.stop()
        self.start()



async def coloop():
    # simulates main loop
    i = 1
    while True:
        await asyncio.sleep(1)
        print(f'main loop: {i}')
        i += 1


def callback():
    #callback is not async since xmlrpc rpcs are synchronous
    print('so long and thanks for all the fish')


# async def timerstart():
#     # can be skipped
#     timer = Timer(3,callback)
#     timer.start()


async def main():
    timer = Timer(3,callback)
    timer.start()
    await coloop()

    #tasks = asyncio.gather(timerstart(), coloop())
    #await tasks

asyncio.run(main())






