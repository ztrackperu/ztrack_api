from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.comando import (
    GuardarComandos,
    RetrieveComandos,
    ProcesarData,
    GuardarComandos_libre,
    GuardarComandos_super_libre,
    comando_jhon_vena,
    RetrieveComandos_test,
    RetrieveComandos_oficial,
    GuardarComandos_super_libre_supervisado,
    procesar_on_pabecsa,
    procesar_off_pabecsa,
    procesar_off_guardia_civil,
    procesar_on_guardia_civil
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
@router.post("/libre/", response_description="Datos agregados a la base de datos.")
async def add_comando_2(datos: ComandoSchema = Body(...)):
    datos = jsonable_encoder(datos)   
    new_notificacion = await GuardarComandos_libre(datos)
    print("*******")
    print(new_notificacion)
    print("*******")

    return new_notificacion

@router.post("/super_libre/", response_description="Datos agregados a la base de datos.")
async def add_comando_2(datos: ComandoSchema = Body(...)):
    datos = jsonable_encoder(datos)   
    new_notificacion = await GuardarComandos_super_libre(datos)
    print("*******")
    print(new_notificacion)
    print("*******")

    return new_notificacion

@router.get("/buscar/testapi/{imei}", response_description="Datos recuperados")
async def get_comandos_testapi(imei:str):
    notificacions = await RetrieveComandos_test(imei)
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/buscar/oficial/{imei}", response_description="Datos recuperados")
async def get_comandos_oficial(imei:str):
    notificacions = await RetrieveComandos_oficial(imei)
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

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

#secuencua para homologara datos a la plataforma ztrack
@router.get("/Supervisar_Demonio/", response_description="Datos procesados")
async def supervisar():
    notificacions = await GuardarComandos_super_libre_supervisado()
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta xx")

#secuencua para homologara datos a la plataforma ztrack
@router.get("/JhonVena/{imei}", response_description="Datos procesados")
async def procesar_comandos_jhon_vena(imei:str):
    notificacions = await comando_jhon_vena(imei)
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta xx")


#secuencua para homologara datos a la plataforma ztrack
@router.get("/Pabesca_on/", response_description="Datos procesados")
async def procesar_on_comandos():
    notificacions = await procesar_on_pabecsa()
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta xx")

#secuencua para homologara datos a la plataforma ztrack
@router.get("/Pabesca_off/", response_description="Datos procesados")
async def procesar_off_comandos():
    notificacions = await procesar_off_pabecsa()
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta xx")


#secuencua para homologara datos a la plataforma ztrack
@router.get("/Guardia_on/", response_description="Datos procesados")
async def procesar_on_comandos_1():
    notificacions = await procesar_on_guardia_civil()
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta xx")

#secuencua para homologara datos a la plataforma ztrack
@router.get("/Guardia_off/", response_description="Datos procesados")
async def procesar_off_comandos_2():
    notificacions = await procesar_off_guardia_civil()
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta xx")





