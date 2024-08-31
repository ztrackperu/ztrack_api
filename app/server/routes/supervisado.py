from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.supervisado import (
    GuardarSupervisado,
    analisis_supervisado_ok,
)
#Aqui importamos el modelo necesario para la clase 
from server.models.supervisado import (
    ErrorResponseModel,
    ResponseModel,
    SupervisadoSchema,
    
)
router = APIRouter()

@router.post("/", response_description="Datos agregados a la base de datos.")
async def add_comando(datos: SupervisadoSchema = Body(...)):
    datos = jsonable_encoder(datos)   
    new_notificacion = await GuardarSupervisado(datos)
    print("*******")
    print(new_notificacion)
    print("*******")

    return new_notificacion

#secuencua para analizar si proceso sigue activo en  la plataforma ztrack
@router.get("/Analizar/", response_description="Datos procesados")
async def procesar_comandos():
    notificacions = await analisis_supervisado_ok()
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta xx")





@router.post("/libre/", response_description="Datos agregados a la base de datos.")
async def add_comando_2(datos: SupervisadoSchema = Body(...)):
    datos = jsonable_encoder(datos)   
    new_notificacion = await GuardarSupervisado(datos)
    print("*******")
    print(new_notificacion)
    print("*******")

    return new_notificacion

@router.post("/super_libre/", response_description="Datos agregados a la base de datos.")
async def add_comando_2(datos: SupervisadoSchema = Body(...)):
    datos = jsonable_encoder(datos)   
    new_notificacion = await GuardarSupervisado(datos)
    print("*******")
    print(new_notificacion)
    print("*******")

    return new_notificacion

@router.get("/buscar/testapi/{imei}", response_description="Datos recuperados")
async def get_comandos_testapi(imei:str):
    notificacions = await GuardarSupervisado(imei)
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/buscar/oficial/{imei}", response_description="Datos recuperados")
async def get_comandos_oficial(imei:str):
    notificacions = await GuardarSupervisado(imei)
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/buscar/{imei}", response_description="Datos recuperados")
async def get_comandos(imei:str):
    notificacions = await GuardarSupervisado(imei)
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

#secuencua para homologara datos a la plataforma ztrack
@router.get("/Homologar/", response_description="Datos procesados")
async def procesar_comandos():
    notificacions = await GuardarSupervisado()
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta xx")

#secuencua para homologara datos a la plataforma ztrack
@router.get("/JhonVena/{imei}", response_description="Datos procesados")
async def procesar_comandos_jhon_vena(imei:str):
    notificacions = await GuardarSupervisado(imei)
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta xx")
