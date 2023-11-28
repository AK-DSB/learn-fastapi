from typing import Annotated, Any

from fastapi import FastAPI, Depends, HTTPException, status


app = FastAPI()


class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = '', *args: Any, **kwds: Any) -> Any:
        return q and self.fixed_content in q


checker = FixedContentQueryChecker('bar')


@app.get('/query-checker/')
async def read_query_check(fixed_content_included: Annotated[bool, Depends(checker)]):
    print(fixed_content_included)
    return {"fixed_content_in_query": fixed_content_included}
