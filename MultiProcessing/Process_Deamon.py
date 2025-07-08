import time
import sys
from multiprocessing import Process, current_process

start = time.perf_counter()


def show(name):
    print(f'Started {name}')
    print(current_process())
    time.sleep(3)
    print(f'Ending {name}')


p1 = Process(target=show, args=("One",), daemon=True)
p2 = Process(target=show, args=("Two",), daemon=True)

p1.start()
p2.start()


end = time.perf_counter()

print(round(end - start))
sys.exit()