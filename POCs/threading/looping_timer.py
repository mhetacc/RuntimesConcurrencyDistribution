from threading import Timer

class LoopTimer(Timer):

    def run(self):
        # makes 'if' of Timer.run() a 'while'
        # returns False each time times out
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)