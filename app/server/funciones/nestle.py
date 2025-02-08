import json
from server.database import collection ,collectionTotal
from bson import regex
from datetime import datetime,timedelta

import requests


def homologar_temperatura(dato):
    if dato :
        retorno1 = dato if -50 < dato <140 else None
    else : 
        return None
    return retorno1

async def procesar_nestle() :
    notificacions = []

    # La URL de la API que deseas consumir
    url = "http://161.132.206.104:9010/contenedores/ListaDispositivoEmpresa/70"

    # Realizar una solicitud GET para obtener datos
    response = requests.get(url)

    # Comprobar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Convertir la respuesta en formato JSON
        data = response.json()
        data =data['data']
        #print(data['data'])
        # Imprimir los datos obtenidos
        for dispositivo in data:
            
            #buscar dato en la collecion nestle_general 
            nestle_collection = collection('nestle_general')
            dispositivo_encontrado = await nestle_collection.find_one({"Dispositivo": dispositivo['nombre_contenedor'],"estado":1},{"_id":0})
            if dispositivo_encontrado :
                #actualizar estructura 
                #print("*********************")
                #print(dispositivo_encontrado)
                #print("*********************")
                if dispositivo_encontrado['UltimaConexion']!=dispositivo['ultima_fecha'] : 
                    #if len(dispositivo_encontrado['Retorno']) >= 60:
                        #dispositivo_encontrado['Retorno'].pop(0)
                        #dispositivo_encontrado['Suministro'].pop(0)
                        #dispositivo_encontrado['Evaporador'].pop(0)
                        #dispositivo_encontrado['SetPoint'].pop(0)
                        #dispositivo_encontrado['Compresor'].pop(0)
                        #dispositivo_encontrado['fechas'].pop(0)

                    AgregarDispositivo = await nestle_collection.update_one(
                        {"Dispositivo" : dispositivo['nombre_contenedor']},
                        {
                            "$set": {
                                "Descripcion":dispositivo['descripcionC'],
                                "UltimaConexion":dispositivo['ultima_fecha'],
                                "PowerState":dispositivo['power_state'],
                            },
                            "$push":{
                                "Retorno":{
                                    "$each" : [homologar_temperatura(dispositivo['return_air'])],
                                    "$slice": -60
                                },                               
                                "Suministro":{
                                    "$each" :[homologar_temperatura(dispositivo['temp_supply_1'])],
                                    "$slice": -60
                                },
                                "Evaporador":{
                                    "$each" : [homologar_temperatura(dispositivo['evaporation_coil'])],
                                    "$slice": -60
                                },
                                "SetPoint":{
                                    "$each" :[homologar_temperatura(dispositivo['set_point'])],
                                    "$slice": -60
                                },
                                "Compresor":{
                                    "$each" :[homologar_temperatura(dispositivo['compress_coil_1'])],
                                    "$slice": -60
                                },
                                "fechas":{
                                    "$each" :[dispositivo['ultima_fecha']],
                                    "$slice": -60
                                }      
                            }
                        }
                    )

            else : 
                body = {
                    "Dispositivo" : dispositivo['nombre_contenedor'] ,
                    "estado" :1,
                    "Descripcion":dispositivo['descripcionC'],
                    "UltimaConexion":dispositivo['ultima_fecha'],
                    "PowerState":dispositivo['power_state'],
                    "Retorno":[homologar_temperatura(dispositivo['return_air'])],
                    "Suministro":[homologar_temperatura(dispositivo['temp_supply_1'])],
                    "Evaporador":[homologar_temperatura(dispositivo['evaporation_coil'])],
                    "SetPoint":[homologar_temperatura(dispositivo['set_point'])],
                    "Compresor":[homologar_temperatura(dispositivo['compress_coil_1'])],
                    "fechas":[dispositivo['ultima_fecha']]
                }
                AgregarDispositivo = await nestle_collection.insert_one(body)
       
    else:
        print(f"Error al consumir la API. Código de estado: {response.status_code}")
    return "PROCESADO OKEY "




def bd_gene(imei):
    fet =datetime.now()
    #part = fet.strftime('%d_%m_%Y')
    part = fet.strftime('_%m_%Y')
    colect ="S_"+imei+part
    return colect
 
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









