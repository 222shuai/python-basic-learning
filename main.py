import threading

def f1():
    print(1)

def f2():
    print(2)

t1 = threading.Thread(target=f1)
t2 = threading.Thread(target=f2)
t1.start()
t2.start()
