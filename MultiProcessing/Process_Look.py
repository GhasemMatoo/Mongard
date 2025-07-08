from multiprocessing import Process, Lock


def p1_func(number, lock):
    with lock:
        for _ in range(1000):
            number += 1



def p2_func(number, lock):
    lock.acquire()
    for _ in range(1000):
        number -= 1
    lock.release()

number = 0
lock = Lock()

p1 = Process(target=p1_func, args=(number, lock))
p2 = Process(target=p2_func, args=(number, lock))

p1.start()
p2.start()

p1.join()
p2.join()

print(number)
