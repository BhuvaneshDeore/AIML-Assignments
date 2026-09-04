"""Day 7: Python Fundamentals
   Date : 16 -Aug -2026
   Name: Bhuvanesh Himmat Deore
   Contact no : 8080649149
   Email :bhuvideore18@gmail.coM
   Description : Topics that are covered on day 7
   Topics : 1)python libraries, 2) numpy list ,3) numpy array ,4)  accessing and changing elements ,
    5) A URL, and Python's built-in way to fetch on  6)requests are the simple syntax to use"""

    python libraries


import math

math.sqrt(25)



"""1. math& calculus
2. files
3. websites& the internet
4. dates & time
5. data processing
6. graphs & charts
7. datasets
8. machine learning model
"""

pip install numpy

import numpy as np

#numpy list
numbers = [10,20,30]
# list can

#numpy array
numbers = np.array([10,20,30,40])
# arrays can only stores single type of elements
#in arrays there are organised data so we ca flip the array but data will same and organised

numbers = [10,20,30]
result= []
for n in numbers:
  result.append(n*2)
result

numbers = np.array([10,20,30])
result = numbers*2
result

np.zeros(5)

np.ones(5)

np.arange(0,10,2)

# accessing and changing elements
numbers = np.array([10,20,30])
numbers[0]
numbers[1]=99
numbers

numbers+5

numbers*2

numbers/10

a= np.array([10,20,30])
b = np.array([1,2,3])
a+b

a*b

numbers =([10,20,30,40,50])
print(np.sum(numbers))
print(np.median(numbers))
print(np.max(numbers))

numbers = np.array([
[1,2,3],
[4,5,6]])
numbers.shape

numbers[0,1]



"""A URL, and Python's built-in way to fetch one"""

import urllib.request

response = urllib.request.urlopen('https://google.com')

response.status

"""requests are the simple syntax to use"""

import requests as req
req.get('https://google.com')

# making a GET requet , and reading it back

