import asyncio

class ATimer:
    """
    Scheduling periodic callbacks using handler
    call_later(timeout, callback) ensure that jobs don't get cancelled after timer stop()
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
        self._handler = self._loop.call_later(self._timeout, self._run)



    def start(self):
        self._handler = self._loop.call_later(self._timeout, self._run)

    def stop(self):
        self._handler.cancel()

    def reset(self):
        self.stop()
        self.start()

#################################### run ############################


async def coloop():
    # simulates main loop
    i = 1
    while True:
        await asyncio.sleep(1)
        print(f'main loop: {i}')
        i += 1


def callback():
    print('so long and thanks for all the fish')


async def main():
    timer = ATimer(3,callback)
    timer.start()
    await coloop()


asyncio.run(main())






