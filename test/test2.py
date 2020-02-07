import threading

t = threading.currentThread()

print(t.getName() == "MainThread")

def demo():
    print("I am Thread")
    t = threading.currentThread()
    print(t.getName())

new_t = threading.Thread(target=demo, name="嗯哼")
new_t.start()

