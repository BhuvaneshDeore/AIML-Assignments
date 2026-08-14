# Errors
# ZeroDivisionError 42/0 , ValueError int('abc') , TypeError '2'+2 , IndexError [1,2][5]

# hw 4 diff codes for this exceptions

# 1) ZeroDivisionError

def div(a,b):
  try:
    a = int(input("enter a:"))
    b = int(input("enter b:"))
    print(a/b)
  except ZeroDivisionError:
      print("Division by zero error , enter no except 0")




# 2) ValueError

def spam(x):
   try:
      x= int(input("Enter number:"))
      return x
   except ValueError:
      print("ValueError , enter integer")


5# 3) TypeError

x = int(input("Enter x:"))
y = input("Enter y:")
def spam(x, y):
    try:
        return x + y
    except TypeError:
        print("TypeError")

spam(x, y)

# 3) IndexError

my_list = [10, 20, 30]

def spam(my_list):
    try:
        return my_list[4]
    except IndexError:
        print("IndexError")

spam(my_list)