from typing import Annotated

from fastapi import Depends, FastAPI, Cookie, HTTPException, Header

app = FastAPI()


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != 'fake-super-secret-token':
        raise HTTPException(status_code=400, detail='X-Token header invalid')


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != 'fake-super-secret-key':
        raise HTTPException(status_code=400, detail='X-Key header invalid')
    return x_key


@app.get('/items/', dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    print(111)
    return [{"item": "Foo"}, {"item": "Bar"}]
