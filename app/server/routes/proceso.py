from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.motor import paginate

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.proceso import (
    GuardarProceso,
    EditarProceso,
    traer_procesos,
    buscar_proceso,
    delete_proceso,
 
)
#Aqui importamos el modelo necesario para la clase 
from server.models.proceso import (
    ErrorResponseModel,
    ResponseModel,
    ProcesoSchema,

)
#aqui se definen las rutas de la API REST
router = APIRouter()

@router.post("/", response_description="Datos de los recetas agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_notificacion_data(notificacion: ProcesoSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    #print(notificacion)
    #enviar a la funcion añadir  
    new_notificacion = await GuardarProceso(notificacion)
    return ResponseModel(new_notificacion, "ok")

@router.get("/", response_description="recetas recuperados")
async def get_notificacions():
    notificacions = await traer_procesos()
    if notificacions:
        return ResponseModel(notificacions, "Datos de las recetas recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")


@router.get("/{id}", response_description="Datos de la recetas recuperados")
async def get_notificacion_data(id: int):
    notificacion = await buscar_proceso(id)
    if notificacion:
        return ResponseModel(notificacion, "Datos de la recetas recuperado exitosamente")
    return ErrorResponseModel("Ocurrió un error.", 404, "notificacion doesn't exist.")


@router.put("/{id}")
async def update_notificacion_data(id: int, req: ProcesoSchema = Body(...)):
    #ANALIZADOR DE ESTRUCTURA req
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_notificacion = await EditarProceso(id, req)
    if updated_notificacion:
        return ResponseModel(
            #"ConceptoOT with ID: {} name update is successful".format(id),
            "ok",
            "recetas  updated successfully",
        )
    return ErrorResponseModel("An error occurred",404,"There was an error updating the recetas data.",)

@router.delete("/{id}", response_description="recetas data deleted from the database")
async def delete_notificacion_data(id: int):
    deleted_notificacion = await delete_proceso(id)
    if deleted_notificacion:
        return ResponseModel(
            "notificacion with ID: {} removed".format(id), "recetas deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "recetas with id {0} doesn't exist".format(id)
    )


