from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.generador import (
    Guardar_Datos,
    retrieve_datos,
    
)
#Aqui importamos el modelo necesario para la clase 
from server.models.generador import (
    ErrorResponseModel,
    ResponseModel,
    GeneradorSchema,
)
router = APIRouter()

@router.post("/", response_description="Datos agregados a la base de datos.")
async def add_data(datos: GeneradorSchema = Body(...)):
    datos = jsonable_encoder(datos)   
    new_notificacion = await Guardar_Datos(datos)
    print(new_notificacion)
    text = "todo esta bien,todo esta bien,todo esta bien no tengo idea de lo que estoy haciendo"
    text =text +" Hay veces que pienso que tomar una cerveza es pecado , por lo que me todo dos para estar seguro de pecar bien :) 123"
    text = "Trama_Readout(int TipoTrama)"
    text = "Trama_Readout(5)"
    #return text 
    return new_notificacion
    #return ResponseModel(new_notificacion, "ok")

@router.get("/{imei}", response_description="Datos recuperados")
async def get_notificacions(imei:str):
    notificacions = await retrieve_datos(imei)
    if notificacions:
        return ResponseModel(notificacions, "Datos  recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")



