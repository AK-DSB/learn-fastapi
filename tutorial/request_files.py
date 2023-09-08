from typing import Annotated
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post('/file/')
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    return {'file_size': len(file)}


@app.post('/uploadfile/')
async def create_upload_file(file: Annotated[UploadFile, File(description="A file read as UploadFile")]):
    print(file)
    print(file.file)
    return {'filename': file.filename}


@app.post('/files/')
async def create_fiels(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}


@app.post('/uploadfiles/')
async def create_upload_files(
    files: Annotated[list[UploadFile], File()],
    fileb: Annotated[bytes, File()],
    token: Annotated[str, Form()]
):
    print(len(fileb))
    print(token)
    return {"filenames": [file.filename for file in files]}
