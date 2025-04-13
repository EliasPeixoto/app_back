from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from zoneinfo import ZoneInfo

from  model import Base

"""Relação do pátio, é nesta tabela que a maior parte dos procedimentos irá ocorrer"""

class Yard(Base):
    __tablename__ = "yard"

    id = Column("pk_yard", Integer, primary_key=True)
    checkin_date = Column(DateTime, default=datetime.now())
    plate = Column(String(7), ForeignKey("veicle.pk_veicle"), unique= True)

    veicle_data = relationship("Veicle", back_populates="yard")

    def __init__(self, plate:str, checkin_date:Union[DateTime,None] = None):

        self.plate = plate
    
        if checkin_date:
              self.checkin_date = checkin_date  