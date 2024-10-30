import asyncio
from re import split
from typing import List


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

import asyncio


class A:


    def __init__(self):
        print("class A")


a = A()