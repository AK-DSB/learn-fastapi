from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    usl: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None
    images: list[Image] = []


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item] = []


@app.put('/items/{item_id}')
async def update_item(item_id: int, item: Item):
    print(item)
    print(item.tags)
    results = {"item_id": item_id, "item": item}
    return results


@app.post("/offers/", response_model=Offer)
async def create_offer(offer: Offer):
    return offer


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights
