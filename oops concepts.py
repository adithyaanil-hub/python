# inheritance
# encapsulation
# abstraction
# polymorphism


# inheritance

# single level
# class Person1:  # parent class
#     def __init__(self):
#         pass

#     def read(self):
#         print("person can read")

#     def run(self):
#         print("person can run")


# class Person2(Person1):  # child class
#     def __init__(self):
#         pass

#     def jump(self):
#         print("person can jump")

#     def write(self):
#         print("person can write")


# p2 = Person2()
# p2.read()


# multi level

# class Person1:
#     def __init__(self):
#         pass

#     def read(self):
#         print("person can read")

#     def run(self):
#         print("person can run")


# class Person2(Person1):
#     def __init__(self):
#         pass

#     def jump(self):
#         print("person can jump")

#     def write(self):
#         print("person can write")


# class Person3(Person2):
#     def __init__(self):
#         pass

#     def fly(self):
#         print("person can fly")

#     def swim(self):
#         print("person can swim")


# class Person4(Person3):
#     def __init__(self):
#         pass

#     def sleep(self):
#         print("person can sleep")

#     def eat(self):
#         print("person can eat")


# p4 = Person4()
# p4.fly()


# class Person1:
#     def __init__(self):
#         pass

#     def read(self):
#         print("person can read")

#     def run(self):
#         print("person can run")


# class Person2(Person1):
#     def __init__(self):
#         pass

#     def jump(self):
#         print("person can jump")

#     def write(self):
#         print("person can write")


# class Person3(Person2):
#     def __init__(self):
#         pass

#     def fly(self):
#         print("person can fly")

#     def swim(self):
#         print("person can swim")

#     def speak(self):
#         print("person 3 can speak")


# class Person4(Person3):
#     def __init__(self):
#         pass

#     def sleep(self):
#         print("person can sleep")

#     def eat(self):
#         print("person can eat")

#     def speak(self):
#         print("person 4 can speak")
#         super().speak()


# p4 = Person4()
# p4.speak()


# multiple level

# class Person1:
#     def __init__(self):
#         pass

#     def read(self):
#         print("person can read")

#     def run(self):
#         print("person can run")

#     def speak(self):
#         print("person 1 can speak")


# class Person2():
#     def __init__(self):
#         pass

#     def jump(self):
#         print("person can jump")

#     def write(self):
#         print("person can write")

#     def speak(self):
#         print("person 2 can speak")


# class Person3():
#     def __init__(self):
#         pass

#     def fly(self):
#         print("person can fly")

#     def swim(self):
#         print("person can swim")

#     def speak(self):
#         print("person 3 can speak")


# class Person4(Person1, Person2, Person3):
#     def __init__(self):
#         pass

#     def sleep(self):
#         print("person can sleep")

#     def eat(self):
#         print("person can eat")


# # MRO-method resolution order
# p4 = Person4
# p4.speak()


# polymorphism
# poly-many
# morph-forms

# operator overloading

# class Student:
#     def __init__(self, m1, m2):
#         self.m1 = m1
#         self.m2 = m2

#     def __add__(self, othr):
#         t1 = self.m1+othr.m1
#         t2 = self.m2+othr.m2
#         return (t1, t2)

#     def __sub__(self, othr):
#         print("no difference allowed")

#     def __mul__(self, othr):
#         t3 = self.m1*othr.m1
#         t4 = self.m2*othr.m2
#         return (t3, t4)

#     def __truediv__(self, othr):
#         t5 = self.m1/othr.m1
#         t6 = self.m2/othr.m2
#         return (t5, t6)


# s1 = Student(7, 8)
# s2 = Student(5, 10)
# print(s1+s2)
# s1-s2
# print(s1*s2)
# print(s1/s2)


# method overloading

# class Mydata:
#     def __init__(self):
#         pass

#     def display(self, a, b):
#         print(a, b)

#     def display(self, a, b, c):
#         print(a, b, c)


# d1 = Mydata()
# d1.display(3, 4)
# d1.display(4, 5, 6)

# method overriding


# class A:
#     def __init__(self):
#         pass

#     def hello(self):
#         print("A hello")


# class B(A):
#     def __init__(self):
#         pass

#     def hello(self):
#         print("B hello")


# b = B()
# b.hello()


# abstraction


# from abc import ABC, abstractmethod


# class Animal(ABC):  # Abstract class
#     def __init__(self):
#         pass

#     @abstractmethod
#     def make_sound(self):
#         print("animal makes sound")


# class Dog(Animal):
#     def __init__(self):
#         pass

#     def make_sound(self):
#         print("makes sound")


# d = Dog()


# from abc import ABC, abstractmethod


# class Payment(ABC):
#     def __init__(self):
#         pass

#     @abstractmethod
#     def pay(self, amount):
#         pass


# class Upipayment(Payment):
#     def __init__(self):
#         pass

#     def pay(self, amount):
#         print(f"payed {amount} with upi")


# class Cardpayment(Payment):
#     def __init__(self):
#         pass

#     def pay(self, amount):
#         print(f"payed {amount} with card")


# upi = Upipayment()
# card = Cardpayment()
# upi.pay(2000)
# card.pay(1000)
