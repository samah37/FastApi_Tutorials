from fastapi import FastAPI, Query,Path
from enum import Enum
from pydantic import BaseModel
from typing import Optional
from Item import Item


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet =  "lenet"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
            return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path: path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
from typing import Optional
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id" : item_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.post("/item_test/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str]= None):
    item.name =  "hihi"
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

@app.get("/items_test/")
async def read_items(q: Optional[str]= Query(None, max_length=50)):
    results =  {"items": [{"item_id": "Foo"}, {"item"}]}
    if q:
        results.update({"q": q})
    return results

@app.get('/items_path/{item_id}')
async def read_items(
        item_id : int = Path(..., title="The ID of the item to get"),
        q: Optional[str] =  Query(None, alias="item-query")
):
    results = {"item_id": item_id}
    if q:
        results.update({"q" : q})
    return results







