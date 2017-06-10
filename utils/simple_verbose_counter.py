import time


class SimpleVerboseCounter(object):
    "Simple counter that prints a message periodically."

    def __init__(self, period, message):
        self.counter = 0
        self.period = period
        self.message = message
        self.period_start_time = time.time()

    def __call__(self):
        "Increases internal counter and prints message and returns True if a full period has passed, False otherwise."
        self.counter += 1
        if self.counter % self.period == 0:
            current_time = time.time()
            elapsed = current_time - self.period_start_time
            self.period_start_time = current_time
            print(self.message.format(self.counter, elapsed))
            return True
        return False

    def __lt__(self, other):
        return self.counter < other

    def ___le__(self, other):
        return self.counter <= other

    def __eq__(self, other):
        return self.counter == other

    def __ne__(self, other):
        return self.counter != other

    def __gt__(self, other):
        return self.counter > other

    def __ge__(self, other):
        return self.counter >= other
