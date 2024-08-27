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

async def analisis_proceso():
    data_collection = collection("procesos")
    encontrado = await data_collection.find_one({"estado":1},{"_id":0})
    if encontrado :
        print(encontrado)
    return 0




async def GuardarProceso(ztrack_data: dict) -> dict:
    #dat = ztrack_data['fecha']
    #print(ztrack_data)
    data_collection = collection("procesos")
    #fet =datetime.now()
    #ztrack_data['fecha_creacion'] = fet
    #primero consultar si ya existe un comando pendiente 

    traer_id = []
    ids_collection = collection("ids")
    async for notificacion in ids_collection.find({"id":1},{"_id":0}):
        print(notificacion)
        traer_id.append(notificacion)
    id_proceso =  traer_id[0]['proceso_id'] +1 if len(traer_id)!=0 else 1

    encontrado = await data_collection.find_one({"estado":1},{"_id":0})
    if encontrado :
        return 0
    ztrack_data['id']=id_proceso
    notificacion = await data_collection.insert_one(ztrack_data)
    updated_ids = await ids_collection.update_one(
            {"id": 1}, {"$set": {"receta_id":id_proceso}}
        )
    new_notificacion = await data_collection.find_one({"_id": notificacion.inserted_id},{"_id":0})
    return new_notificacion

async def EditarProceso(id: int, data: dict) -> dict:
    if len(data) < 1:
        return False
    notificacion_collection = collection("procesos")
    notificacion = await notificacion_collection.find_one({"id": id})
    data["id"]=id
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
async def traer_procesos():
    notificacions = []
    notificacion_collection = collection("procesos")
    async for notificacion in notificacion_collection.find({},{"_id":0}):
        #print(notificacion)
        notificacions.append(notificacion)
    return notificacions

async def buscar_proceso(id: int) -> dict:
    #print(id)
    #importante convertir a int cunado se busca a un dato por numero
    notificacion_collection = collection("procesos")
    notificacion = await notificacion_collection.find_one({"id": int(id),"estado":1},{"_id":0})
    #print(notificacion)
    if notificacion:
        return notificacion
    
# Eliminar un notificacion de la base de datos
async def delete_proceso(id: int):
    notificacion_collection = collection("procesos")

    updated_notificacion = await notificacion_collection.update_one(
            {"id": id}, {"$set": {"estado":0}}
        )
    if updated_notificacion:
            return True
    return False


