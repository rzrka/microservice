import asyncio


def deco(a):
    def inner(func):
        def wrapper(*args, **kwargs):

            print(a)
            result = func(*args, **kwargs)

            return result

        return wrapper
    return inner


@deco(10)
def func(string):
    print("call func")
    return string

print(func("hello"))