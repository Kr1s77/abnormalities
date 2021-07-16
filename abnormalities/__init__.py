# _*_ coding: utf-8 _*_
"""
Author: Kris
Github: https://github.com/Kr1s77
"""
import traceback
from io import StringIO
from typing import Callable
from functools import wraps
from types import (
    FunctionType,
    CoroutineType,
    GeneratorType,
    AsyncGeneratorType
)

__version__ = '1.0.2'
__name__ = 'abnormalities'
__author = 'Kris'

# Find without callback objects
WITHOUT_CALLBACK_OBJECTS = []


def _error_callback(context: dict):
    #: Ignore exceptions while settings ignore_exceptions
    if type(context['error']) in context['ignore_exceptions']:
        raise

    #: Create Io receive error message and invoking call
    #: back function, bring error message to this func/
    fd = StringIO()
    traceback.print_exc(file=fd)
    context['callback'](fd.getvalue())

    #: If the program is configured with the option to
    #: exit when an error occurs, the program exits when
    #: the exception occurs and throws the exception as
    #: normal
    if context['need_exit']:
        exit(0)

    #: If there is no configuration program will work/
    else:
        pass


def _out_wrapper(context: dict, *args, **kwargs) -> None:
    try:
        return context['func'](*args, **kwargs)
    except context.get('exceptions', (BaseException,)) as error:
        # If in ignore exceptions, pass error
        context.setdefault('error', error)
        return _error_callback(context=context)


async def _async_out_wrapper(context: dict, *args, **kwargs) -> None:
    try:
        return await context['func'](*args, **kwargs)
    except context.get('exceptions', (BaseException,)) as error:
        # If in ignore exceptions, pass error
        context.setdefault('error', error)
        return _error_callback(context=context)


def exception_hook(context: dict) -> Callable:
    def hook_func(func):
        # Settings context
        context.setdefault('func', func)

        # Check if 'func' is a generator function.
        # Code from types. def coroutine(func): line 244
        if func.__code__.co_flags & 0x180:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                return await _async_out_wrapper(context, *args, **kwargs)
        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                return _out_wrapper(context, *args, **kwargs)
        return wrapper

    return hook_func


def exception_hook_class(context: dict) -> Callable:
    def hooker(cls):
        try:
            class Inner(cls):
                def __init__(self, *args, **kwargs):
                    for func_name in cls.__dict__.keys():
                        func = cls.__dict__[func_name]
                        if not isinstance(func, FunctionType) or func_name.endswith('__'):
                            continue
                        # Check if 'func' is a coroutine function.
                        if func.__code__.co_flags & 0x180:
                            self.set_wrapper_async(func=func)
                        else:
                            self.set_wrapper(func)

                    super(Inner, self).__init__(*args, **kwargs)

                def set_wrapper(self, func):
                    def wrapper(*args, **kwargs):
                        return _out_wrapper(context, self, *args, **kwargs)

                    setattr(self, func.__name__, wrapper)  # rewrite function

                def set_wrapper_async(self, func):
                    async def wrapper(*args, **kwargs):
                        return await _async_out_wrapper(context, self, *args, **kwargs)

                    setattr(self, func.__name__, wrapper)  # rewrite function

            return Inner
        except TypeError:
            WITHOUT_CALLBACK_OBJECTS.append(cls)
            return cls

    return hooker


def patch_all_exception(
        callback: Callable,
        objects: dict,
        exceptions: tuple = None,
        need_exit: bool = True,
        ignore_exceptions: tuple = None,
        ignore_objects: tuple = None
) -> list:
    """
    doc
    --------------------------------------------------------------
    This function is used to handle some abnormal errors. There
    are two ways to handle exceptions. The first is to throw an
    exception when it is found. The second is to choose not to
    throw an exception and configure the corresponding parameters.
    This method must be used after all the functions to be hooked
    . Do this method It is to notify me in time through my callback
    function robot when the program is abnormal, hope this method
    is suitable for you

    sample by kris: /usr/bin/python3 test func
    --------------------------------------------------------------
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


    >> Log:  Traceback (most recent call last):
    >> File "/Users/xxx/xxx/xxx/xxx/hook_exc.py", line 14, in wrapper
    >> return func(*args, **kwargs)
    >> File "/Users/xxx/xxx/test.py", line 12, in test
    >> raise TypeError('Hello')
    >> TypeError: Hello
    -------------------------------------------------------------------------------------

    sample by kris: /usr/bin/python3 test class and async func
    -------------------------------------------------------------------------------------
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

    -------------------------------------------------------------------------------------
    :param callback:  Callback function, occurs after the function is abnormal,
                      you can call the early warning program, etc.
    :param objects:   Object that are Hooked, if you want to Hook all functions
                      except magic functions, you can directly pass locals()
    :param exceptions: Want to handle those abnormal errors, the default is BaseException
    :param need_exit: Is it necessary to exit the program if an abnormality is found
    :param ignore_exceptions: Uncaught exception
    :param ignore_objects: Object not captured
    :return: None
    """
    ignore_objects = ignore_objects or tuple()
    ignore_exceptions = ignore_exceptions or tuple()

    hook_functions = filter(lambda x: not x.endswith('__'), objects.keys())
    exceptions = exceptions or (BaseException,)

    for func_name in hook_functions:
        if (func_name == callback.__name__ or
                not isinstance(objects[func_name], object) or
                not callable(objects[func_name]) or
                objects[func_name] == CoroutineType or
                objects[func_name] == GeneratorType or
                objects[func_name] == AsyncGeneratorType or
                objects[func_name] in ignore_objects):
            continue

        context = {
            'exceptions': exceptions,
            'callback': callback,
            'need_exit': need_exit,
            'ignore_exceptions': ignore_exceptions,
        }

        # Functions
        if isinstance(objects[func_name], FunctionType):
            objects[func_name] = exception_hook(context)(objects[func_name])
        # Classes do not need check generator
        else:
            objects[func_name] = exception_hook_class(context)(objects[func_name])

    return WITHOUT_CALLBACK_OBJECTS
