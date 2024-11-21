import json
from server.database import collection ,collectionTotal
from bson import regex
from datetime import datetime,timedelta
from fastapi_pagination.ext.motor import paginate
import mysql.connector


def bd_gene(imei):
    fet =datetime.now()
    #part = fet.strftime('%d_%m_%Y')
    part = fet.strftime('_%m_%Y')
    colect ="G_"+imei+part
    return colect
 

async def procesar_maersk():
    fet =datetime.now()
    imei = "863576046753492"
    #aqui capturamos al coleccion y procesamos los datos 
    data_collection = collection(bd_gene(imei))
    #pasamos todo a nueva base de datos D_MAERSK_11_2024
    proceso_collection =collection(bd_gene("MAERSK"))
    notificacions=[]
    cont_config = 0 
    cont_on =0
    cont_off =0
    cont_fail =0
    async for notificacion in data_collection.find({"estado":1},{"_id":0}).sort({"fecha":1}):
        if notificacion['d01'] and  notificacion['d02'] and  notificacion['d03'] and  notificacion['d04'] and  notificacion['i'] :
            cont_config+=1
        elif  notificacion['d00'] and  notificacion['d09'] and  notificacion['i'] :
            cont_on+=1
        elif notificacion['gps'] and notificacion['d00']==False and  notificacion['d09']==False and notificacion['d01']==False and  notificacion['d02']==False and  notificacion['d03']==False and  notificacion['d04']==False and  notificacion['i'] : 
            cont_off+=1
        else :
            cont_fail=1

        print(notificacion)
        notificacions.append(notificacion)
    return  [cont_config ,cont_on ,cont_off , cont_fail ,notificacions]










async def Guardar_Datos(ztrack_data: dict) -> dict:
    #dat = ztrack_data['fecha']
    fet =datetime.now()
    
    #part = fet.strftime('%d_%m_%Y')
    #colect ="Datos_"+part
    #print(colect)
    ztrack_data['fecha'] = fet
    #print(ztrack_data)
    comando ="sin comandos pendientes"
    Hay_dispositivo=""
    #COLECCION ESPECIFICA PARA DISPOSITIVO
    data_collection = collection(bd_gene(ztrack_data['i']))
    #COLECCION PARA TODOS LOS DISPOSITIVOS
    dispositivos_collection = collection(bd_gene('dispositivos'))
    #COLECCION ESPECIFICA PARA EL CONTROL
    control_collection = collection(bd_gene("control"))
    #AQUI SE GUARDA LA TRAMA 

    notificacion = await data_collection.insert_one(ztrack_data)

    new_notificacion = await data_collection.find_one({"_id": notificacion.inserted_id},{"_id":0})
    #Verificar que exista el dispositivo en el registro
    dispositivo_encontrado = await dispositivos_collection.find_one({"imei": ztrack_data['i'],"estado":1},{"_id":0})
    
    if dispositivo_encontrado is not None:
        try:
            Hay_dispositivo= dispositivo_encontrado['imei'] 
            print("Elemento encontrado")
        except ValueError:
            print("NO SE ENCONTRO CONTROL")
    verificar_dispositivo = await dispositivos_collection.update_one({"imei": ztrack_data['i'],"estado":1},{"$set":{"ultimo_dato":fet}}) if Hay_dispositivo else await dispositivos_collection.insert_one({"imei":ztrack_data['i'],"estado":1,"fecha":fet ,"tipo":"generador"})
    control_encontrado =    await control_collection.find_one({"imei": ztrack_data['i'],"estado":1},{"_id":0})
    #if control_encontrado['comando'] :
    if control_encontrado :
        veces_control = control_encontrado['estado']-1 if control_encontrado['comando'] else 0
        comando = control_encontrado['comando']
        actualizar_comando = await control_collection.update_one({"imei": ztrack_data['i'],"estado":1},{"$set":{"estado": veces_control,"status":2,"fecha_ejecucion":fet}})
    return comando

async def retrieve_datos(imei: str):
    notificacions = []
    data_collection = collection(bd_gene(imei))
    async for notificacion in data_collection.find({"estado":1},{"_id":0}):
        #print(notificacion)
        notificacions.append(notificacion)
    return notificacions

async def retrieve_datos_e():
    notificacions = []
    data_collection = collection(bd_gene())
    async for notificacion in data_collection.find({"estado":1},{"_id":0}):
        #print(notificacion)
        notificacions.append(notificacion)
    return notificacions









