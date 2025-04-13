from sqlalchemy import Column, Integer, Float, DateTime, Date
from datetime import datetime
from typing import Union

from  model import Base

"""Classe de receita"""

class Income(Base):
    __tablename__= 'income'

    income_date = Column("pk_income" ,Date, primary_key= True)
    cash = Column(Float)
    pix = Column(Float)
    debit = Column(Float)
    credit = Column(Float)

    def __init__(self, cash, pix, debit, credit, income_date:Union[DateTime, None] = None):

        self.cash = cash
        self.pix = pix
        self.debit = debit
        self.credit = credit

        if income_date:
            self.income_date = income_date

    



