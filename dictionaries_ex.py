data = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}
other=data.get("johndoe")

print(other)
# print("Printing keys...")
# for i in data:
#     print(i)

# print("Now the values:")

# for j in data.values():
#     print(j)

class Person():
    def __init__(s,name,last_name,age):
        s.name=name
        s.last_name=last_name
        s.age=age
    
    def talk(s):
        return f"I am {s.name} {s.last_name} and I am {s.age}."
    
class Student(Person):
    def __init__(s, name, last_name, age,num_classes,major):
        super().__init__(name,last_name,age)
        s.num_classes=num_classes
        s.major=major
    
    def student_talk(s):
        result=s.talk()+ f"\nI took {s.num_classes} classes and my major is {s.major}."
        return result
    
#student=Student("Daniel","Figueroa",26,4,"Computing Science")

class Car:
    def __init__(self,make,mile):
        self.__make=make
        self.mile=mile

    def get_make(s):
        return s.__make
    
    def set_make(s,make):
        s.__make=make

# car1=Car("Honda",45651)

# car1.set_make("Kia")
# print(car1.get_make())
