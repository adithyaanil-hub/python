# thread
# it is a worker inside a process

# import threading


# def work(name):
#     print(f"{name} am working")


# t1 = threading.Thread(target=work, args=["mohan"])
# t2 = threading.Thread(target=work, args=["das"])

# t1.start()
# t2.start()
# t1.join()
# t2.join()


# import threading
# import time
# lock = threading.Lock()
# x = 0


# def work(name):
#     global x
#     for i in range(1, 4):
#         with lock:
#             x = x+i
#             print(name, x)
#             time.sleep(1)


# t1 = threading.Thread(target=work, args=["A"])
# t2 = threading.Thread(target=work, args=["b"])

# t1.start()
# t2.start()
# t1.join()
# t2.join()

# print("main", x)
