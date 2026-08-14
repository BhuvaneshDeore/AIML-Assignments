''' Day 3: Python Fundamentals
   Date : 11 -Aug -2026
   Name: Bhuvanesh Himmat Deore
   Contact no : 8080649149
   Email :bhuvideore18@gmail.com
   Description : Topics that are covered on day 2
   Topics : 1) While loop,2) Break statement ,3) continue statement ,4) for loop , 5) range() function with 3 arguments, 6) modules ,
   7)random Module, 8) sys Module , 9)os Module, 10) math Module, 11)Minor project'''


# Loops , Flow Control and Modules

spam = 0
if spam <5:
  print("Hello world")
  spam += 1

# While loop
spam = 0
while spam <5:
  print("Hello World")
  spam += 1

name = ""
while name != 'your name':
  print('Please type your name.')
  name =input('>')
print("thank you")

""" **Break - stop the loop completely**"""

name = ""
while name != 'your name':
  print('Please type your name.')
  name =input('>')
  if name == 'your name':
    break
print("thank you")

"""**continue - skip some ietrations**"""

for num in range(10):
  if num % 2 ==0:
    continue
  print(num)

# for loop

for i in range(5):
  print('hello')

"""** range() takes 1 , 2,3 arguments
- range(stop)
- range(start, stop)
- range(start, stop, step) **
"""

# range()

for i in range(5):
  print('hii')

# range(start , stop)

for i in range(0,10):
  print(i)

# range(start, stop,step)
for i in range(0,10,2):
  print(i)

total = 0
for i in range(101):
  total += i
print(total)

"""# Module

- a module is a file of pre-written, related function
- konthi function use kartana module name .function
"""

# 1)random Module

import random
random.randint(1,10)

# 2) sys Module - provides communicattion with computer environment

#3) os Mudule -  it lets talks with os like connects with files , folders

# 4) math Module

import sys

while True:
  print('type to exit')
  response = input('>')
  if response =='exit':
    sys.exit()
  print('you typed'+ response+'')

"""**Minor Project**"""

# This is a guess the number game.
import random
secret_number = random.randint(1, 20)

print('I am thinking of a number between 1 and 20.')

# Ask the player to guess 6 times.
for guesses_taken in range(1, 7):
    print('Take a guess.')
    guess = int(input('>'))
    if guess < secret_number:
        print('Your guess is too low.')
    elif guess > secret_number:
        print('Your guess is too high.')
    else:
        break # This condition is the correct guess!

if guess == secret_number:
    print('Good job! You got it in ' + str(guesses_taken) + ' guesses!')
else:
    print('Nope. The number was ' + str(secret_number))