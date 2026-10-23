import time
# print(time.time())
# print(time.ctime(1791885416.4559026))  #epoch time

# start=time.time()
# for i in range(1,6):
#     print(i)
#     time.sleep(1)
# end=time.time()

# print("total time:",end-start)


# def total_time(fun):
#     def wrapper(*args, **kwargs):
#         start = time.time()
#         fun(*args, **kwargs)
#         end = time.time()
#         print("total", end-start)
#     return wrapper


# @total_time
# def greet(name):
#     print(f"hello {name}")


# greet("adithya")


# @total_time
# def addz(a, b):
#     print(a+b)


# addz(4, 5)


# @total_time
# def ntimes(n):
#     for i in range(1, n+1):
#         print(i)
#         time.sleep(1)


# ntimes(3)
