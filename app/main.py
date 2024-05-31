from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math
import cmath
import numpy as np

app = FastAPI()

class Data(BaseModel):
    a: float
    b: float
    u: float
    l: float
    f: float
    o: float
    e: float
    c: float
    
class DataP(BaseModel):
    a: float
    b: float
    u: float
    f: float
    o: float
    e: float

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
    permitividad_dielec = (fa*permitividad) * 0.3 * 1e-3
    conductividad_conductor = data.o*1e7
    # longitud = np.zeros(int(data.l))
    atenuacion_l = []
    
    pen = math.sqrt(2/(fa * permea_medio * conductividad_conductor))
    # pen_str = format(pen, ".2e")
    if pen > data.a*1e-2:
        divisor = math.log(data.b / data.a)
        if divisor != 0:
            # L = permea_medio / (2 * math.pi) + permea_medio / math.pi * (math.log(data.b / data.a))
            j = cmath.sqrt(-1)
            L = permea_medio / (2 * math.pi) * (math.log(data.b/data.a)+1/4+1/(4*(data.c**2-data.b**2))*(data.b**2-3*data.c**2+4*data.c**4/(data.c**2-data.b**2)*math.log(data.c/data.b)))
            C = (2*math.pi * (permitividad)) / (math.log(data.b/data.a))
            R = 1/(2*conductividad_conductor*math.pi)*(1/data.a**2+1/(data.c**2-data.b**2))
            G = (math.pi*permitividad_dielec)/(math.log(data.b/data.a))
            Y = cmath.sqrt((R+j*fa*L)*(G+j*fa*C))
            for i in range(int(data.l)):
                atenuacion = Y.real*8.686*i
                atenuacion_l.append(atenuacion)
            return {
                'msg':'Es baja frecuencia',
                "L": format(L, ".2e"),
                'C': format(C, ".2e"),
                "R": format(R, ".2e"),
                "G": format(G, ".2e"),
                "conduc_d" : format(pen, ".2e"),
                "atenuacion" : atenuacion_l,
                "longitud": list(range(int(data.l)))
            }
        else:
            return {
                "error": "División por cero"
            }
    elif pen < data.a*1e-2:
        j = cmath.sqrt(-1)
        L=((permea_medio/(2*math.pi))*math.log(data.b/data.a))
        C = (2*math.pi*permitividad)/(math.log(data.b/data.a))
        R = (1/(2*math.pi*pen*conductividad_conductor))*(1/(data.a*1e-2)+1/(data.b*1e-2))
        G = (2*math.pi*permitividad_dielec)/(math.log(data.b/data.a))
        Y = cmath.sqrt((R+j*fa*L)*(G+j*fa*C))
        for i in range(int(data.l)):
            atenuacion = Y.real*8.686*i
            atenuacion_l.append(atenuacion)
        
        return {
            'msg':'Es alta frecuencia',
            "L": format(L, ".2e"),
            'C': format(C, ".2e"),
            "R": format(R, ".2e"),
            "G": format(G, ".2e"),
            "conduc_d" : format(permitividad_dielec, ".2e"),
            "atenuacion" : atenuacion_l, 
            "longitud": list(range(int(data.l)))
        }

def obtener_params_placas(data:DataP):
    fa = 2 * math.pi * data.f
    permea_medio = data.u * 4 * math.pi * 1e-7
    permitividad = data.e * 8.8542*1e-12
    conduc_dielect = fa*permitividad*0.2*1e-3 
    conductividad_conduc = data.o*1e7
    
    pen = math.sqrt(2 / (fa * permea_medio * conductividad_conduc))
    L = (permea_medio*data.a)/math.pi
    C = (permitividad*data.b)/data.a
    R = 2/(conductividad_conduc*pen*data.b)
    G = (conduc_dielect*data.b)/data.a
    
    return {
        "msg": 'Placas paralelas',
        "L": format(L, ".2e"),
        'C': format(C, ".2e"),
        "R": format(R, ".2e"),
        "G": format(G, ".2e"),
        
    }

@app.get("/")
async def root():
    return {"greeting": "Hola tilin"}

@app.post("/coaxial")
async def root(data: Data):
    return obtener_parametros(data)

@app.post("/placas")
async def root(data:DataP):
    return obtener_params_placas(data)