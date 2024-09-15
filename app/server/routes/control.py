from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.control import (
    GuardarControl,
    RetrieveControls,
    RetrieveControl_oficial,
    Procesar_control_oficial

)
#Aqui importamos el modelo necesario para la clase 
from server.models.control import (
    ErrorResponseModel,
    ResponseModel,
    ControlSchema,
    
)
router = APIRouter()

@router.post("/", response_description="Datos agregados a la base de datos.")
async def add_control(datos: ControlSchema = Body(...)):
    datos = jsonable_encoder(datos)   
    new_notificacion = await GuardarControl(datos)
    print("*******")
    print(new_notificacion)
    print("*******")
    return new_notificacion


@router.get("/buscar/libre/{imei}", response_description="Datos recuperados")
async def get_control_libre(imei:str):
    notificacions = await RetrieveControls(imei)
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/buscar/oficial/{imei}/{user}", response_description="Datos recuperados")
async def get_control_oficial(imei:str,user:str):
    notificacions = await RetrieveControl_oficial(imei,user)
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

