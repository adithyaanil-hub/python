# file handling

# file1 = open("hello.txt", "r")
# print(file1.read())
# file1.close()

# file2=open("bye.txt","w")
# file2.write("i am adithya.........")
# file2.close()

# file3 = open("demo.txt", "a")
# for i in range(1, 100):
#     file3.write(f"i am legendary!!!!!!!times{i}!!!!!!!\n")
# file3.close()


# with open("hello.txt","r")as f:
#     print(f.read())


import os
# os.mkdir("django")
# os.rename("bye.txt","byyyyye.txt")
# file_path = "C:\\Users\\LENOVO\\OneDrive\\Desktop\\monkey.txt"
# os.remove(file_path)
# if os.path.exists(file_path):
#     if os.path.isdir(file_path):
#         print("folder")
#     elif os.path.isfile(file_path):
#         print("its a file")


# exception handling
# Exceptions-events that affects the execution of the program

# try:
#     a = int(input("enter a number:"))
#     b = int(input("enter a number:"))
#     print(a/b)
# except:
#     print("an errror occured!!!!!")
# print("mohan")


# try:
#     a = int(input("enter a number:"))
#     b = int(input("enter a number:"))
#     print(a/b)
# except Exception as e:
#     print("an errror occured!!!!!", e)
# print("mohan")

# try:
#     a = int(input("enter number:"))
#     b = "6"
#     print(a/b)
# except ZeroDivisionError:
#     print("you cant divide a number by zero")
# except ValueError:
#     print("check your values")
# except TypeError:
#     print("check your type!!!")
# finally:
#     print("this will always execute")


# raise

# class Age_error(Exception):
#     pass
# age = 14
# if age < 18:
#     raise Age_error("age should greater than 18")


