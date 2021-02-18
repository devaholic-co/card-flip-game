from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from app.services import game_service

game_service_obj = game_service.game_service()

app = FastAPI()

class PlayPayload(BaseModel):
    name: str
    pos: int

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/play")
def play(payload: PlayPayload):
    return game_service_obj.play_game(payload.name, payload.pos)