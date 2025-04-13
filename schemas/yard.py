from pydantic import BaseModel
from typing import Optional, List
from model.veicle import Veicle
from model.yard import Yard
from datetime import datetime, timedelta

class YardScheme(BaseModel):

    plate: str = "TAV8C99"

class YardSearchScheme(BaseModel):  
    
    plate: str

class YardViewScheme(BaseModel):
    
    plate: str = "TAV8C99"
    model: str = "Moto"
    color: str = "Preta"
    checkin_date: datetime
    elapsed_time : int = 0

class YardListScheme(BaseModel):

    yard: List[YardViewScheme]


class YardRemoveScheme(BaseModel):

    plate: str
    message: str

"""Metodo para calcular o tempo que o carro passou no estacionamento. O valor retornado é em segundos."""

def elapsed_time(checkin_date):
    timedelta = datetime.now() - checkin_date
    return int(timedelta.total_seconds())

"""Método padrão para retorno de veículo."""

def veicle_info(plate, model, color, checkin_date, elapsed_time):
    
    return {
         "plate": plate,
         "model": model,
         "color": color,
         "checkin_date": checkin_date,
         "elapsed_time": elapsed_time,
    }

