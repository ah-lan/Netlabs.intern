letters =['a','b','c','d']
print(letters)
vowels=['e','o','i','u']
letters.append('mugenyi')
print(letters)
x=letters.extend(vowels)
print(x)
print(letters)
letters.pop()
print(letters)
letters.count(letters)##
print(letters) 
letters.reverse()  
print(letters)
letters.sort(key=len)     ###
print(letters)

my_tuple =(1,2,3,"allan")
print(my_tuple)

set1 ={1,2,3,4}
set2 ={3,4,5,6}
n=set1.intersection(set2)
y=set1.union(set2)
print(n,y)
z=set1.symmetric_difference(set2)
m=set1.difference(set2)
print(z,m)

#file handling, writing and reading files.
file =open("C:\\Users\\ALLAN\Desktop\\netlabs\\allan.txt ", "r")
content=file.read()
print(content)
file.close()

with open("C:\\Users\\ALLAN\Desktop\\netlabs\\allan.txt ", "r") as file:
    content=file.read()
print(content)

##EXCEPTION handling.


student_info = {
    'name': 'Sarah',
    'age': 16,
    'subjects': ['Math', 'Science', 'Computer Science'],
    'gpa': 3.8
}

def display_student(student):
    print(f"Student: {student['name']}")
    print(f"Age: {student['age']}")
    print("Subjects:")
    for subject in student['subjects']:
        print(f" - {subject}")
    if student['gpa'] >= 3.5:
        print("Great job! You're doing excellent!")
    else:
        print("Keep working hard!")

display_student(student_info)