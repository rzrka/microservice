import asyncio
from re import split
from typing import List


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

import asyncio


def running_operation(result, digit, operation) -> int:
    if not result:
        return int(digit)

    if operation == "*":
        result *= int(digit)
    elif operation == "-":
        result -= int(digit)
    elif operation == "+":
        result += int(digit)
    elif operation == "/":
        result /= int(digit)

    return result

def foo(string):
    global left
    operator = None
    result_operation = 0
    while left < len(string) - 1:
        left += 1
        s = string[left]
        if s in ("/", "+", "-", "*"):
            operator = s
            continue

        if s == '(':
            result_operation = running_operation(result_operation, foo(string), operator)

        if s == ')':
            return result_operation

        if s.isdigit():
            result_operation = running_operation(result_operation, s, operator)

    return result_operation

left = -1
print(foo("(*(+3 6)(*1 2 3))"))