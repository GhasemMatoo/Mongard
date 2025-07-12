from multiprocessing import Pool, cpu_count
import time

start = time.perf_counter()

def show(name):
    print(f'Starting {name}')
    time.sleep(3)
    print(f'Ending  {name}')

names = ['one', 'two', 'three', 'four', 'five']
pool = Pool(processes=cpu_count())
pool.map(show, names)
pool.close()
pool.join()

end = time.perf_counter()
print(round(end - start))