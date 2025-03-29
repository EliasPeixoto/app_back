from pydantic import BaseModel
from typing import Optional, List
from model.veicle import Veicle
from datetime import datetime

class VeicleScheme(BaseModel):

    plate: str = "TAV8C99"
    model: str = "Moto"
    color: str = "Preta"
    checkin_date: datetime

class VeicleSearchScheme(BaseModel):

    plate:str

class VeicleListScheme(BaseModel):

    veicles:List[VeicleScheme]

def show_veicles(veicles: List[Veicle]):

    result = []
    for veicle in veicles:
        result.append(
            {
                "plate": veicle.plate,
                "model": veicle.model,
                "color": veicle.color,
                "checkin_date":veicle.checkin_date
            }
        )
    return {"veicles": result}

class VeicleViewScheme(BaseModel):

    id: int = 1
    plate: str = "TAV8C99"
    model: str = "Moto"
    color: str = "Preta"
    checkin_date: datetime

class VeicleCheckoutScheme(BaseModel):

    message: str
    plate: str

def show_veicle(veicle: Veicle):

    return {
        "id": veicle.id,
        "plate": veicle.plate,
        "model": veicle.model,
        "color": veicle.color,
        "checkin_date": veicle.checkin_date
    }

