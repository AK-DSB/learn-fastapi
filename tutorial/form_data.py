from typing import Annotated
from fastapi import FastAPI, Form, Request

app = FastAPI()


@app.post('/login/')
async def login(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    return {"username": username}


@app.put('/login/')
async def login(request: Request):
    # data = await request.json()
    data = await request.form()
    print(data)
    print(data.get('username'))
    return data
