
  ''' Day 5: Python Fundamentals
   Date : 13 -Aug -2026
   Name: Bhuvanesh Himmat Deore
   Contact no : 8080649149
   Email :bhuvideore18@gmail.com
   Description : Topics that are covered on day 5
   Topics : 1) Type Hints,2) Class ,3) object ,4)  Attribute , 5) methods , 
   7)special methods,
   '''

# Type Hints , classes and special methods

def add(a,b):
  return a + b
add(2.5,4)

def add(a:int, b:int):  # Type hint
  return a+b

add(2,3.1)  # doesnot matter what value we passed its just an notation

name:str ='Gaurav'
age:int =21
height:float =5.4
is_student: bool =True
score:int # a hint alone . no value yet

# python verify nhi karta Type Hint ko
# int mention hai aur humne float diya toh bhi accept kr leta hai

def square(num:int) ->int: # -> return_type or the output datatpe
  return num * num

square(4)

def get_name()-> str:
  return 'Zopie'
get_name()

# multiple type hints are possible
def print_id(user_id:int | str): # | = indicates or
  print(user_id)
print_id(101)

numbers :list[int] =[10,20,30]
student_marks :dict[str,int]={'Alice':90}

def double(number:int)->int:
  return number * 2
double('Hii')

"""**Type hint just to help the programmer (just for reading , bertter documentatipon) it will never throuws an error even with datatype mismatched**"""

def calculate_avg(marks:list[int])->float:
  return sum(marks) / len(marks)

def display_student(name:str, marks:list[int]) ->None:
  avg :float =calculate_avg(marks)
  print(f'student:{name}')
  print(f'Average:{avg:.2f}')
display_student('Gaurav',[85,90,92])

"""# Class
  - a way to create your own type of object -keeping related data and behavior together
  - class  = is a blueprint
  - object = thing built from it
"""

class student:  # creating a class
  pass
stud1 =student() # creating a object
stud2 =student()

"""# Attribute
- data attached to an object
- object.(jo attribute usko specify karta hai)
"""

stud =student
stud.name ='Gaurav'
stud.age =20
stud.marks = 85
print(stud.name)

"""# __init__() method"""

class Student:
  def __init__(self,name,age):  # __init__ create am constructor
    self.name =name
    self.age= age
stud =Student('Gaurav',21)

# what is self - separate values/ attributes ko maintain karne main help karta hai

# jo class ke andar func define kiya jate hai usko methods bolte hai

class Student:
  def __init__(self,name , age): # create constructor
    self.name = name
    self.age =age
  def introduce(self): # introduce = method
    print(f'My name is {self.name}')
    print(f'My age is {self.age}')
stud =Student('Gaurav',21)
stud.introduce()

"""# Instance vs Class atrribute

- instance = dynamic anate hai aur sare objects main use hote hai

- class = dynamically nhi hote , hum bas use use karte hai
"""

class BankAccount:
  def __init__(self,owner,balance):
    self.owner =owner
    self.balance =balance
  def deposit(self,amount):
    self.balance += amount
  def withdraw(self,amount):
    if amount <= self.balance:
      self.balance -= amount
    else:
      print('insufficient balance')
  def show_balance(self):
    print(f'Balance:{self.balance}')
acc = BankAccount('Gaurav',5000)
acc.deposit(1500)
acc.withdraw(2000)
acc.show_balance()

# __str__ is a special method that returns string

class student:
  def __init__(self,name):  # create an constructor
    self.name =name
  def __str__(self):   # __str__ to return an string
    return f'{self.name}'
    print(student)


  def __repr__(self):   # __repr__ to return string only , if we passes an int still it will print 'int'
    return f'Student({self.name!r})'
    print(repr(student))

stud = student('gaurav')
print(stud)
print(repr('gaurav'))

# __repr__ ia special method that returns only string ( if we provide any datatype , it prints only in format of string)

class student:
  def __repr__(self):
    return f'Student({self.name!r})'
    print(repr(student))

  print(repr('gaurav'))

# __len__ is also a special method that returns length of an argumenmt
def __len__(self):
  return len(self.songs)
  len(playlist)

# __eq__ is used to compare 2 arguments or entities

def __eq__(self,other):
  return self.roll_no == other.roll_no
  stud1 == stud2


