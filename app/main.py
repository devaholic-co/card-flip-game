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

@app.websocket("/global-best-score")
async def get_global_best_score(websocket: WebSocket):
    await websocket.accept()
    current_best_score = 8888
    while True:
        if(current_best_score != game_service_obj.get_global_best_score()):
          current_best_score = game_service_obj.get_global_best_score()
          await websocket.send_text(str(current_best_score))
