from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math

app = FastAPI()

class Data(BaseModel):
    a: int
    b: int
    u: int
    l: int
    f: int
    o:int

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def obtener_parametros(data:Data):
    fa = 2*math.pi*data.f
    perm_medio = data.u*4*math.pi*1e-7
    pen = format(math.sqrt(2/(fa*perm_medio*data.o)),".2e")
    return{
        pen
    }


@app.get("/")
async def root():
    return {"greeting": "Hello world"}

@app.post("/coaxial")
async def root(data: Data):
    return obtener_parametros(data)    