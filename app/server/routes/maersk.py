from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.maersk import (
    Guardar_Datos,
    retrieve_datos,
    procesar_maersk,
    
)

#Aqui importamos el modelo necesario para la clase 
from server.models.maersk import (
    ErrorResponseModel,
    ResponseModel,
    #GeneradorSchema,
)

router = APIRouter()

@router.get("/pre", response_description="Datos recuperados")
async def get_notificacions(imei:str):
    notificacions = await retrieve_datos(imei)
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")



