from typing import Annotated

from fastapi import Body, FastAPI, Query, Path, Depends
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None
    description: str | None = None
    price: float = Field(
        gt=0, description='The price must be greater than zero')
    tax: float | None = None


@app.put('/items/{item_id}')
async def update_item(
        item_id: Annotated[int, Path(title='The ID of hte item to get', ge=0, le=1000)],
        importance: Annotated[int, Body()],
        important: int = Body(),
        q: str | None = None,
        item: Item | None = None,
        user: User | None = None,
):
    """
    {
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
        },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
        }
    }
    """

    results = {'item_id': item_id}

    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    if user:
        results.update({"user": user})
    if importance:
        results.update({"importance": importance})
    if important:
        results.update({"important": important})
    return results


@app.post('/items_with_embed/{item_id}')
async def items_with_embed(
        item_id: int,
        item: Annotated[Item, Body(embed=True)]
):
    results = {"item_id": item_id, "item": item}
    return results


@app.post('/items_without_embed')
async def items_without_embed(
        item_id: int,
        item: Annotated[Item, Body(embed=False)]
):
    results = {"item_id": item_id, "item": item}
    return results


class QueryItem(BaseModel):
    price: int = Query(gt=0)
    name: str = Query()


@app.get('/items')
async def read_items(q: QueryItem = Depends()):
    results = {'q': q}
    print(q)
    return q
