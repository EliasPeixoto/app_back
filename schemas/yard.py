from pydantic import BaseModel
from typing import Optional, List
from model.veicle import Veicle
from model.yard import Yard
from datetime import datetime

class YardScheme(BaseModel):

    plate: str = "TAV8C99"

class YardSearchScheme(BaseModel):  
    
    plate: str

class YardViewScheme(BaseModel):
    
    plate: str = "TAV8C99"
    model: str = "Moto"
    color: str = "Preta"
    checkin_date: datetime

class YardListScheme(BaseModel):

    yard: List[YardViewScheme]


class YardRemoveScheme(BaseModel):

    plate: str
    message: str

def veicle_info(plate, model, color, checkin_date):
    
    return {
         "plate": plate,
         "model": model,
         "color": color,
         "checkin_date": checkin_date
    }

