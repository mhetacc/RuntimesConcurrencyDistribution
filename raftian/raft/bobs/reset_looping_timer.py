from threading import Timer

class LoopTimer(Timer):
    """Subclass of threading.Timer: starts a timer that loops in a separate thread, call a callback each time it runs out"""

    def __init__(self, interval, function, args=None, kwawrgs=None):
        Timer.__init__(self, interval, function, args, kwawrgs)
        self.was_reset : bool = False

    def run(self):
        # makes 'if' of Timer.run() a 'while'
        # returns False each time it runs out
        while not self.finished.wait(self.interval):
            if not self.was_reset:
                self.function(*self.args, **self.kwargs)
            self.was_reset = False

    def reset(self, interval=None):
        # reset flag based since stopping an re starting timers is illegal
        self.was_reset = True

        if interval is not None:
            self.interval = interval

