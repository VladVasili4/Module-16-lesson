from fastapi import FastAPI, Path, HTTPException, status, Body, Request, Form
from fastapi.responses import HTMLResponse
# from typing import Annotated
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory='templates_16_6')


messages_db = []


class Message(BaseModel):
    id: int = None
    text: str

@app.get("/")
def get_all_messages(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('message.html', {'request': request, 'messages': messages_db})


@app.get(path="/message/{message_id}")
def get_message(request: Request, message_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse('message.html', {'request': request, 'message': messages_db[message_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.post("/", status_code=status.HTTP_201_CREATED) # status_code=status.HTTP_201_CREATED - не обязательно.
# "/" должен совпадать с <form method="post" action="/"> в message.html (внимание на action)
def create_message(request: Request, message: str = Form()) -> HTMLResponse:
    # message_id = len(messages_db)
    if messages_db:
        message_id =max(messages_db, key=lambda m: m.id).id + 1
    else:
        message_id = 0
    messages_db.append(Message(id=message_id, text=message))
    return templates.TemplateResponse('message.html', {'request': request, 'messages': messages_db})


@app.put("/message/{message_id}")
def update_message(message_id: int, message: str = Body()) -> str:
    try:
        edit_message = messages_db[message_id]
        edit_message.text = message
        return f"Message updated!"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")



@app.delete("/message/{message_id}")
def delete_message(message_id: int) -> str:
    try:
        messages_db.pop(message_id)
        return f"Message ID={message_id} deleted!"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.delete("/")
def kill_message_all() -> str:
    messages_db.clear()
    return "All messages deleted!"

# uvicorn main:app              - запуск сервака
# python -m venv venv
# pip install
