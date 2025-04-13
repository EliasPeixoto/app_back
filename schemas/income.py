from pydantic import BaseModel
from typing import Optional, List
from model.veicle import Veicle
from model.yard import Yard
from model.income import Income
from datetime import datetime

class IncomeViewScheme(BaseModel):

    cash: float = 0
    pix: float = 0
    debit: float = 0
    credit: float = 0

class PriceViewScheme(BaseModel):

    price: float


"""Método de retorno da receita"""

def income_info(cash, pix, debit, credit):

    return{
        "cash": cash,
        "pix": pix,
        "debit": debit,
        "credit": credit,
    }

"""Método de cálculo do preço do estacionamento. Cada meia hora, adiciona 3 reais no preço. Você pode alterar essas informações para testar a tabela income
de forma mais rápida. Se tirar a divisão por 30 o valor será adicionado a cada minuto."""

def calculate_price(elapsed_time):
    
    price = int((elapsed_time/60)/30)*3
    return {
        "price":price
    }
    
    