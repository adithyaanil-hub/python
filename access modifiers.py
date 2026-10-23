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