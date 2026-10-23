# list
# collection of data

# numbers=[1,2,3,4,5,6,7,8,9,10]
# print(numbers)
# print(type(numbers))

# 1.any data of any type

# a=[1,2,3,4,5,"mohan",True,[1,2,3]]

# 2.ordered

# a=[1,2,3]
# b=[2,3,1]

# 3.indexed

# list has index and it start from zero
# [start:end:step]
#  0 1 2 3 4 5 6 7 8 9 10 11 12
# a=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
# print(a)
# print(a[7])
# print(a[7:18])
# print(a[:4])
# print(a[::3])
# print(a[-2])
# print(a[::-1])

# a="adithya"
# print(a[1:5:2])
# print(a[::-1])

# a=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
# print(a[::2])

# mutable (changable)
# list is mutable

# a=[1,2,3,4,5,6,7]
# a[3]="mohan"
# print(a)

# string is immutable
# a="mohan"
# a[0]="l"
# print(a)

# list is dynamic

# add--->grow
# remove--->shrink

# inbuild methods
# add

# append()-add element to the end of list
# a=[1,2,3,4,5]
# a.append(300)
# print(a)

# extend(indexed iterable)
# a=[11,12,13,14,15]
# a.extend("adithya")
# print(a)

# insert(index,value)
# a=[11,12,13,14,15]
# a.insert(0,300)
# print(a)


# a=[11,12,13,14,15]
# a.insert(3,300)
# print(a)

# remove
# a=[11,12,13,14,15]
# a.remove(11)
# print(a)

# pop
# a=[11,12,13,14,15]
# a.pop(0)
# print(a)

# a=[11,12,13,14,15]
# a.pop()
# print(a)

# a=[11,12,13,14,15]
# a.clear()
# print(a)


# tuple
# collection of data
# ()

#  tuple is immutable
# t1=(11,12,13,14,15)
# t1[0]="mohan"
# print(t1)

# tuple is ordered
# tuple is indexed

# t1=(1,2,3,4,5,[1,2,3,4],"adithya")
# print(t1[5])

# t1 = (1, 2, 3, 4, 5, [1, 2, 3, "das", 4], "adithya")
# print(t1[5][3])

# a=[10,20,30]
# a.insert(1,100)
# print(a)

# name="mohan"
# a=[1,2,3,4,5]
# b=[11,12,13,14,15]

# for i in name:
#     print(i)

# for i in a:
#    print(i)

# for i in b:
#    print(i)

# len(name)

# for i in range(0,len(name)):
#     print(i,name[i])


#  1st method

# a = "hari"
# for i in range(len(a)):
#     if a[i] == "a" or a[i] == "e" or a[i] == "i" or a[i] == "o" or a[i] == "e" or a[i] == "u":
#      print(i, a[i])

# 2nd method

# a="hari"
# v="a,e,i,o,u"
# for i in range(len(a)):
#     if a[i] in v:
#         print(i,a[i])

# in -->membership operator

# a = "hari"
# b = [1, 2, 3, 4, 5]
# if 3 in b:
#     print("yes")


# string formatting

# name="mohan"
# age=20
# rating=8.7
# married_status=True
# z=f"my name is {name} my age is {age} my rating {rating} married_status {married_status}"
# print(z)

# create a list of first 100 numbers
# li=[]
# for i in range(1,101):
#     li.append(i)
# print(li)

# create a lists of even and odd numbers from first 100 numbers
# li=[]
# for i in range(1, 101):
#   if i % 2 ==0:
#      li.append(i)
#   else:
#     li.append(i)
# print(li)


# check if numbers are positive or negative or zero from given list
# z=[0,-2,-89,1,4,5,-199,-6]

# for i in z:
#   if i>0:
#     print(i,"positive")
#   elif i<0:
#     print(i,"negative")
#   else:
#     print(i,"zero")

# remove duplicates
# data=[1,2,3,4,5,3,4,1,2,3,6,5,4,2,7,8,3,2,1]
# b=[]
# for i in data:
#     if i not in b:
#         b.append(i)
# print(b)

# find smallest and largest from the given
# a=[10,-1,1000,-999,0,89,67,32,3278]

# largest=0
# smallest=0
# for i in a:
#     if i>largest:
#         largest=i
#     if i<smallest:
#         smallest=i
# print(largest,smallest)
