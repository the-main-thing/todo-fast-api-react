from typing import Union
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel

from todo import Todo
from id_generator import id_generator
from fake_db import db

app = FastAPI()

COOKIE_NAME = 'user_id'


def get_user(request: Request, response: Response):
    # every user shoul have a cookie with a unique identifier
    user_id = request._cookies.get(COOKIE_NAME)
    # looks like the first visit
    if not user_id:
        user_id = id_generator.get_id()
        # check for collisions
        while db.get_todos(user_id):
            user_id = id_generator.get_id()

        response.set_cookie(key=COOKIE_NAME, value=user_id)

    return user_id


@app.get("/get_all")
def get_all(request: Request, response: Response):
    user_id = get_user(request, response)
    todos = db.get(user_id)
    if not todos:
        todos = db.set_todos(user_id, [])

    return {"todos": todos}


@app.post("/update")
def update_todo(todo: Todo, request: Request, response: Response):
    user_id = get_user(request, response)
    todos = db.get(user_id)
    if not todos:
        todos = db.set_todos(user_id, [todo])

    updated = False
    for i in range(len(todos)):
        saved_todo = todos[i]
        if saved_todo.id == todo.id:
            updated = True
            todos[i] = todo

    if not updated:
        todos.append(todo)

    db.set_todos(user_id, todos)
    return todo
