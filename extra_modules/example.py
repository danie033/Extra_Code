myset={"Daniel","Andres","Andres","Other"}


print(myset)

my_list=list(myset)

print(my_list)

def example(name:str,age:int) -> str:
    return f"This is {name} and my age is {age}."

print(example("Daniel",26))