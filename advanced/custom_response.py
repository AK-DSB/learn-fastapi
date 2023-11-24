import typing
from fastapi import FastAPI
from fastapi.responses import FileResponse, ORJSONResponse, HTMLResponse, Response, StreamingResponse
import orjson

app = FastAPI()


@app.get('/items/', response_class=ORJSONResponse)
async def read_items():
    return ORJSONResponse([{'item_id': 'Foo'}])


@app.get("/html_items/", response_class=HTMLResponse)
async def read_html_items(return_str: bool):
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    if return_str:
        return html_content
    return HTMLResponse(content=html_content, status_code=200)


@app.get('/legacy/')
def get_legacy_data():
    data = """<?xml version="1.0"?>
        <shampoo>
        <Header>
            Apply shampoo here.
        </Header>
        <Body>
            You'll have to use soap here.
        </Body>
        </shampoo>
        """
    return Response(content=data, media_type='application/xml')


async def fake_video_streamer():
    for i in range(10):
        yield b'some fake video bytes'


@app.get('/')
async def main(return_video: bool = False, return_file: bool = False):
    if return_video:
        return StreamingResponse(fake_video_streamer(), media_type='video/mp4')
    some_file_path = "large-video-file.mp4"

    if return_file:
        return FileResponse(some_file_path)

    def iterfile():
        with open(some_file_path, mode='r') as f:
            yield from f
    return StreamingResponse(iterfile(), media_type='video/mp4')


class CustomORJSONResponse(Response):
    media_type = 'application/json'

    def render(self, content: typing.Any) -> bytes:
        assert orjson is not None, "orjson must be installed to use ORJSONResponse"
        return orjson.dumps(content, option=orjson.OPT_UTC_Z)


@app.get('/orjson/', response_class=CustomORJSONResponse)
def read_orjson():
    return [{'item_id': 'Foo'}]
