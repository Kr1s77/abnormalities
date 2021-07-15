<h4>Tracer</h4>

###### What is tracer? 
Tracer is a package that can capture global exceptions, and you can configure which methods will be captured by tracer. After the exceptions are captured, you need to add a callback function, and the program will automatically execute this callback function. 


###### How to use tracer? 
1. Use tracer hook function 
```python3
# coding: utf-8
import patch_all_exception

def error_call_back(exc_traceback):
    print("Log: ", exc_traceback)


def test_func():
    raise TypeError('Hello')


patch_all_exception(
    error_call_back, locals(), exceptions=(TypeError, RuntimeError)
)


if __name__ == '__main__':
    test_func()
```
2. Use tracer hook class and async func
```python3
# coding: utf-8
import asyncio
from tracer import patch_all_exception


def error_call_back(exc_traceback):
    print("Log: ", exc_traceback)


def _func():
    raise Exception('Hello')


class TModel(object):
    def __init__(self):
        pass

    def func(self):
        raise TypeError('world')
        # print('in')

    async def run(self):
        raise TypeError('hello')


async def run():
    raise TypeError('world')


patch_all_exception(
    error_call_back, locals(), exceptions=(Exception, RuntimeError)
)


if __name__ == '__main__':
    asyncio.run(TModel().run())
```

###### What did tracer solve for us? 
Tracer can use the callback method to call back when there is an exception in our program, and we can perform early warning and other methods after the exception, which is very convenient. 