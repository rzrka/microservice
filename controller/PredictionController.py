from enum import Enum
from typing import Optional, List, Sequence

from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from db.postgresql.postgresql import db_instance
from fastapi import APIRouter, Response, status, Query, Path, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.PostModel import Post
from schemas.PostSchema import PostRead, PostCreate, PostPartialUpdate, PostBase
from repository.PostRepository import PostRepository
from utils.Pagination import pagination
from datetime import datetime
from uuid import UUID
from models.NewsgroupsModel import PredictionOutput, newgroups_model, memory


router = APIRouter(
    prefix="/prediction",
    tags=["prediction"],
)




@router.post("")
async def prediction(
    output: PredictionOutput = Depends(newgroups_model.predict),
) -> PredictionOutput:
    return output


@router.delete("/cache", status_code=status.HTTP_204_NO_CONTENT)
def delete_cache():
    memory.clear()