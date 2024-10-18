import asyncio
from re import split
from typing import List


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

import asyncio

async def task_1():
    await asyncio.sleep(2)
    print("Task 1 completed")
    return 1

async def task_2():
    await asyncio.sleep(1)
    print("Task 2 completed")
    return 2

async def main():
    tasks = [task_1(), task_2()]
    while True:
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        for task in done:
            print(f"Result: {task.result()}")

        for task in pending:
            task.cancel()



asyncio.run(main())