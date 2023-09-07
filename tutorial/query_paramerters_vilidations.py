from typing import Annotated

from fastapi import Depends, FastAPI, Query, Request
from pydantic import BaseModel


app = FastAPI()


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


@app.get('/items_annotated/')
async def read_items_by_annnotated(
    q: Annotated[
        str | None, Query(max_length=50, regex='^fixedquery$')
    ] = None
):
    results = {'items': [{'item_id': 'Foo'}, {'item_id': 'Bar'}]}
    if q:
        results.update({'q': q})
    return results


@app.get('/items_old_version/')
async def read_items(q: str | None = Query(default=None, max_length=50, regex='^fixedquery$', pattern='^fixedquery$')):
    results = {'items': [{'item_id': 'Foo'}, {'item_id': 'Bar'}]}
    if q:
        results.update({'q': q})
    return results


@app.get('/items_with_default/')
async def read_items_with_default(q: Annotated[str, Query(min_length=3)] = 'finxedquery'):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get('/items_with_required')
async def read_items_with_required(q: Annotated[str, Query(max_length=3)]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get('/items_with_ellipsis')
async def read_items_with_ellipsis(q: Annotated[str, Query(min_length=3)] = ...):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get('/items_required_with_none')
async def read_items_required_with_none(q: Annotated[str, Query(min_length=3)] = ...):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get('/items_with_multiple_values')
# async def read_items_with_multiple_values(q: Annotated[list[str] | None, Query()] = None):
async def read_items_with_multiple_values(q: list[str] | None = Query(default=['22', '33'])):
    print(q)  # ['22']
    query_items = {'q': q}
    return query_items


@app.get('/items_with_alias')
async def read_items_with_alias(q: Annotated[str | None, Query(alias='item-query')] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get('/items_with_exclude/')
async def read_items_with_exclude(hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None):
    if hidden_query:
        return {'hidden_query': hidden_query}
    return {'hidden_query': 'Not found'}


class QueryItem(BaseModel):
    price: int = Query(gt=0)
    name: str = Query()


@app.get('/items_query')
async def read_items_with_query(q: QueryItem = Depends()):
    results = {'q': q}
    print(q)
    return q
