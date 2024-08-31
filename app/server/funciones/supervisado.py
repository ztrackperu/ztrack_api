import json
from server.database import collection ,collectionTotal ,conexion_externa
from bson import regex
from datetime import datetime,timedelta
import mysql.connector


def bd_gene(imei):
    fet =datetime.now()
    #part = fet.strftime('%d_%m_%Y')
    part = fet.strftime('_%m_%Y')
    colect ="D_"+imei+part
    return colect

async def analisis_supervisado_ok():
    data_collection = collection("supervisado")
    encontrado = await data_collection.find_one({"estado":1},{"_id":0})
    mensaje = "SIN CONTROL SUPERVISADO"
    hora_actual = datetime.now()
    #quitar 20 minutos a hora actual para validar
    fecha_modificada = hora_actual - timedelta(minutes=20)
    if encontrado :
        print(encontrado)      
        consulta_mysql =[]
        #pedir ultimos datos con esas carcteristicas
        cnx = mysql.connector.connect(
            host= "localhost",
            user= "ztrack2023",
            passwd= "lpmp2018",
            database="zgroupztrack"
        )
        curB = cnx.cursor()
        consulta_J = (
            "SELECT * FROM contenedores WHERE telemetria_id = %s"
        )
        curB.execute(consulta_J, (14872,))
        for data in curB :
            consulta_mysql.append(data)
            #print(data[0])
        obj_vali ={
            "menbrete":consulta_mysql[0][4],
            "power_state":consulta_mysql[0][53],
            "set_point_co2":consulta_mysql[0][61],
            "sp_ethyleno":consulta_mysql[0][79],
            "inyeccion_hora":consulta_mysql[0][77],
            "humidity_set_point":consulta_mysql[0][56],
            "set_point":consulta_mysql[0][10],
            "avl":consulta_mysql[0][27],
            "controlling_mode":consulta_mysql[0][54],
            "fresh_air_mode":consulta_mysql[0][57],
            "ultima_conexion": consulta_mysql[0][13],
        }
        #notificacion = await comandos_collection.insert_one(comando_json)

        curB.close()
        cnx.close()
        if(fecha_modificada>obj_vali['ultima_conexion']):
            mensaje_hora ="SE HA PERIDO CONEXION MAS DE 20 MINUTOS , NO EJCUTAR COMANDOS "
        else:
            mensaje_hora ="CONEXION ESTABLE "

        print("--------------------")
        print(mensaje_hora)
        print("--------------------")



        
        mensaje = obj_vali
        print("--------------------")
        print("sobre le dato validado actual")
        print(obj_vali['sp_ethyleno'])
        print("--------------------")
        print("sobre el control supervisado")
        print(encontrado['sp_etileno'])
        print("--------------------")     
        if(float(encontrado['sp_etileno'])==float(obj_vali['sp_ethyleno'])):
            val ="SONIGUALES NO HACER ACCIONES"
        else :
            val = "PROBLEMAS ENVIAR COMANDO PARA REGULIZAR"

        print(val)

    return mensaje


