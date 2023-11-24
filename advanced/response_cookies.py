from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse


app = FastAPI()


def create_cookie(response: Response, return_response: bool = False):
    if return_response:
        content = {'message': 'Come to the dark side'}
        headers = {'X-Cat-Dog': 'alone in the world'}
        response = JSONResponse(content=content, headers=headers)
        response.set_cookie(key='fakesession', value='fake cookie value')
        return response
    response.set_cookie(key='fakesession', value='fake cookie value')
    response.headers['X-Cat-Dog'] = 'alone in the world'
    response.status_code = status.HTTP_201_CREATED
    return {'message': 'Come to the dark side'}
