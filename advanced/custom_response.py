from fastapi import FastAPI
from fastapi.responses import ORJSONResponse, HTMLResponse, Response, StreamingResponse

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
async def main():
    return StreamingResponse(fake_video_streamer())
