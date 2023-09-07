from typing import Annotated

from fastapi import FastAPI, Header, Query, Request

app = FastAPI()


@app.get('/items/')
async def read_items(
    user_agent: Annotated[str | None, Header()] = None,
    Authorization: Annotated[str | None, Header(
        convert_underscores=False)] = None,
    token: Annotated[str | None, Header(alias='Authorization')] = None
):
    print(user_agent)
    return {
        'User-Agent': user_agent,
        'Authorization': Authorization,
        'token': token
    }


@app.get('/items/strange/')
async def read_strange_items(
    strange_header: Annotated[str | None, Header(
        convert_underscores=False)] = None
):
    print(strange_header)
    return {'strange_header': strange_header}


@app.get('/items/multiple/')
async def read_multiple_items(
    requset: Request,
    x_token: Annotated[list[str] | None, Header()] = None
):
    print(x_token)
    print(requset.headers)
    return {'X-Token values': x_token}


@app.get('/items/params')
async def read_params_items(
    request: Request,
    qs: Annotated[list[str] | None, Query()] = None
):
    print(request.query_params)
    print(request.query_params.get('qs'))
    print(request.query_params.getlist('qs'))
    print(qs)
    return {'qs': qs}
