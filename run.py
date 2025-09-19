from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class Item(BaseModel):
    name: str
    value: int

@app.get("/")
def hello():
    return {"Hello": "World"}

@app.get("/time")
def get_time():
    return {"current_time": datetime.now().isoformat()}

@app.get("/soma")
def soma(a: int, b: int):
    return {"result": a + b}

@app.post("/item")
def create_item(item: Item):
    return {"mensagem": f"Recebido {item.name} com valor {item.value}"}

@app.get("/invert")
def invert(texto: str):
    return {"invertido": texto[::-1]}
