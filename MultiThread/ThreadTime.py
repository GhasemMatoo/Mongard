from threading import Timer


def show():
    print('hello')


t = Timer(10, show)
t.start()
