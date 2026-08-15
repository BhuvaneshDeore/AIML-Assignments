# Decorators and Context Managers in Python

## 1. Decorators

A decorator is used to add some extra functionality to an existing function without changing the actual function.

### Basic Decorator

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper
```

Here, `func` is the original function and `wrapper` is used to call that function.

`*args` : is used for positional arguments and stores them in a tuple like (TRue , 3.14,'Gaurav')

`**kwargs` is used for keyword arguments and stores them in a dictionary like kwargs = {"name": "Gaurav", "age": 20}

### Using `@decorator`

Instead of writing:

```python
add = decorator(add)
```

we can use:

```python
@decorator
def add(a, b):
    return a + b
add(10, 20)
```
---

## 2. Timing Decorator


```python
import time
from functools import wraps

def show_time(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        start = time.time()

        result = function(*args, **kwargs)

        print(f"Time taken: {time.time() - start:.4f}s")

        return result

    return wrapper
```

I used `time.time()` to get the current timestamp.

First, I store the starting time:

```python
start = time.time()
```

Then the original function is executed:

```python
result = function(*args, **kwargs)
```

After that, I subtract the starting time from the current time:

```python
time.time() - start
```

This gives the time taken by the function.

### Example

```python
@show_time
def train_one_epoch():
    time.sleep(2)
    print("Training completed!")

train_one_epoch()
```

The output will be something like:

```text
Training completed!
Time taken: 2.0003s
```

---

## 3. `@wraps(function)`

I learned that when a function is decorated, Python can treat the wrapper as the function.

`@wraps(function)` helps preserve the information of the original function, like its name and docstring.

```python
from functools import wraps
```

Then:

```python
@wraps(function)
def wrapper(*args, **kwargs):
```

So I can remember it as:

> `@wraps(function)` keeps the original function's information when using a decorator.

---

# 4. Context Managers

Context managers are useful when something needs to be opened and then properly closed.
A common example is file handling.

### Manual way

```python
file = open('/content/sample_data/mnist_test.csv')

content = file.read()

print(content)

file.close()
```

If I forget to close it, it can cause problems when working with files.

### Using `with`

Python provides a better way:

```python
with open('/content/sample_data/mnist_test.csv') as file:
    content = file.read()

print(content)
```

The `with` statement automatically handles closing the file.

This is one of the main reasons context managers are useful.

---

# 5. `__enter__()` and `__exit__()`

A context manager can be created using two special methods:

* `__enter__()`
* `__exit__()`

Example:

```python
class MyContext:

    def __enter__(self):
        print("Entering")
        return self

    def __exit__(self, exc_type, exc_value, tb):
        print("Leaving")

with MyContext():
    print("Inside")
```

Output:

```text
Entering
Inside
Leaving
```

---

# 6. Context Manager Using `@contextmanager`

Python also provides a shorter way to create a context manager using:

```python
from contextlib import contextmanager
```

Example:

```python
import time
from contextlib import contextmanager

@contextmanager
def timer():

    start = time.time()

    try:
        yield

    finally:
        print(f"Time: {time.time() - start:.4f}s")

with timer():
    train_one_epoch()
```


From this assignment, I understood:

* How decorators work in Python
* How `@decorator` works internally
* Difference between `*args` and `**kwargs`
* How to measure function execution time using a decorator
* Why `@wraps()` is used
* What context managers are
* How the `with` statement works
* How `__enter__()` and `__exit__()` work
* How `@contextmanager` can be used to create a context manager