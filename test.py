"""
 Hello 

"""
import threading
import time


def p():
    print(str(time.time()) + "aaa")
    timer = threading.Timer(3, p, [])
    timer.start()


if __name__ == "__main__":
    p()
