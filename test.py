import asyncio
from re import split
from typing import List


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

import asyncio


def foo():
    print(1)
    yield 1
    print(2)

f = foo()
print(next(f))
print(next(f))