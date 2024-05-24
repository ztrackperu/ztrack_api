from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.datos import (
    Guardar_Datos,
    retrieve_datos,
)
#Aqui importamos el modelo necesario para la clase 
from server.models.datos import (
    ErrorResponseModel,
    ResponseModel,
    DatosSchema,
)
router = APIRouter()

@router.post("/", response_description="Datos agregados a la base de datos.")
async def add_data(datos: DatosSchema = Body(...)):
    datos = jsonable_encoder(datos)   
    new_notificacion = await Guardar_Datos(datos)
    print(new_notificacion)
    return ResponseModel(new_notificacion, "ok")

@router.get("/", response_description="Datos recuperados")
async def get_notificacions():
    notificacions = await retrieve_datos()
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

