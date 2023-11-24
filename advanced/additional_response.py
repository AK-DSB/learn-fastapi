from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    value: str


class Message(BaseModel):
    message: str


app = FastAPI()


@app.get('/items/{item_id}', response_model=Item, responses={404: {'model': Message}})
async def read_item(item_id: str):
    if item_id == 'foo':
        return {'id': 'foo', 'value': 'there goes my hero'}
    return JSONResponse(status_code=404, content={'detail': 'Not found'})


@app.get(
    '/items/{item_id}',
    response_model=Item,
    responses={
        200: {
            'content': {'image/png': {}},
            'description': 'Return the JSON item or an image'
        },
    }
)
async def read_file_item(item_id: str, img: bool | None = None):
    if img:
        return FileResponse('static/img.png', media_type='image/png')
    return {'id': 'foo', 'value': 'there goes my hero'}
