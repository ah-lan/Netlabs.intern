student ={ "name":"mugeny",
          "sex": "male",
          "age":"25"}
print(student["name"])
for key,value in student.items():
    print(key,value)
if student["name"]=="mugenyi":
    print("he is the man")
else:
    print("you are not allowed in here")

for i in range(5):
    print(i)
x=input("enter ur new name")
def greet(x):
    return x
new_name = greet(x)
print(new_name) 

def calc(m,y):
    return m+y,m*y
total,product=calc(2,3)
print (total,product)

    

