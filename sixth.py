#  elif statement

# smark = 85

# if smark > 90:
#     print("A")
# elif smark > 80:
#     print("B")
# elif smark > 70:
#     print("C")
# elif smark > 60:
#     print("D")
# else:
#     print("Fail")

# check if a number is positive negative or zero

# a = int(input("enter a number:"))
# if a > 0:
#     print("positive")
# elif a < 0:
#     print("negative")
# else:
#     print("zero")


# or statement

# true true = true
# true false = true
# false true = true
# false false = false

# a = 10
# b= 18
# if a>=10 or b<15:
#    print("yes")

# and

# true true = true
# true false = false
# false true = false
# false false = false

# a = 7
# b = 45
# c = 18
# if a >= 7 and b< 40:
#     print("yes")

# not
# a=18
# if not a>15:
#     print("yes")

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


# control statements

# while

# i = 1
# while i <= 10:
#     i = i+1
#     print(i)

# sum
# n=int(input("enter no:"))
# i=1
# s=0
# while i<=n:
#         s=s+i
#         i=i+1
# print(s)

# i = 1
# esum = 0
# osum = 0
# while i <= 100:
#  if i % 2 == 0:
#     esum = esum+i
# else:
#     osum = osum+i
#     i = i+1
# print(esum, osum)

# n = int(input("enter a no:"))
# i = 1
# fact = 1
# while i <= n:
#     fact = fact*i
#     i = i+1
# print(fact)

# num = 15324
# while num > 0:
#     print(num)
#     num = num//10

num = 15324
while num > 0:
    num = num//10
