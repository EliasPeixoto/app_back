from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from logger import logger
from model import Session, Veicle
from schemas import *
from flask_cors import CORS

info = Info(title="Estacionator", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")
veicle_tag = Tag(name="Veículo", description="Adição, visualização e remoção de um veiculo na base de dados")

@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')

@app.post('/veicle', tags=[veicle_tag],
          responses={"200": VeicleViewScheme,"409":ErrorScheme,"400": ErrorScheme})
def checkin_veicle(form: VeicleScheme):

    veicle = Veicle(
        plate = form.plate,
        model = form.model,
        color = form.color)
    logger.debug(f"Adicionando veiculo de placa: '{veicle.plate}'")
    try:
        session = Session()

        session.add(veicle)

        session.commit()
        logger.debug(f"O veiculo de placa '{veicle.plate}' foi adicionado com sucesso.")
        return show_veicle(veicle), 200

    except IntegrityError as e:

        error_msg = "O veiculo já está cadastrado :/"
        logger.warning(f"Erro ao adicionar o veiculo de placa '{veicle.plate}', '{error_msg}'")
        return {"message": error_msg}, 409
    
    except Exception as e:

        error_msg = "Não foi possível cadastrar o veículo :/"
        logger.warning(f"Erro ao cadastrar o veículo de placa '{veicle.plate}', '{error_msg}'")
        return {"message":error_msg}, 400
    
@app.get('/veicles', tags=[veicle_tag],
         responses ={"200":VeicleListScheme, "404": ErrorScheme})
def get_veicles():
    logger.debug(f"Obtendo veículos")

    session = Session()

    veicles = session.query(Veicle).all()

    if not veicles:
        return {"veicles": []}, 200
    else:
        logger.debug(f"%d veiculos foram encontrados" % len(veicles))
        print(veicles)
        return show_veicles(veicles), 200
    
@app.get('/veicle', tags =[veicle_tag],
         responses={"200": VeicleViewScheme, "404": ErrorScheme})
def get_veicle(query:VeicleSearchScheme):

    veicle_plate = query.plate
    logger.debug(f"Obtendo dados sobre o veiculo de placa #{veicle_plate}")
    
    session = Session()

    veicle = session.query(Veicle).filter(Veicle.plate == veicle_plate).first()
    
    if not veicle:

        error_msg = "Veiculo não encontrado :/"
        logger.warning(f"Erro ao buscar o veiculo de placa '{veicle_plate}','{error_msg}'")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Veiculo de placa '{veicle.plate}' encontrado!")
        return show_veicle(veicle), 200
    
@app.delete('/veicle', tags=[veicle_tag],
            responses={"200": VeicleCheckoutScheme, "404": ErrorScheme})
def  checkout_veicle (query: VeicleSearchScheme):

    veicle_plate = unquote(unquote(query.plate))
    print(veicle_plate)
    logger.debug(f"Removendo o veiculo de placa #'{veicle_plate}'")

    session = Session()

    count = session.query(Veicle).filter(Veicle.plate == veicle_plate).delete()
    session.commit()

    if count:
        
        logger.debug(f"O veiculo de placa #{veicle_plate} foi removido")
        return {"message": "Veiculo removido", "id" : veicle_plate}
    else:

        error_msg = "O veiculo não foi encontrado :/"
        logger.warning(f"Erro ao reemover o veiculo de placa #'{veicle_plate}', {error_msg}")
        return {"message": error_msg}, 404