# function
# It is a block of code executed when it is called

# def functionname(parameters):
# code to be executed

# def hello():
#     print("hello my name is")


# hello()  # calling the function

# arguements
# values to be passed to the function


# 2 types

# positional arguements
# def add(a,b):
#     print(a+b)
# add(3,11)

# keyword arguements
# def add(a,b):
#     print(a+b)
# add(b=6,a=6)

# default arguement
# def add(a=0,b=0):
#     print(a+b)
# add()

# factorial of number using function

# def factorial(num):
#     fact=1
#     for i in range(1,num+1):
#      fact*=i
#     print(fact)
# factorial(5)

# write a function to check if a string is unique

# def is_unique(str):
#     unique = True
#     for i in range(0, len(str)):
#         for j in range(i+1, len(str)):
#             if str[i] == str[j]:
#                 unique = False
#     if unique:
#         print("True")
#     else:
#         print("False")


# is_unique("apple")

# def add(a,b):
#     return(a+b)
# print(add(4,5))

# def add(a,b):
#     return(a+b)
# print(add(4,5))

# def add(a,b):
#     return 12,13,14,86,45,18,7
# print(add(4,5))

# simple calculator using functions

# def add(a, b):
#     return a + b


# def sub(a, b):
#     return a - b


# def mul(a, b):
#     return a * b


# def div(a, b):
#     return a / b


# a = int(input("Enter number: "))
# b = int(input("Enter number: "))

# op = input("Enter operation (+, -, *, /): ")

# if op == "+":
#     print(add(a, b))
# elif op == "-":
#     print(sub(a, b))
# elif op == "*":
#     print(mul(a, b))
# elif op == "/":
#     print(div(a, b))
# else:
#     print("Invalid operation")


# lambda function
# Anonymous function
# lambda arguements:expression

# b= lambda x,y: x+y
# print(b(4, 5))

# sqr= lambda n :n**2
# print(sqr(10))

# product of 3 numbers
# area of a triangle
# perimeter of circle
# full name of a person(fname)
# square root of a number
# average of 5 numbers
# check if a person is eligible to vote or not

# product of 3 numbers
# a=lambda x,y,z:x*y*z
# print(a(4,5,6))

# area of triangle
# area=lambda base,height:0.5*base*height
# print(area(4,5))

# perimeter of circle
# perimeter= lambda radius:2*3.14*radius
# print(perimeter(4))

# full name of a person(fname)

# fname=lambda a,b:a+" "+b
# print(fname("adithya","anil"))

# sqrt= lambda square:square*0.5
# print(sqrr(16)

# average of 5 numbers
# average=lambda a,b,c,d,e:(a+b+c+d+e)/5
# print(average(10,20,30,40,50))

# check if a person is eligible to vote or not
# vote = lambda age: "Eligible to vote" if age >= 18 else "Not eligible to vote"
# print(vote(20))


# recursion
# to recure to go back

# def countozero(n):
#     print(n)
#     if n==0:
#         return 0
#     return countozero(n-1)

# countozero(10)

# def countozero(n):
#     if n==0:
#         return 0
#     return n+countozero(n-1)

# print(countozero(5))

# def fact(n):
#     if n==1:
#         return n
#     return n*fact(n-1)

# print(fact(3))

# check if a number is amstrong or not
# num = 153


# def count(num):
#     count = 0
#     while num > 0:
#         count = count+1
#         num = num//10
#     return count


# print(count(num))


# def amstrong(num):
#     actual_no = num
#     c = count(num)
#     sum = 0
#     while num > 0:
#         b = num % 10
#         sum = sum+b**c
#         num = num//10

#     if sum == actual_no:
#         print("True")
#     else:
#         print("False")


# amstrong(num)
