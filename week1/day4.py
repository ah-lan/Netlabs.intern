# class Calculator:
#     def add(self, a, b):
#         return a + b

#     def subtract(self, a, b):
#         return a - b

#     def multiply(self, a, b):
#         return a * b

#     def divide(self, a, b):
#         if b == 0:
#             return "Cannot divide by zero!"
#         return a / b

# # Create a Calculator object
# calc = Calculator()

# print(calc.add(5, 3))   
# print(calc.subtract(10, 4))  
# print(calc.multiply(2, 7))   
# print(calc.divide(20, 5))    
# print(calc.divide(10, 0))    


# class Greet:
#     def __init__(self,name,birthday):
#         self.name =name
#         self.birthday = birthday

#     def say_hi(self):
#         print(f"hi",self.name)
#     def Birthday(self):
#         print(f"my birthday is",self.birthday)

# x=Greet("Allan","14th December")
# x.say_hi()
# x.Birthday()


class Student:
    def __init__ (self, name, age, grade):
        # These are attributes
        self.name = name      # String attribute
        self.age = age        # Integer attribute
        self.grade = grade    # Integer attribute
        self.subjects = []    # List attribute
        self.gpa = 0.0       # Float attribute

    def get_info(self):
        return f"{self.name} - Grade {self.grade}"
        
    
    # Method that changes object state (setter)
    def set_gpa(self, new_gpa):
        if 0.0 <= new_gpa <= 4.0:
            self.gpa = new_gpa
            print(f"my new_gpa is",new_gpa)
        else:
            print("Invalid GPA! Must be between 0.0 and 4.0")
    
    # Method that performs an action
    def celebrate_birthday(self):
        self.age += 1
        print(f"🎉 Happy Birthday {self.name}! Now {self.age} years old!")

student = Student("Emma", 16, 3.5)
print(student.get_info())
student.celebrate_birthday()
student.set_gpa(3.5)




