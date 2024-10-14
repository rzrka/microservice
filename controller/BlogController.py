from enum import Enum
from typing import Optional, List

from fastapi import APIRouter, Response, status, Query, Path, Body, Depends
from schemas.BlogSchema import BlogSchema


def required_functionality():
    return {"message": "Learning FastAPI"}

router = APIRouter(
    prefix="/blog",
    tags=["blog"],
)


@router.get(
    "/all",
    summary="Получить все блоги",
    description="Апи предоставляет возможность получить все блоги",
    response_description="Список блогов",
)
def get_blog_all(page=1, page_size: Optional[int] = None, req_parameter: dict = Depends(required_functionality)):
    return {"message": f"page - {page}, page_size - {page_size}", "req": req_parameter}


@router.get('/{id}/comments/{comment_id}', tags=["blog", "comment", ])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    """
    Simulates retrieving a comment of a blog
    - **id** mandatory path parameter
    - **comment_id** mandatory path parameter
    - **valid** optional query parameter
    - **username** optional query parameter
    """
    return {'message': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}'}


class BlogType(str, Enum):
    short = "short"
    story = "story"
    howto = "howto"


@router.get("/type/{type}")
def get_blog_type(type: BlogType):
    return {"message": f"Blog type {type}"}


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_blog(id: int, response: Response):
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"Blog {id} not found"}
    return {"message": f"Blog with id -  {id}"}


@router.post("/new/{id}")
def create_blog(blog: BlogSchema, id: int, version: int = 1):
    return {
        "data": blog,
        "id": id,
        "version": version,
    }

@router.post("/new/{id}/comment/{comment_id}")
def create_comment(
        blog: BlogSchema,
        id: int,
        comment_title: int = Query(
            10,
            title="Title of the comment",
            description="Some descriptions for comment_title",
            alias="commentTitle",
            deprecated=True,
        ),
        content: str = Body(
            ...,
            min_length=10,
            max_length=50,
            regex="^[a-z\s]*$"
        ),
        v: Optional[List[str]] = Query(None),
        comment_id: int = Path(..., gt=5, le=10)
        ):
    return {
        "body": blog,
        "id": id,
        "comment_title": comment_title,
        "comment_id": comment_id,
        "content": content,
        "v": v,
    }