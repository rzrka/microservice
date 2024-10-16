# from sqlalchemy.util import await_only
# import asyncio
# from repository.UserRepository import UserRepository
# from db.postgresql.postgresql import db_instance
#
# from repository.BaseRepository import BaseRepository
#
# async def get_repository(rep: str) -> BaseRepository:
#     repositories = {
#         "UserRepository": UserRepository
#     }
#     # async with db_instance.get_async_session() as session_gen:
#     session = await db_instance.get_async_session().__anext__()
#     return repositories[rep](session)