async def analisis_supervisado():
    data_collection = collection("supervisado")
    comandos_collection = collection(bd_gene("control"))

    encontrado = await data_collection.find_one({"estado":1},{"_id":0})
    if encontrado :
        print(encontrado)      
        consulta_mysql =[]
        #pedir ultimos datos con esas carcteristicas
        cnx = mysql.connector.connect(
            host= "localhost",
            user= "ztrack2023",
            passwd= "lpmp2018",
            database="zgroupztrack"
        )
        curB = cnx.cursor()
        consulta_J = (
            "SELECT * FROM contenedores WHERE telemetria_id = %s"
        )
        curB.execute(consulta_J, (14872,))
        for data in curB :
            consulta_mysql.append(data)
            #print(data[0])
        obj_vali ={
            "menbrete":consulta_mysql[0][4],
            "power_state":consulta_mysql[0][53],
            "set_point_co2":consulta_mysql[0][61],
            "sp_ethyleno":consulta_mysql[0][79],
            "inyeccion_hora":consulta_mysql[0][77],
            "humidity_set_point":consulta_mysql[0][56],
            "set_point":consulta_mysql[0][10],
            "avl":consulta_mysql[0][27],
            "controlling_mode":consulta_mysql[0][54],
            "fresh_air_mode":consulta_mysql[0][57],
        }
        #notificacion = await comandos_collection.insert_one(comando_json)

        curB.close()
        cnx.close()

        if(encontrado['estado_proceso']==0):
            #analizar que todo los parametrso de homogenizacion esten listos 
            if(obj_vali['set_point']==1) :
                if(encontrado['temperatura_homogenizacion']==obj_vali['set_point']) :
                    if(encontrado['humedad_homogenizacion']==obj_vali['humidity_set_point']) :
                        #actualizar proceso a 1 
                        updated_notificacion = await data_collection.update_one(
                        {"id": encontrado['id']
                        }, {"$set": {"estado_proceso":1}}
                        )
                        print("parametros de homogenizacion validados")
                    else:
                        #enviar comando de humedad de no existir
                        buscar_comando = await comandos_collection.find_one({"tipo": 6, "estado":3,"user":"jhonvena"},{"_id":0})
                        if buscar_comando  :
                            # no hacer nada ,esperar a que se termine
                            print("esperamos que se ejecute la humedad")
                        else :
                            #ingresar comando de humedad 
                            #humedad_homogenizacion
                            comando_json = {
                                "imei": "866782048942516",
                                "estado": 3,
                                "comando": "Trama_Writeout(4,"+encontrado['humedad_homogenizacion']+",100)",
                                "evento": "change order for humidity ",
                                "user": "jhonvena",
                                "receta": encontrado['id'],
                                "tipo": 6,
                                "dato": encontrado['humedad_homogenizacion']
                            }
                            notificacion = await comandos_collection.insert_one(comando_json)

                else :
                    #enviar comando de humedad de no existir
                    buscar_comando = await comandos_collection.find_one({"tipo": 7, "estado":3,"user":"jhonvena"},{"_id":0})
                    if buscar_comando  :
                        # no hacer nada ,esperar a que se termine
                        print("esperamos que se ejecute la temperatura")
                    else :
                        #ingresar comando de humedad 
                        #humedad_homogenizacion
                        comando_json = {
                            "imei": "866782048942516",
                            "estado": 3,
                            "comando": "Trama_Writeout(0,"+encontrado['temperatura_homogenizacion']+",100)",
                            "evento": "change order for temperature",
                            "user": "jhonvena",
                            "receta": encontrado['id'],
                            "tipo": 7,
                            "dato": encontrado['temperatura_homogenizacion']
                        }
                        notificacion = await comandos_collection.insert_one(comando_json)

            else :
                #enviar comando de humedad de no existir
                buscar_comando = await comandos_collection.find_one({"tipo": 1, "estado":3,"user":"jhonvena"},{"_id":0})
                if buscar_comando  :
                    # no hacer nada ,esperar a que se termine
                    print("esperamos que se ejecute el encendido")
                else :
                    #ingresar comando de humedad 
                    #humedad_homogenizacion
                    comando_json = {
                        "imei": "866782048942516",
                        "estado": 3,
                        "comando": "Trama_Writeout(29,1,1)",
                        "evento": "change order for temperature",
                        "user": "jhonvena",
                        "receta": encontrado['id'],
                        "tipo": 1,
                        "dato": 1
                    }
                    notificacion = await comandos_collection.insert_one(comando_json)



        return encontrado
    else :
        return 0




async def GuardarSupervisado(ztrack_data: dict) -> dict:
    #dat = ztrack_data['fecha']
    #print(ztrack_data)
    data_collection = collection("supervisado")
    #fet =datetime.now()
    #ztrack_data['fecha_creacion'] = fet
    #primero consultar si ya existe un comando pendiente 

    traer_id = []
    ids_collection = collection("ids")
    async for notificacion in ids_collection.find({"id":1},{"_id":0}):
        print(notificacion)
        traer_id.append(notificacion)
    id_supervisado =  traer_id[0]['supervisado_id'] +1 if len(traer_id)!=0 else 1

    encontrado = await data_collection.find_one({"estado":1},{"_id":0})
    if encontrado :
        return 0
    ztrack_data['id']=id_supervisado
    notificacion = await data_collection.insert_one(ztrack_data)
    updated_ids = await ids_collection.update_one(
            {"id": 1}, {"$set": {"supervisado_id":id_supervisado}}
        )
    new_notificacion = await data_collection.find_one({"_id": notificacion.inserted_id},{"_id":0})
    return new_notificacion

async def EditarSupervisado(id: int, data: dict) -> dict:
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
async def traer_Supervisados():
    notificacions = []
    notificacion_collection = collection("procesos")
    async for notificacion in notificacion_collection.find({},{"_id":0}):
        #print(notificacion)
        notificacions.append(notificacion)
    return notificacions

async def buscar_supervisado(id: int) -> dict:
    #print(id)
    #importante convertir a int cunado se busca a un dato por numero
    notificacion_collection = collection("procesos")
    notificacion = await notificacion_collection.find_one({"id": int(id),"estado":1},{"_id":0})
    #print(notificacion)
    if notificacion:
        return notificacion
    
# Eliminar un notificacion de la base de datos
async def delete_supervisado(id: int):
    notificacion_collection = collection("procesos")

    updated_notificacion = await notificacion_collection.update_one(
            {"id": id}, {"$set": {"estado":0}}
        )
    if updated_notificacion:
            return True
    return False


