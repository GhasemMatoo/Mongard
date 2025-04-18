from concurrent.futures import ThreadPoolExecutor
from time import sleep


def show(name):
    print(f'Starting {name} ....')
    sleep(3)
    print(f'Finishing {name} .....')


with ThreadPoolExecutor(max_workers=2) as executor:
    names = ['One', 'Two', 'Three', 'Four', 'Five', 'six', 'seven']
    executor.map(show, names)

print('Done ...')
