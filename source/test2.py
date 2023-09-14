import threading

def my_func1():
    print('Inside func 1')

def my_func2():
    print('Inside func 2')


t1 = threading.Thread(target=my_func1, daemon=True)


t2 = threading.Thread(target=my_func2, daemon=True)
t2.start()