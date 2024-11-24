from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.maersk import (
    Guardar_Datos,
    retrieve_datos,
    procesar_maersk,
    grafica_generador,
    
)

#Aqui importamos el modelo necesario para la clase 
from server.models.maersk import (
    ErrorResponseModel,
    ResponseModel,
    SolicitudGeneradorSchema,
)

router = APIRouter()

@router.get("/pre", response_description="Datos recuperados")
async def get_notificacions():
    notificacions = await procesar_maersk()
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.post("/DatosGrafica/", response_description="Datos de los notificacion agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def pedir_grafica_generador(notificacion: SolicitudGeneradorSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    #print(notificacion)
    #enviar a la funcion añadir  
    #print ("desde r")
    new_notificacion = await grafica_generador(notificacion)
    return ResponseModel(new_notificacion, "ok")
   #return paginate(new_notificacion)

