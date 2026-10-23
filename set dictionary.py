# set
# {}
# collection of data
# unordered
# unindex
# mutable
# does not allow duplicate values
# a={1,2,3,3,3,2,1,4,5,6}
# print(a)

# a={1,2,3,4,5,6}
# b={4,5,6,7,8,9}

# print(a.union(b))
# or
# print(a|b)
# print(a.intersection(b))
# or
# print(a&b)

# print(b-a)

# fruits={"mango","orange","apple","pineapple"}
# for i in fruits:
#     print(i)

# dictionary

# collection of data
# key:value pairs
# key is unique
# no index
# mutable

# data={"name":"Adithya" ,"age":21,"place":"kannur"}
# print(data)
# print(type(data))
# print(data["age"])

# data["email"]="adithya@gmail.com"
# print(data)

# data={"name":"Adithya" ,"age":21,"place":"kannur"}
# data["name"]="adhi"
# print(data)

# userdata={}
# print(type(userdata))

# opeartions

# get
# data={"name":"adithya","age":21,"place":"kannur"}
# print(data["name"])
# or
# print(data.get("name"))

# update
# data.update({"age":"adithya@12.com"})
# print(data)

# pop
# data.pop("name")
# print(data)

# data={"name":"adithya","age":21,"place":"kannur"}
# print(data.keys())
# print(data.values())
# for i in data:
#     print(i,data[i])

# find reverse of a string without using[::-1]

# a="hari"
# rev=""
# for i in range(len(a)-1,-1,-1):
#     rev=rev+a[i]
# print(rev)

# data="my name is mohan , i am 27 years old"
# a=" "
# for i in data:
#     if i!= " ":
#         a=a+i
# print(a)

a = "my name is mohan,i am 27 years old"
words = a.split(" ")
li = []
for i in words:
    li.append(" " + i + " ")
print(li)
