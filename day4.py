#1. Numbers

# Arithmetic
a = 30
b = 6
print(a + b)
print(a - b)

# Modulus
a = 23
b = 7
print(a % b)


# Power
a = 3
b = 3
print(a ** b)

# Average
a = 75
b = 85
c = 95
avg = (a + b + c) / 3
print(avg)

# 2. Strings

# Index
name = "bhuvi"
print(name[0])
print(name[3])

# Slice
name = "Computer"
print(name[0:4])
print(name[:5])

# Methods
name = "bhuvi"
print(name.upper())
print(name.lower())

# Operations

a = "Good"
b = "Morning"
print(a + " " + b)
print(a * 3)



# 3. Lists

# Index
nums = [15, 25, 35, 45]
print(nums[0])
print(nums[-1])

# Add
nums = [15, 25, 35]
nums.append(45)
print(nums)

# Remove
nums = [15, 25, 35, 45]
nums.remove(25)
print(nums)
x = nums.pop()
print(x)
print(nums)

# Sort
nums = [60, 20, 50, 10, 40]
nums.sort()
print(nums)


# 4. Tuples

# Index
data = ("bhuvi", 22, "Python")
print(data[0])
print(data[1])

# Slice
nums = (15, 25, 35, 45, 55)
print(nums[1:4])
print(nums[:3])

# Unpack
data = ("Bhuvi", 22, "Python")
name, age, course = data
print(name)
print(age)

# Methods

nums = (10, 20, 20, 30, 20)
print(nums.count(20))
print(nums.index(30))

# 5. Dictionaries

# Access
student = {
    "name": "Bhuvi",
    "age": 22,
    "marks": 80
}
print(student["name"])
print(student["marks"])

# Add
student = {
    "name": "Bhuvi",
    "age": 22
}
student["course"] = "Python"
print(student)

# Update
student = {
    "name": "Gaurav",
    "age": 22
}
student["age"] = 23
print(student)