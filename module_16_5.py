from fastapi import FastAPI, Path, HTTPException, Request
from pydantic import BaseModel
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')
users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get('/')
async def editing(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})

@app.get('/users/{user_id}')
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id-1]})


@app.post('/user/{username}/{age}')
async def post_user(user: User,
                    username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                    age: float = Path(ge=18, le=120, description='Enter age')) -> str:
    user.id = len(users) + 1
    user.username = username
    user.age = age
    users.append(user)
    return f"User {user.id} is registered"


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path()],
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                      age: float = Path(ge=18, le=120, description='Enter age')) -> str:
    try:
        edit_user = users[user_id - 1]
        edit_user.username = username
        edit_user.age = age
        return f"The User {user_id} is updated"
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path()]) -> str:
    try:
        users.pop(user_id - 1)
        return f'User ID {user_id} deleted!'
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')