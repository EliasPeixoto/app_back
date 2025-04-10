from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from typing import Union

from  model import Base

class Veicle(Base):
    __tablename__= "veicle"

    plate = Column("pk_veicle",String(10), primary_key=True)
    model = Column(String(140))
    color = Column(String(140))

    yard = relationship("Yard", back_populates="veicle_data")

    def __init__ (self,plate:str,model:str,color:str):
    
        self.plate = plate.upper()
        self.model = model.capitalize()
        self.color = color.capitalize()