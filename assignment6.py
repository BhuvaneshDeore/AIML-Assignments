''' Assignment understand this code '''

# handling any arguments  
def decorator(func):
  def wrapper(*args, **kwargs):  # *args  -> accepts any number of positional arguments like args = (10, "hello", True)
    result =func(*args, **kwargs)  # **kwargs -> accepts any number of keyword arguments 
    return result                 # kwargs is a dictionary of keyword arguments like {'name':'gaurav}, 'age':20}
  return wrapper

# 'variable = decorator(add)'  = @decorator
@decorator  # @decorator matlab decorator le andar function call hota hai like decorator(add)
def add(a,b):
  return a + b

add(10,20)

'''timing decorator example'''

import time # we import time module
from functools import wraps  # functools se wraps import kiya 

# Decorator function
def show_time(function):
    # @wraps(function) is used to preserve the information of the original function when we use a decorator.
    @wraps(function)  # @wraps function original function ko wrap kr rha hai , original function ki info preserve kro 

    def wrapper(*args, **kwargs):
        start = time.time() # time.time current time ko leti hai aur voh value start variable main store kiya hai 

        result = function(*args, **kwargs) #jo values wrapper ko mili hain, woh values original function ko do, function ko run karo, use result main store kro
        print(f"Time taken: {time.time() - start:.4f}s") # ye print karega ki func ko ecexute hone main kitna time laga
       
        return result
    return wrapper


@show_time
def train_one_epoch():
    time.sleep(2)
    print("Training completed!")
train_one_epoch()


'''Context manager'''

# manual 
file = open('/content/sample_data/mnist_test.csv') # open the file 
content = file.read() # read it inside the variable content

print(content) # print the content that it read
file.close() # close the file 


# File Handling
with open('/content/sample_data/mnist_test.csv') as file: # this syntax is of file handling
    content = file.read()
print(content) # print the data that we read previously


'''__enter__ and __exit__'''  

class MyContext:
    def __enter__(self):
        print("Entering")
        return self
    def __exit__(self, exc_type, exc_value, tb):
        print("Leaving")
with MyContext():
    print("Inside")

'''Worked Example'''

import time # import time module
from contextlib import contextmanager # contextlib se contextmanager import kiya hai 

@contextmanager # decorator create kiya
def timer():
    start = time.time() # current time ko start variable main store kiya
    try:
        yield

    finally:
        print(f"Time: {time.time() - start:.4f}s") # code execute hone main kitna time laga ye print krta hai 
with timer():
    train_one_epoch()
