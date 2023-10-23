from typing import Union
from fastapi import FastAPI, HTTPException

import schemas


# DB
from deta import Deta
deta = Deta()
users = deta.Base("users")



app = FastAPI()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate):
    if users.fetch({"email": user.email}).count > 0:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = str(hash(user.password))
    return users.insert(user.model_dump())


@app.get("/users/", response_model=schemas.UserList)
def list_users(last: Union[str, None] = None, limit: int = 100):
    result = users.fetch(limit=limit, last=last)
    return schemas.UserList(users=result.items, last=result.last)


@app.get("/users/{key}", response_model=schemas.User)
def read_user(key: str):
    return get_user(key)


@app.post("/users/{key}/items/", response_model=schemas.User)
def create_item_for_user(key: str, item: schemas.Item):
    #users.update({"items": users.util.append(item.model_dump())}, key)
    user = get_user(key)
    user.items.append(item)
    user_dict = user.model_dump()
    ITEMS = "items"
    users.update({ITEMS: user_dict[ITEMS]}, key)

    return get_user(key)


@app.get("/users/{key}/items/", response_model=list[schemas.Item])
def read_items_for_user(key: str):
    return get_user(key).items


def get_user(key: str) -> schemas.User:
    db_user = users.get(key)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = schemas.User.model_validate(db_user)
    return user