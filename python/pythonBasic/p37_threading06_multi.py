import threading

def example():
    for _ in range(1, 10):
        print(_)

threading.Thread(target=example).start()
threading.Thread(target=example).start()