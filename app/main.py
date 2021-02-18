from typing import Optional
import time

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

from app.services import game_service

game_service_obj = game_service.game_service()

app = FastAPI()

class PlayPayload(BaseModel):
    name: str
    pos: int
class NewGamePayload(BaseModel):
    name: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/play")
def play(payload: PlayPayload):
    return game_service_obj.play_game(payload.name, payload.pos)

@app.post("/new-game")
def play(payload: NewGamePayload):
    return game_service_obj.start_new_game(payload.name)

from fastapi.responses import HTMLResponse

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <div id="content">temp</div>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:80/ws");
            ws.onmessage = function(event) {
                document.getElementById("content").innerHTML = event.data;
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
@app.get("/html")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    highest_score = 9999
    while True:
        if(highest_score != game_service_obj.get_global_best_score()):
          highest_score = game_service_obj.get_global_best_score()
          await websocket.send_text(str(highest_score))
          