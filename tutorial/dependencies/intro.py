from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel


app = FastAPI()


class CommonParameter(BaseModel):
    q: str | None = None
    skip: int = 0
    limit: int = 100


async def common_parameters(q: str | None, skip: int = 0, limit: int = 100):
    return {'q': q, 'skip': skip, 'limit': limit}


@app.get('/items/')
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get('/users/')
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


CommonsDep = Annotated[dict, Depends(CommonParameter)]


@app.get('/items/common/')
# async def read_items(commons: Annotated[CommonParameter, Depends(CommonParameter)]):
async def read_items(commons: CommonsDep):
    return commons


@app.get('/users/common/')
async def read_users(commons: CommonParameter = Depends(CommonParameter)):
    return commons
