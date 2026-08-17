# assignment

# worked example :Student_marks.py

marks = np.array([86,90,78,92,86])
print("Marks:", marks)
print("Total:", np.sum(marks))
print("Average:", np.mean(marks))
print("Highest:", np.max)

# Requests and JSON
# - making get request , and reading it back


res = requests.get('https://www.google.com/')
res.status_code

res.text

res.raise_for_status()  # raises an error automatically on 404,500,etc

# this code provides an error bcz google returns HTML page and we are trying to send data in json

res = requests.get('https://www.google.com/')
data = res.json()
data['name']

"""# Getting JSON data - python objects , not text

# GET vs. POST
- asking vs. sending
"""

# syntax of get request
requests.get(url)

requests.get('https://www.google.com/')

# syntax of post request
requests.post(url, json =data)

requests.post('https://www.google.com/', json = {'text':'hello'})
