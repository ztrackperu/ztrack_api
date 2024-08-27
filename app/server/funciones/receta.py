import json
from server.database import collection ,collectionTotal ,conexion_externa
from bson import regex
from datetime import datetime,timedelta
#import mysql.connector

def bd_gene(imei):
    fet =datetime.now()
    #part = fet.strftime('%d_%m_%Y')
    part = fet.strftime('_%m_%Y')
    colect ="D_"+imei+part
    return colect

async def GuardarReceta(ztrack_data: dict) -> dict:
    #dat = ztrack_data['fecha']
    #print(ztrack_data)
    data_collection = collection("recetas")
    #fet =datetime.now()
    #ztrack_data['fecha_creacion'] = fet
    #primero consultar si ya existe un comando pendiente 

    traer_id = []
    ids_collection = collection("ids")
    async for notificacion in ids_collection.find({"id":1},{"_id":0}):
        print(notificacion)
        traer_id.append(notificacion)
    id_receta =  traer_id[0].receta_id +1 if len(traer_id)!=0 else 1

    encontrado = await data_collection.find_one({"nombre_receta":ztrack_data['nombre_receta'],"estado":1},{"_id":0})
    if encontrado :
        return 0
    notificacion = await data_collection.insert_one(ztrack_data)
    updated_ids = await ids_collection.update_one(
            {"id": 1}, {"$set": {"receta_id":id_receta}}
        )
    new_notificacion = await data_collection.find_one({"_id": notificacion.inserted_id},{"_id":0})
    return new_notificacion

async def EditarReceta(id: int, data: dict) -> dict:
    if len(data) < 1:
        return False
    notificacion_collection = collection("recetas")
    notificacion = await notificacion_collection.find_one({"id": id})
    if notificacion:
        updated_notificacion = await notificacion_collection.update_one(
            {"id": id}, {"$set": data}
        )
        if updated_notificacion:
            return True
        return False
    
#notificacion_collection = collection("notificaciones")
# crud operation
# Recuperar todos los notificacions presentes en la base de datos.
async def traer_recetas():
    notificacions = []
    notificacion_collection = collection("recetas")
    async for notificacion in notificacion_collection.find({"estado":1},{"_id":0}):
        #print(notificacion)
        notificacions.append(notificacion)
    return notificacions

async def buscar_receta(id: int) -> dict:
    #print(id)
    #importante convertir a int cunado se busca a un dato por numero
    notificacion_collection = collection("recetas")
    notificacion = await notificacion_collection.find_one({"id": int(id),"estado":1},{"_id":0})
    #print(notificacion)
    if notificacion:
        return notificacion
    
# Eliminar un notificacion de la base de datos
async def delete_receta(id: int):
    notificacion_collection = collection("recetas")

    updated_notificacion = await notificacion_collection.update_one(
            {"id": id}, {"$set": {"estado":0}}
        )
    if updated_notificacion:
            return True
    return False


