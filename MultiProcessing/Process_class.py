import time
from multiprocessing import Process

start = time.perf_counter()


def show(name, delay):
    print(f'Started {name}')
    time.sleep(delay)
    print(f'Ending {name}')

class ShowProcess(Process):
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay

    def run(self) -> None:
        show(self.name, self.delay)


p1 = ShowProcess(name="One", delay=3)
p2 = ShowProcess(name="Two", delay=7)

p1.start()
p2.start()

p1.join()
p2.join()

end = time.perf_counter()

print(round(end - start))
