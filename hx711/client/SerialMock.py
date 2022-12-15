import random

class SerialMock:
    def __init__(self):
        self.is_open = True
    def readline(self):        
        return str(random.randint(-1000, 100000)).encode()
