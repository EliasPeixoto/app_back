from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from logger import logger
from model import Session, Veicle, Yard, Income
from schemas import *
from flask_cors import CORS

info = Info(title="Estacionator", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")
veicle_tag = Tag(name="Veículo", description="Cadastro de veículos no banco de dados")
yard_tag = Tag(name="Pátio", description="Adição, remoção e visualização dos veiculos no pátio")
income_tag = Tag(name="Receita", description="Adição dos valores na receita")

@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')

@app.post('/yard', tags=[yard_tag, veicle_tag],
          responses={"200": YardViewScheme, "409": ErrorScheme, "400": ErrorScheme})
def add_veicle(form: VeicleScheme):

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
            plate = form.plate
            )
        session.add(park)
        session.commit()
       
        return veicle_info(form.plate,form.model, form.color,park.checkin_date)
    
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

    session = Session()
    yard_list = session.query(Yard).join(Veicle)
    if not yard_list:
        return {"yard": []}, 200 
    else:
        veicles = []
        for item in yard_list:
            veicles.append(veicle_info(item.plate,item.veicle_data.model,item.veicle_data.color,item.checkin_date))    
        return {"yard": veicles}, 200
    
