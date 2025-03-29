from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

class Veicle(Base):
    __tablename__='veicle'

    id = Column("pk_veicle", Integer, primary_key=True)
    plate = Column(String(7), unique=True)
    model = Column(String(140))
    color = Column(String(140))
    checkin_date = Column(DateTime, default=datetime.now())
    checkout_date = Column(DateTime)
    payment_method = Column(String(140))
    value = Column(Float)

    def __init__ (self,plate:str,model:str,color:str,checkin_date:Union[DateTime, None] = None):
    
        self.plate = plate
        self.model = model
        self.color = color

        if checkin_date:
            self.checkin_date = checkin_date