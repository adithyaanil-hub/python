# control statements
# control the flow of a program

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

# find sum of all digits of number 15324

# num = 15324
# sum = 0
# while num > 0:
#     digit = num % 10
#     sum = sum+digit
#     num = num//10
# print(sum)

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

# for loop
# for i in range()

# range(start,stop,step)

# for i in range(1,20,2):
#     print(i)

# for i in range(10,0,-1):
#     print(i)

# sum of 1st 10 numbers using for loop
# sum = 0
# for i in range(1,10,1):
#     sum = sum+i
# print(sum)

# factorial of number

# fact=1
# num=int(input("enter no:"))
# for i in range(1,num+1):
#     fact=fact*i
# print(fact)

# count=int(input("enter count:"))
# sum=0
# for i in range(1,count+1):
#     b=int(input("enter num:"))
#     sum=sum+b
# print(sum)
# print(sum/count)

# check if a number is prime or not
# num = int(input("enter no:"))
# flag = True
# if num == 1:
#     print("not a prime number")
# else:
#     for i in range(2, num):
#         if num % i == 0:
#             flag = False
#             break
# if flag == True:
#     print("prime")
# else:
#     print("not prime")


# continue
# for i in range(1, 10):
#     if i == 6:
#      continue
#     print(i)

# break
