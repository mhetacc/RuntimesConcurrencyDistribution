from threading import Timer

class LoopTimer(Timer):
    """Subclass of threading.Timer: starts a timer that loops in a separate thread, can call a callback function each time it runs out"""

    def run(self):
        # makes 'if' of Timer.run() a 'while'
        # returns False each time times out
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)