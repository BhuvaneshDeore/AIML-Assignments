''' Day 6: Python Fundamentals
   Date : 14 -Aug -2026
   Name: Gaurav Bharat Deore
   Contact no : 9373446328
   Email :bharatdeore7813@gmail.com
   Description : Topics that are covered on day 5
   Topics : 1)Iterators ,2) Generators ,3) Decorators ,4)  Content manager (self)
   7)special methods,
'''

for nums in [10,20,30]: # iterable - jisse hum chize nikalte hai
  print(nums)

# ieterator - jo chize nikalta hai

nums =[10,20,30]
iterator = iter(nums)
print(next(iterator))
print(next(iterator))

iterator = iter([10,20])  # StopIteration : it throws an error when the elements are not in the range
print(next(iterator))
print(next(iterator))
print(next(iterator))

class Countdown:  # class create kela
  def __init__(self,start):  # init method banavli
    self.current =start
  def __iter__(self):  # iter method banavli ji pratek element la access karte
    return self
  def __next__(self):  # next method banavli ji next element return krte
    if self.current <0:
      raise StopIteration
    number =self.current
    self.current -= 1
    return number
for number in Countdown(3):
  print(number)

# assignment - 1) create iterator using iter and next method 3 elements chi list call 4 times a iterator
# Hw

iterator = iter(['a','b','c']) 
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator)) #StopIteration occurs when the iterator call for 4th time bcz there are only 3 elements

def get_num():
  yield 10  # yield to adding the number into function
  yield 20
  yield 30
get = get_num()
print(next(get))  # you actually go with explicit iteration call after the generator
print(next(get))
print(next(get))

# failure : to get the different values why ? bcz this is generator and it will go forgot

def count_up_to(limit):
  num = 1
  while num <= limit:
    yield num
    num += 1
for num in count_up_to(5):
  print(num)

num =list(
    range(1,1_000_001)   # buffiet
)

def num():
  for n in range(1,1_000_001):   # restraunt
    yield n

# List comprehension
[n *n for n in range(5)]

# generator expression()
(n*n for n in range(5)) # added a generator by swapping []
sq =(n*n for n in range(5))

print(next(sq))
print(next(sq))
print(next(sq))
print(next(sq))
print(next(sq))

def even_num(limit):
  for num in range(2,limit+1,2):
    yield num
for num in even_num(10):
  print(num)

# assignment
def even_num():
  for num in range(2,11,2):   # start :2 , stop :11, step 2
    yield num
for num in even_num(): # this for loop is for printing the next number
  print(num)

"""# Decorator"""

def say_hello():                                     # define an function
    user_name = str(input('Enter Your name:'))
    print(f"hello, {user_name}!!")

# A decorator is a function that takes another function as an argument
def decorator(func):   # define a decorator : it is use to decorate the function 
    def wrapper():    # wrapper is the new function that will replace the original function
        print("bol na bhidu")
        func()
    return wrapper


hel = decorator(say_hello)  # hel is a variable where we call function inside decorator

hel()

# syntax : @decorator

# assignment add syntax for this code

def decorator(func):
    def wrapper():
        print("bol na bhidu")
        func()
    return wrapper

@decorator
def say_hello():
    user_name = str(input("Enter Your name:"))
    print(f"hello, {user_name}!!")

say_hello()



# handling any arguments 
def decorator(func):
  def wrapper(*args, **kwargs):
    result =func(*args, **kwargs)
    return result
  return wrapper

@decorator
def add(a,b):
  return a + b

add(10,20)