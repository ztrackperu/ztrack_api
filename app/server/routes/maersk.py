from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.maersk import (
    Guardar_Datos,
    retrieve_datos,
    procesar_maersk,
    grafica_generador,
    procesar_tabla_datos,
    live_generador,
    empresa,
    config,
    procesar_grafico_datos,
    
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

@router.get("/livegenerador", response_description="Datos recuperados")
async def get_notificacions():
    notificacions = await live_generador()
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
    new_notificacion = await procesar_grafico_datos(notificacion)
    return ResponseModel(new_notificacion, "ok")
   #return paginate(new_notificacion)

@router.post("/DatosTabla/", response_description="Datos de los notificacion agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def pedir_tabla_generador(notificacion: SolicitudGeneradorSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    #print(notificacion)
    #enviar a la funcion añadir  
    #print ("desde r")
    new_notificacion = await procesar_tabla_datos(notificacion)
    return ResponseModel(new_notificacion, "ok")
   #return paginate(new_notificacion)


@router.get("/datos/empresa/{id}", response_description="Datos de la notificacion recuperados")
async def get_empresa_data(id: int):
    notificacion = await empresa(id)
    if notificacion:
        return ResponseModel(notificacion, "Datos de los generadores recuperado exitosamente")
    return ErrorResponseModel("Ocurrió un error.", 404, "notificacion doesn't exist.")

@router.get("/datos/config/{id}", response_description="Datos de la notificacion recuperados")
async def get_config_data(id: int):
    notificacion = await config(id)
    if notificacion:
        return ResponseModel(notificacion, "Datos del generador recuperado exitosamente")
    return ErrorResponseModel("Ocurrió un error.", 404, "notificacion doesn't exist.")