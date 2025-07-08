import time
from multiprocessing import Process
from concurrent.futures import ProcessPoolExecutor

start = time.perf_counter()

def show(name):
    print(f'Started {name}')
    time.sleep(3)
    print(f'Ending {name}')

def main():
    with ProcessPoolExecutor(max_workers=2) as executor:
        names = ["one", "two", "three", 'four', 'five', 'six', 'seven']
        executor.map(show, names)

main()

end = time.perf_counter()
