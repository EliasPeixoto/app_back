from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, Date


from logger import logger
from model import Session, Veicle, Yard, Income
from schemas import *
from flask_cors import CORS

from datetime import datetime, date

info = Info(title="Estacionator", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")
veicle_tag = Tag(name="Veículo", description="Cadastro de veículos no banco de dados")
yard_tag = Tag(name="Pátio", description="Adição, remoção e visualização dos veiculos no pátio")
income_tag = Tag(name="Receita", description="Adição dos valores na receita")

@app.get('/', tags=[home_tag])
def home():
   
    """Esta é a minha API para o gerenciamento de um estacionamento"""

    return redirect('/openapi')

@app.post('/yard', tags=[yard_tag, veicle_tag],
          responses={"200": YardViewScheme, "409": ErrorScheme, "400": ErrorScheme})
def add_veicle(form: VeicleScheme):

    """ Adiciona um veículo à base de dados de veículos caso já não esteja lá e também adiciona no patio.
"""

    session = Session()
    query_plate = session.query(Veicle).filter(Veicle.plate == form.plate).first()

    if not query_plate:
            veicle = Veicle(
                plate = form.plate,
                model = form.model,    
                color = form.color)
            session.add(veicle)
    try:
        park = Yard(
            plate = form.plate,
            checkin_date = datetime.now()
            )
        session.add(park)
        session.commit()
       
        return veicle_info(form.plate,form.model, form.color,park.checkin_date,elapsed_time(park.checkin_date)), 200
    
    except IntegrityError:
        error_msg = "Veículo já cadastrado!"
        logger.warning(f"O veículo de placa '{form.plate}' já está no sistema")
        return{"message": error_msg}, 409
    
    except Exception as e:
        error_msg = "Não foi possivel adicionar o veiculo"
        logger.warning(f"Erro ao adicionar o veículo '{form.plate}', {error_msg}")
        return {"message": error_msg}, 400
    
@app.get('/yard', tags=[yard_tag, veicle_tag], 
         responses={"200": YardListScheme, "409": ErrorScheme, "400": ErrorScheme})
def get_yard_list():

    """Retorna a lista de pátio. Este método coleta informações tanto da tabela de pátio quando da tabela de veículos."""

    session = Session()
    yard_list = session.query(Yard).join(Veicle)
    if not yard_list:
        return {"yard": []}, 200 
    else:
        veicles = []
        for item in yard_list:
            veicles.append(veicle_info(item.plate,item.veicle_data.model,item.veicle_data.color,item.checkin_date,elapsed_time(item.checkin_date)))    
        return {"yard": veicles}, 200
    

@app.get('/search_yard', tags=[yard_tag,veicle_tag],
         responses={"200": YardViewScheme, "409": ErrorScheme, "400": ErrorScheme})
def search_yard(query: VeicleSearchScheme):

    """Retorna as informações de um veículo. Este método coleta informações tanto da tabela de pátio quando da tabela de veículos."""

    session = Session()
    veicle = session.query(Yard).join(Veicle).filter(Yard.plate == query.plate).first()
    if not veicle:
        return {"O veículo não está no patio"}, 200
    else:
        return veicle_info(veicle.plate, veicle.veicle_data.model, veicle.veicle_data.color, veicle.checkin_date, elapsed_time(veicle.checkin_date)), 200

@app.get('/income', tags=[income_tag],
          responses={"200" : IncomeViewScheme , "409" : ErrorScheme , "400" : ErrorScheme})
def get_income():

    """Retorna o valor da receita do dia. Caso não existir receita no banco de dados, o código retorna valores padrão."""

    session = Session()
    today = date.today()
    income = session.query(Income).filter(Income.income_date == today).with_for_update().first()
    if not income:
        return income_info(0,0,0,0), 200
    else:
        return income_info(income.cash, income.pix, income.debit, income.credit),200


@app.post('/income', tags=[income_tag],
          responses= {"200" : IncomeViewScheme, "409" : ErrorScheme, "400" : ErrorScheme })
def update_income(form: IncomeViewScheme):

    """Metodo que atualiza o banco de dados em relação a novas receitas. Caso seja a primeira receita, ele preencherá os outros valores com zero."""

    session = Session()
    today = date.today()
    income = session.query(Income).filter(Income.income_date == today).first()
    if income:
        income.cash += form.cash
        income.pix += form.pix
        income.debit += form.debit
        income.credit += form.credit
        session.merge(income)
        session.commit()
        return income_info (income.cash, income.pix, income.debit, income.credit)
    else:
        new_income = Income(
            income_date = date.today(),
            cash = form.cash,
            pix = form.pix,
            debit = form.debit,
            credit = form.credit
        )
        session.add(new_income)
        session.commit()
        return income_info (new_income.cash, new_income.pix, new_income.debit, new_income.credit)

@app.get("/income_price", tags=[income_tag],
         responses={"200" : PriceViewScheme, "409" : ErrorScheme, "400" : ErrorScheme})
def get_price(query: VeicleSearchScheme):

    """Metodo que retorna o valor do estacionamento para a caixa de checkout"""

    session = Session()
    veicle = session.query(Yard).filter(Yard.plate == query.plate).first()
    
    if not veicle:
        return "", 200
    else:
        return calculate_price(elapsed_time(veicle.checkin_date)), 200
    
@app.delete("/yard", tags=[yard_tag], 
            responses={"200" : YardRemoveScheme, "404" : ErrorScheme})
def remove_veicle(query : VeicleSearchScheme):

    """Método para remover o veículo"""

    session = Session()
    veicle_plate = unquote(unquote(query.plate))
    veicle = session.query(Yard).filter(Yard.plate == query.plate).delete()
    session.commit()

    if veicle:
        return {"message": "O veiculo de placa: " + veicle_plate + " foi removido!"}
    else:
        return {"message": "Não foi possivel remover o veiculo de placa: " + veicle_plate}
    
        
