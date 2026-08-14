
''' Day 1: Python Fundamentals
   Name: Bhuvanesh Himmat Deore
   Contact no : 8080649149
   Email :bhuvideore18@gmail.com
   Description : Topics that are covered on day 1
   Topics : 1) virtual environment ,2) vscode/jupyter notebook/kaggle ,3) commands ,4) DataTypes, 5) dictionary, 6) List , 
   7) Indexing, 8) Slicing , 9)Conditional Statements, 10)For loop, 11) While loop'''

# DataTypes
x=int(input("enter a valid number:"))
print(x)

# string to int
x ='12'
print(int(x))

# dictionary
dict = { 'x': "sham", 'y':"Aditya"}
print(dict['x'])
# list
list = ['2','5','6.5','amol',True,dict]
print(list)

# indexing
print(list[2])  


# slicing
print(list[1:3])

# question1 : take an string
m = "my name is bhuvi"

#question 2: print char upto index 6
print(m[0:6])

#question 3: print strings by removing first 2 chars
print(str[2:])

#question 4 : print middle char from str
print(str[11:17])

# formulate an problem statement based on conditional statement
age = int(input("enter your age : "))
if age>= 18:
  print("you are eligible to vote")
else:
  print("you are not eligible to vote")


"""Homework done
"""

# formulate an problem statement on for loop
# Example 1
for i in range(1,11):
  print(i)
c
# Example 2
for i in range(0,21,2):
  print(i)


x = "Abhishek"
for i in x:
    print(i)


    
# formulate an problem wih while loop
# Example 1|
n = int(input("Enter an number:"))
i = 1
while i <=10:
  print(i * n)
  i += 1

# Example 2
list = [5,10,15,20,25,30,35,40,45,50]
num = int(input("Enter number to find:"))
i = 0
while i < len(list):
  if list[i] == num:
    print('Number found at', i)
  i += 1

