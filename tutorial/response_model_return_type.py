from typing import Any
from fastapi import FastAPI, Response
from pydantic import BaseModel, EmailStr
from fastapi.responses import RedirectResponse

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


# @app.post('/items/')
# async def create_item(item: Item) -> Item:
@app.post('/items/', response_model=Item)
async def create_item(item: Item) -> Any:
    return item


# @app.get('/items/')
# async def read_items() -> list[Item]:
@app.get('/items/', response_model=list[Item])
async def read_items() -> Any:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str


@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    print(user)
    return user


@app.get('/portal', response_model=None)
async def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get('/items/{item_id}', response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items.get(item_id)

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get(
    '/items/{item_id}/name',
    response_model=Item,
    response_model_include={'name', 'description'}
)
async def read_item_name(item_id: str):
    return items.get(item_id)


@app.get('/items/{item_id}/public', response_model=Item, response_model_exclude={'tax'})
async def read_item_public_data(item_id: str):
    return items.get(item_id)
