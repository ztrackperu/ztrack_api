from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.starcool import (
    procesar_nestle,
      
)
#Aqui importamos el modelo necesario para la clase 
from server.models.starcool import (
    ErrorResponseModel,
    ResponseModel
)
router = APIRouter()

@router.get("/", response_description="Datos recuperados")
async def get_nestles():
    notificacions = await procesar_nestle()
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")



