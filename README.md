<h4>Abnormalities</h4>

###### What is abnormalities? 
Tracer is a package that can capture global exceptions, and you can configure which methods will be captured by tracer. After the exceptions are captured, you need to add a callback function, and the program will automatically execute this callback function. 


###### How to install abnormalities?
> pip3 install abnormalities


###### How to use abnormalities? 
1. Use abnormalities hook function 
```python3
# coding: utf-8
from abnormalities import patch_all_exception

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
from abnormalities import patch_all_exception


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
3. Use class function and async function
```python3
# _*_ coding: utf-8 _*_
import asyncio
from abnormalities import patch_all_exception


def callback(error):
    print('[*] Error: ', error)


def sync_run(*args):
    raise RuntimeError()


def sync_run_t(*args):
    raise RuntimeError()


async def run(*args):
    raise TypeError()


class Runner(object):
    def __init__(self):
        pass

    def sync_run(self):
        raise RuntimeError()

    async def run(self):
        raise RuntimeError()


patch_all_exception(
    callback=callback,
    objects=locals(),
    exceptions=(BaseException, ),
    ignore_exceptions=(TypeError, ),
    need_exit=False
)


def main():
    sync_run('sync_run')
    sync_run_t('sync_run_t')
    runner = Runner()
    runner.sync_run()
    asyncio.run(runner.run())
    asyncio.run(run('run'))


if __name__ == '__main__':

    main()
```

###### What did abnormalities solve for us? 
Abnormalities can use the callback method to call back when there is an exception in our program, and we can perform early warning and other methods after the exception, which is very convenient. 


###### How does it work? 
It uses the principle of decorators, replacing all functions in the code and adding hooks to functions that return errors
