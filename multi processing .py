# Process
# it is an independent running program

# from multiprocessing import Process
# import os
# x = 0


# def work(name):
#     global x
#     print(name, "working")
#     print(os.getpid())
#     for i in range(1, 4):
#         x = x+i
#     print(name, x)


# p1 = Process(target=work, args=["A"])
# p2 = Process(target=work, args=["B"])

# if __name__ == '__main__':

#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
#     print("main", x)
#     print(os.getpid())
