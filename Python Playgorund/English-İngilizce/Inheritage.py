class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def walk(self):
        print(f"{self.name} is walking.")

    def eat(self):
        print(f"{self.name} is eating.")

class Student(Person):
        def __init__(self, name, age, school):
            super().__init__(name, age)
            self.school = school

        def study(self):
            print(f"{self.name} {self.school} is studying in school.")

class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject

    def teach(self):
        print(f"{self.name} {self.subject} teaching in school.")