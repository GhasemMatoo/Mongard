import time
import os
from multiprocessing import Process, current_process

start = time.perf_counter()

def show(name):
    print(f'Started {name}')
    print(current_process())
    print(f'OS pid ==> {os.getpid()}')
    print(f'OS ppid ==> {os.getppid()}')
    time.sleep(3)
    print(f'Ending {name}')


p1 = Process(target=show, args=("One",))
p2 = Process(target=show, args=("Two",))

p1.start()
p2.start()

print(p1.is_alive())
print(p2.is_alive())
p1.terminate()
p2.kill()

p1.join()
p2.join()

print(f'Process is_alive ==>{p1.is_alive()} is exitcode ===>{p1.exitcode}')
print(f'Process is_alive ==>{p2.is_alive()} is exitcode ===>{p2.exitcode}')

end = time.perf_counter()

print(round(end-start))