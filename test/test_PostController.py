import httpx
import pytest
from fastapi import status
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_201_CREATED

from models.PostModel import Post
from test.my_fixtures import post_valid, client, post_invalid, initial_posts, setup_db


@pytest.mark.asyncio
class TestCreatePerson:

    async def test_invalid(self, post_invalid: dict, client: httpx.AsyncClient):
        response = await client.post("/posts/new", json=post_invalid)
        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid(self, post_valid: dict, client: httpx.AsyncClient):
        response = await client.post("/posts/new", json=post_valid)
        assert response.status_code == HTTP_201_CREATED
        json = response.json()


@pytest.mark.asyncio
class TestGetPost:
    async def test_not_existing(self, client: httpx.AsyncClient):
        response = await client.get("/posts/abc/abc")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_existing(
            self, client: httpx.AsyncClient, initial_posts: list[Post]
    ):
        response = await client.get(f"/posts/{initial_posts[0].id}")

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json["id"] == str(initial_posts[0].id)
