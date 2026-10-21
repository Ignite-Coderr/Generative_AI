from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/Aman/Husain")
def add(a: int, b: int):      # My input going to be consider as integer
    return {"result": a + b}


class substractmode(BaseModel):
    a: int
    b: int


def substract(a:int,b:int):
    return a-b


@app.post('/substract')   # To move the particular method runninng in a particular system
def substract_number(model: substractmode):
    return substract(model.a,model.b)

print(add(10,20))

