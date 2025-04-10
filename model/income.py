from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from typing import Union

from  model import Base

class Income(Base):
    __tablename__= 'income'

    id = Column("pk_income", Integer, primary_key=True)
    cash = Column(Float)
    pix = Column(Float)
    debit = Column(Float)
    credit = Column(Float)
    date = Column(DateTime, default= datetime.now().date())

    def __init__(self,date:Union[DateTime, None] = None):

        self.cash = 0
        self.pix = 0
        self.debit = 0
        self.credit = 0

        if date:
            self.date = date


