---
author: Jan Vermeir
brand: xebia.com
date: 2024-06-20 00:00:00+00:00
email: jan.vermeir@xebia.com
focus-keywords: python mocking
guid: https://xebia.com/wp-json/wp/v2/posts/82833
og:
  description: python Mocking, the Sneaky Bits
slug: python-mocking-the-sneaky-bits
status: draft
subtitle: ''
title: Python Mocking, the Sneaky Bits
---

While trying to mock a function in my python code, I found [this excellent blog](https://www.freblogg.com/pytest-functions-mocking-1) by Durga Swaroop Perla.
The blog shows how to use pytest-mock to replace a function with a test version. This would be useful when testing code that calls a database or an external service. The solution relies on the option in python to replace a definition with a new version within the scope of a function.

This looked good, so I wanted to apply the solution to my own code. My code follows a service/repository setup. I started with simple SQL queries and added filtering and other decisions based on data. So, initially I could just mock the database in my tests, but later I wanted to test the logic that was executed on the result set. So I figured I should split the code in a part that handles queries and a part that manipulates data. Duh, you'll say and I would
agree. In my defense I was just experimenting and things got out of hand. Ok, sorry!

So I tried to apply Durga's solution to my setup and was confused by the results. In my case the mocks were ignored. Struggling for a while just added to the confusion and frustration, so I took a step back and reduced the problem to the bare minimum.

My first version is shown below. Note that the code is spread across three files, which is essential. The name of the files is in comments in the code snippets, [you can find the sources here](https://github.com/jvermeir/python-mock-blog/)

```python
# service.py
from repository import my_repository
def my_service():
    print('my_service - calling my_repository')
    return my_repository()

# repository.py
def my_repository():
    print('my_repository - this is the real thing')
    return True

# test/test_service.py
from service import my_service
def test_my_service(mocker):
    mocker.patch('repository.my_repository', return_value=False)
    assert my_service() == False
```

So my assumption was that `mocker.patch('repository.my_repository', return_value=False)` in `test/test_service.py` would replace the `my_repository()` method with a constant `False` instead of `True`. But that didn't happen, the test failed. Argh!

What's the difference with Durga's version? In that example, the test code calls a function that calls another function which is mocked in the test. Exactly like I was doing, right? Not exactly as it turns out. The difference is that in my case the code is spread across three files, a service and repository file and a test file. While in Durga's blog the service and repository code are in the same file. This makes a difference for how the mock works.

To validate the one-file assumption I put the service and repository code in a single file, like this:

```python
# service_v3.py
def my_repository():
    print('my_repository - this is the real thing')
    return True

def my_service():
    print('my_service - calling my_repository')
    return my_repository()

# test/test_service_v3.py
from service_v3 import my_service
def test_my_service(mocker):
    mocker.patch('service_v3.my_repository', return_value=False)
    assert my_service() == False
```

This works, but in my case I would end up with a large file combining two aspects of my code, that I think need to be separated. So, now what?

Well, I thought maybe I'm not replacing the right thing? I changed the test to look like this:

```python
from service import my_service
def test_my_service(mocker):
    mocker.patch('service.my_repository', return_value=False)   
                # ^------- service, because why not?
    assert my_service() == False
```

The crucial change is this:

```python
mocker.patch('repository.my_repository', return_value=False)
```

was replaced by

```python
mocker.patch('service.my_repository', return_value=False)
```

This didn't make much sense to me, but my colleague Arjan Molenaar explained matters like this:

You can see a module as a map (dictionary). What happens is that by importing `my_repository` in the service module, it adds the function to the service module. This function is named `service.my_repository`. So its reasonable that changing `repository.my_repository` does not work because that is not the name of my_repository in the service module. When the test runs, I'm actually executing `service.my_repository` instead of `repository.my_repository`.

There is one alternative that might make things a little  more obvious:

```python
# service_v5.py
import repository  # <------ this is the magic incantation...
def my_service():
    print('my_service - calling my_repository')
    return repository.my_repository()

# repository.py
def my_repository():
    print('my_repository - this is the real thing')
    return True

# test/test_service_v5.py
from service_v5 import my_service
def test_my_service(mocker):
    mocker.patch('repository.my_repository', return_value=False) 
                # ^------------------ ...so we can do this
    assert my_service() == False
```

In this case, service_v5.py calls `import repository`, and then it calls `return repository.my_repository()`. So now we can do `mocker.patch('repository.my_repository', return_value=False)` because now we have `repository.my_repository` as key in our code map. This makes slightly more sense to me, but both versions work.

## Summary

So it's easy to mock the wrong thing. I hope this helps.

## Credits

I'm indebted to my colleague [Arjan Molenaar](https://www.linkedin.com/in/arjanmolenaar/) for explaining how python handles mocking.