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
