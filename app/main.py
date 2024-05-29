from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math

app = FastAPI()

class Data(BaseModel):
    a: float
    b: float
    u: float
    l: float
    f: float
    o: float
    e:float

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def obtener_parametros(data: Data):
    fa = 2 * math.pi * data.f
    permea_medio = data.u * 4 * math.pi * 1e-7
    permitividad = data.e * 8.8542*1e-12
    permitividad_dielec = fa*permitividad*0.2*1e-3 
    
    pen = math.sqrt(2 / (fa * permea_medio * data.o))
    pen_str = format(pen, ".2e")
    # return pen < data.a*1e-2
    if pen > data.a*1e-2:
        divisor = math.log(data.b / data.a)
        if divisor != 0:
            L = permea_medio / (4 * math.pi) + permea_medio / math.pi * (math.log(data.b / data.a))
            C = (2*math.pi * (permitividad)) / (math.log(data.b/data.a))
            R = 1/(2*data.o*math.pi)*(1/data.a**2)
            G = (math.pi*permitividad_dielec)/(math.log(data.b/data.a))
            return {
                'msg':'Es baja frecuencia',
                "L": format(L, ".2e"),
                'C': format(C, ".2e"),
                "R": format(R, ".2e"),
                "G": format(G, ".2e"),
            }
        else:
            return {
                "error": "División por cero"
            }
    elif pen < data.a*1e-2:
        
        L=(permea_medio/2*math.pi)*math.log(data.b/data.a)
        C = (2*math.pi*permitividad)/(math.log(data.b/data.a))
        R = 1/(2*math.pi*data.a*pen*data.o)*(1/data.a+1/data.b)
        G = (2*math.pi*permitividad_dielec)/(math.log(data.b/data.a))
        
        return {
            'msg':'Es alta frecuencia',
            "L": format(L, ".2e"),
            'C': format(C, ".2e"),
            "R": format(R, ".2e"),
            "G": format(G, ".2e"),
        }

def obtener_params_placas(data:Data):
    fa = 2 * math.pi * data.f
    permea_medio = data.u * 4 * math.pi * 1e-7
    permitividad = data.e * 8.8542*1e-12
    pen = math.sqrt(2 / (fa * permea_medio * data.o))
    
    return {}

@app.get("/")
async def root():
    return {"greeting": "Hola tilin"}

@app.post("/coaxial")
async def root(data: Data):
    return obtener_parametros(data)

@app.post("/placas")
async def root(data:Data):
    return obtener_params_placas(data)