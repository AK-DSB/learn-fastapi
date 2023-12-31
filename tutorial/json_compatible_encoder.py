from datetime import datetime
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item
fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


@app.put('/items/{id}')
def update_item(id: str, item: Item):
    print(item.timestamp)
    print(type(item.timestamp))
    json_compatible_item_data = jsonable_encoder(item)
    print(json_compatible_item_data)
    fake_db[id] = json_compatible_item_data
    return fake_db
