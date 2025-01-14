import asyncio
import time

class Timer:
    """Scheduling periodic callbacks using handler"""
    def __init__(self, timeout, callback, args=None, kwargs=None):
        self._timeout = timeout
        self._callback = callback
        self._args = args if args is not None else []
        self._kwargs = kwargs if kwargs is not None else {}
        self._loop = asyncio.get_event_loop()
        # self._handler gets created on start() only


    def _get_timeout(self):
        return self._timeout() if callable(self._timeout) else self._timeout

    def _run(self):
        """Fire callback then restarts timer"""
        self._callback(*self._args, **self._kwargs)
        self._handler = self._loop.call_later(self._get_timeout(), self._run)



    def start(self):
        self._handler = self._loop.call_later(self._get_timeout(), self._run)

    def stop(self):
        self._handler.cancel()

    def reset(self):
        self.stop()
        self.start()


def callback():
    print('so long and thanks for all the fish')

async def main():
    timer = Timer(3,callback)
    timer.start()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


loop.run_until_complete(main())

i=0
while True:
    time.sleep(1)
    print(f'Iteration: {i}')
    i+=1

