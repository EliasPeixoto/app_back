from pydantic import BaseModel
from typing import Optional, List
from model.veicle import Veicle
from datetime import datetime

class VeicleScheme(BaseModel):

    plate: str = "TAV8C99"
    model: str = "Moto"
    color: str = "Preta"

class VeicleSearchScheme(BaseModel):

    plate:str

class VeicleUptadeSucess(BaseModel):
    
    message:str