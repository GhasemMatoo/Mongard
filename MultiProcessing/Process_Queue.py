from multiprocessing import Process, Queue

numbers = []
def p1_func(queue):
    nums = queue.get()
    nums.extend([1,2,3])
    queue.put(nums)
    print(nums)

def p2_func(queue):
    nums = queue.get()
    nums.extend([4, 5, 6])
    queue.put(nums)
    print(nums)

qs = Queue()
qs.put(numbers)

p1_process = Process(target=p1_func, args=(qs,))
p2_process = Process(target=p2_func, args=(qs,))

p1_process.start()
p2_process.start()

p1_process.join()
p2_process.join()

print(qs.get())
