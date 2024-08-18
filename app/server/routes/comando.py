from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.comando import (
    GuardarComandos,
    RetrieveComandos,
    ProcesarData,
    GuardarComandos_libre,
)
#Aqui importamos el modelo necesario para la clase 
from server.models.comando import (
    ErrorResponseModel,
    ResponseModel,
    ComandoSchema,
    
)
router = APIRouter()

@router.post("/", response_description="Datos agregados a la base de datos.")
async def add_comando(datos: ComandoSchema = Body(...)):
    datos = jsonable_encoder(datos)   
    new_notificacion = await GuardarComandos(datos)
    print("*******")
    print(new_notificacion)
    print("*******")

    return new_notificacion
@router.post("/libre", response_description="Datos agregados a la base de datos.")
async def add_comando_2(datos: ComandoSchema = Body(...)):
    datos = jsonable_encoder(datos)   
    new_notificacion = await GuardarComandos_libre(datos)
    print("*******")
    print(new_notificacion)
    print("*******")

    return new_notificacion

@router.get("/buscar/{imei}", response_description="Datos recuperados")
async def get_comandos(imei:str):
    notificacions = await RetrieveComandos(imei)
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

#secuencua para homologara datos a la plataforma ztrack
@router.get("/Homologar/", response_description="Datos procesados")
async def procesar_comandos():
    notificacions = await ProcesarData()
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta xx")

