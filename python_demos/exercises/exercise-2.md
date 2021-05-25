# Exercise 2

1. Implement this code in `__main__.py` in the `rates_demo` folder.

2. Install the "requests" package from PyPi.org.

https://docs.python-requests.org/en/master/user/quickstart/#make-a-request

3. Using the "requests" package API, call the following URL for each date returned from the "business_days" function. Copy the function from the "date_demos" folder, and utilize in the "rates_demo" folder.

http://localhost:5000/api/2019-01-01?base=USD&symbols=EUR

Iterate over a range of 20 business days, and run the above request for each day.

4. Create a list of text values from each response. The text value is formatted as JSON. Do not parse the JSON. Just put each JSON response in the list.

5. Display each list item in the console.