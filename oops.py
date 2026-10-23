# introduction to oops
# object oriented programming language

# object
#    *attributes --variables
#     *behaviours--functions

# class-blueprint

# class Car:
#     def start():
#         print("car starts")

#     def stops():
#         print("car has stopped")


# car1 = Car
# car2 = Car
# print(car1)
# car1.start()
# car2.stops()


# constructor--to initialize
# __init__()

# class Car:
#     def __init__(self):
#         self.name = "honda city"
#         self.color = "black"

#     def start(self):       #methods
#         print("car starts")

#     def stops(self):
#         print("car has stopped")


# car1 = Car()
# print(car1.color, car1.name)
# car2 = Car()
# print(car2.color, car2.name)


# class Car:
#     def __init__(self, n, c):
#         self.n = n
#         self.c = c

#     def start(self):  # methods
#         print(f"{self.n}starts")

#     def stops(self):
#         print(f"{self.n}has stopped")


# car1 = Car("maruthi 800", "red")
# print(car1.c, car1.n)
# car2 = Car("amaze", "blue")
# print(car2.c, car2.n)
# car1.start()


# class Bike:
#     def __init__(self, n, c):
#         self.n = n
#         self.c = c

#     def start(self):  # methods
#         print(f"{self.n}starts")

#     def stops(self):
#         print(f"{self.n}has stopped")


# bike1 = Bike("hero honda", "red")
# print(bike1.c, bike1.n)
# bike2 = Bike("rx100", "blue")
# print(bike2.c, bike2.n)
# bike1.start()


# class Pen:
#     def __init__(self, name, price):
#         self.name = name
#         self.price = price

#     def compare(self, othr):
#         print(self.name)


# p1 = Pen("gripper", 20)
# p2 = Pen("lexi", 10)
# p1.compare(p2)

# create a class Student
# with 6 attributes name m1 m2 m3 m4 m5
# 3 methods
# sum_of_mark()
# average of mark()
# display_details()

class Student:
    def __init__(self, name, m1, m2, m3, m4, m5):
        self.name = name
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.m4 = m4
        self.m5 = m5

    def sum_of_marks(self):
        return self.m1+self.m2+self.m3+self.m4+self.m5

    def average_of_marks(self):
        return s1.sum_of_marks()/5

    def display_details(self):
        return self.name, self.m1, self.m2, self.m3, self.m4, self.m5


s1 = Student("mubasheer", 43, 42, 38, 44, 40)
print(s1.sum_of_marks())
print(s1.average_of_marks())
print(s1.display_details())
