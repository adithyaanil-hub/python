# area of a triangle

# base=int(input("enter base:"))
# height=int(input("enter height:"))
# if base > 0 and height > 0:
#     area=0.5* base* height
#     print("Area of triangle:",area)
# else:
#     print("invalid input")

# perimeter of a circle

# radius =int(input("Enter radius:"))
# if radius > 0:
#     perimeter = 2 * 3.14 *radius
#     print("Perimeter of circle:",perimeter)
# else:
#     print("Invalid radius")

# square of a number

# a = int(input("Enter number: "))
# if a >= 0:
#     print("Square:", a * a)
# else:
#     print("Number is negative")

# converts dollar to inr

# dollar = float(input("Enter dollar: "))
# if dollar > 0:
#     print("INR:", dollar * 88)
# else:
#     print("Invalid amount")

#  miles to km

# miles = float(input("Enter miles: "))
# if miles >= 0:
#     print("KM:", miles * 1.609)
# else:
#     print("Invalid distance")

# check if a number is positive or negative

# a = int(input("Enter number: "))
# if a > 0:
#     print("Positive")
# else:
#     print("Negative")

#  check if a number is a multiple of 5

# a = int(input("Enter number: "))
# if a % 5 == 0:
#     print("Multiple of 5")
# else:
#     print("Not a multiple of 5")

# check if a number is positive negative or zero

# a = int(input("enter a number:"))
# if a > 0:
#     print("positive")
# elif a < 0:
#     print("negative")
# else:
#     print("zero")

# largest of 3 numbers

# a = int(input("enter a number:"))
# b = int(input("enter a number:"))
# c = int(input("enter a number:"))

# if a > b and a > c:
#     print("a is largest")
# elif b > a and b > c:
#     print("b is largest")
# else:
#     print("c is largest")

# REVERSE of a number
# 345
# 543

# num = 345
# rev = 0
# while num > 0:
#     b = num % 10
#     rev = rev*10+b
#     num = num//10
# print(rev)

# for i in range(4):
#     for j in range(4):
#      print("* ",end="")
#     print()

# for i in range(1,6):
#     for j in range(1,i+1):
#         print(j,end="")
#     print()

# for i in range(1,6):
#     for j in range(1,i+1):
#         print(i,end="")
#     print()

# for i in range(1,7):
#     for k in range(1,7-i):
#         print(" ",end="")
#     for j in range(1,i+1):
#         print("$ ",end="")
#     print()

# for i in range(0, 6):
#     for k in range(0, 6-i):
#         print(" ", end="")
#     for j in range(0, i+1):
#         print(" *", end="")
#     print()
# for i in range(6, 0, -1):
#     for k in range(6-i):
#         print(" ", end="")
#     for j in range(1, i+1):
#         print(" *", end="")
#     print()

# for i in range(1,7):
#     for k in range(1,7-i):
#         print(" ",end="")
#     for j in range(1,i+1):
#         print("$ ",end="")
#     print()
# for i in range(7,0,-1):
#     for k in range(7-i):
#         print(" ",end="")
#     for j in range(1,i+1):
#         print("$ ",end="")
#     print()


# lemonade change leetcode

# def lemonade(bills):
#     five = 0
#     ten = 0

#     for bill in bills:

#         if bill == 5:
#             five += 1

#         elif bill == 10:
#             if five == 0:
#                 return False

#                 five -= 1
#                 ten += 1

#         elif bill == 20:
#             if ten > 0 and five > 0:
#                 ten -= 1
#                 five -= 1

#         elif five >= 3:
#             five -= 3

#         else:
#             return False
#     return True


# given a sentence ,create a dictionary containing the frequency of each word.
# input:
# "python is easy and python is powerful"

# # expected:
# {
#     "python":2,
#     "is":2,
#     "easy":1,
#     "and":1,
#     "poweful":1
# }

# a = "python is easy and python is powerful"
# b = {}
# for i in a.split():
#     b[i] = b.get(i, 0)+1
# print(b)

# a = "python is easy and python is powerful"
# a = a.split(" ")
# b = {}
# for i in a:
#     if i in b:
#         b[i] = b[i]+1
#     else:
#         b[i] = 1
# for i in b:
#     print(i, b[i])


# reverse the keys and values of a dictionary
# input:
# {"a":1,"b":2,"c":3}

# output
# {1:"a",2:"b",3:"c"}

# a = {"a": 1, "b": 2, "c": 3}
# b = {}
# for key, value in a.items():
#     b[value] = key
# print(b)

# a = {"a": 1, "b": 2, "c": 3}
# b = {}
# for i in a:
#     b[a[i]]=i
# print(b)


