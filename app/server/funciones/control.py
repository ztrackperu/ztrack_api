import json
from server.database import collection ,collectionTotal ,conexion_externa
from bson import regex
from datetime import datetime,timedelta
import mysql.connector

def formatear_numero(numero):
    # Formatear con dos decimales
    return f"{numero:.2f}"
def bd_gene(imei):
    fet =datetime.now()
    #part = fet.strftime('%d_%m_%Y')
    part = fet.strftime('_%m_%Y')
    colect ="D_"+imei+part
    return colect

#funcion insertar control 
async def GuardarControl(ztrack_data: dict) -> dict:
    #dat = ztrack_data['fecha']
    #print(ztrack_data)
    traer_id = []
    ids_collection = collection("ids")
    async for notificacion in ids_collection.find({"id":1},{"_id":0}):
        print(notificacion)
        traer_id.append(notificacion)
    print(traer_id)
    id_proceso =  traer_id[0]['proceso_id'] +1 if len(traer_id)!=0 else 1
    ahora = datetime.now() 
    dentro_10_minutos = ahora + timedelta(minutes=10)  
    dentro_24_horas = ahora + timedelta(hours=24)
    ztrack_data['id']=id_proceso
    id_comando =  traer_id[0]['comando_id'] +1 if len(traer_id)!=0 else 1

    data_collection = collection(bd_gene("proceso"))
    ztrack_data['fecha_creacion'] = ahora
    ztrack_data['inicio_control'] = dentro_10_minutos
    ztrack_data['fin_control'] = dentro_24_horas
    #MANUAL_RIPE(17.80,90,120,5.00)
    ztrack_data['comando'] = 'MANUAL_RIPE('+str(formatear_numero(ztrack_data['temperatura']))+','+str(ztrack_data['humedad'])+','+str(ztrack_data['etileno'])+','+str(formatear_numero(ztrack_data['co2']))+')'

    #primero consultar si ya existe un comando pendiente 
    encontrado = await data_collection.find_one({"imei":ztrack_data['imei'],"estado":1},{"_id":0})
    if encontrado :
        return 0
    notificacion = await data_collection.insert_one(ztrack_data)

    new_notificacion = await data_collection.find_one({"_id": notificacion.inserted_id},{"_id":0})
    #procesar comando modo ripener directo al inicio
    comando_collection = collection(bd_gene("control"))
    ztrack_comando={
        "imei":ztrack_data['imei'],
        "estado":0,
        "fecha_creacion":ahora ,
        "fecha_ejecucion":None,
        "comando":ztrack_data['comando'],
        "dispositivo":ztrack_data['dispositivo'],
        "evento":"Inicio de proceso de maduracion controlado",
        "user":"ControlSupervisado",
        "receta":ztrack_data['titulo'],
        "tipo":0,
        "status":1,
        "dato":0,
        "id":id_comando
    }
    comando_inicial = await comando_collection.insert_one(ztrack_comando)
    updated_ids = await ids_collection.update_one(
        {"id": 1}, {"$set": {"proceso_id":id_proceso,"comando_id":id_comando}}
    )
    return new_notificacion


#funcion de control cada minuto evalua 

async def RetrieveControls(imei: str):
    notificacions = []
    data_collection = collection(bd_gene("proceso"))
    async for notificacion in data_collection.find({"imei":imei},{"_id":0}).sort({"fecha_creacion":-1}):
        notificacions.append(notificacion)
    return notificacions


async def RetrieveControl_oficial(imei: str,user:str):
    notificacions = []
    data_collection = collection(bd_gene("control"))
    #{user:"jhonvena",$or:[{status:0},{status:2}]}
    async for notificacion in data_collection.find({"imei":imei ,"user":user,"$or":[{"status":1},{"status":2}]},{"_id":0}).sort({"fecha_creacion":-1}):
        notificacions.append(notificacion)
    return notificacions
  
    
async def Procesar_control_oficial():
    #consultar todos los pendientes en tabla procesos 
    data_collection = collection(bd_gene("control"))
    print("aqui ocurre la magia jajaja")
    async for control in data_collection.find({"estado":1},{"_id":0}).sort({"fecha_creacion":-1}):
        #aqui tenemos los procesos activos
        #verificar si el la fecha de  ya incio con respecto a la fecha actual
        print("chelas")
        print(control)
        ahora = datetime.now()
        if(ahora >control['inicio_control']):
            #consultar en datos de mysql ultimo estado y validar nivel de etileno
            eest="vamos a evaluar"
        else :
            #no pasa nada 
            est =0 
    return 1

    

async def comando_jhon_vena(imei: str):
    notificacions = []
    print("me voy a casa")
    print(imei)
    print("me voy a casa")
    data_collection = collection(bd_gene("control"))
    fecha_actual = datetime.now()
    #fecha_modificada = fecha_actual - timedelta(hours=1)
    fecha_modificada = fecha_actual - timedelta(hours=1)
    cont =0
    print(fecha_actual)
    print(fecha_modificada)
    #fechaI=datetime.fromisoformat(fecha_actual)
    #fechaF=datetime.fromisoformat(fecha_modificada)

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
    curB.close()
    cnx.close()




    async for notificacion in data_collection.find({"$and": [{"fecha_creacion": {"$lte": fecha_modificada}},{"estado":1},{"user":"jhonvena"}]},{"_id":0}).sort({"fecha_creacion":-1}):
        cont =cont+1
        #validar_tipo(dato,tipo,json_v):
        valor =validar_tipo(notificacion['dato'],notificacion['tipo'],obj_vali)
        notificacion['validacion']=valor
        notificacions.append(notificacion)
    async for notificacion in data_collection.find({"$and": [{"fecha_creacion": {"$gte": fecha_modificada}},{"user":"jhonvena"}]},{"_id":0}).sort({"fecha_creacion":-1}):
        cont =cont+1
        valor =validar_tipo(notificacion['dato'],notificacion['tipo'],obj_vali)
        notificacion['validacion']=valor
        notificacions.append(notificacion)
    print(cont)


    res ={
        "contador":cont,
        "objeto_datos":obj_vali,
        "fecha_menor" :fecha_modificada,
        "consulta_mysql" :consulta_mysql,

        "lista":notificacions
    }
    #async for notificacion in data_collection.find({"imei":imei},{"_id":0}):
        #notificacions.append(notificacion)
    #return notificacions
    return res

def convertir_a_float(dato):
    if isinstance(dato, float):
        return dato
    try:
        float_value = float(dato)
        return round(float_value,1)
    except ValueError:
        return None


def pasar_temp(numero):
    if -40 <= numero <= 130:
        return numero
    else:
        return None

async def ProcesarData():
    print("yamos jodidos")
    dispositivos=[]
    dispositivos_collection = collection(bd_gene("dispositivos"))
    #async for notificacion in dispositivos_collection.find({"estado":1,"imei":"866782048942516"},{"_id":0}):
    async for notificacion in dispositivos_collection.find({"estado":1},{"_id":0}):

        #aqui procesamos 
        datos_dispositivo =bd_gene(notificacion['imei'])
        print(datos_dispositivo)
        unidad_collection = collection(datos_dispositivo)
        async for trama in unidad_collection.find({"estado":1},{"_id":0}):
            #dato_id = await dispositivos_collection.find_one({"estado":1,"imei":"866782048942516"},{"_id":0})
            dato_id = await dispositivos_collection.find_one({"estado":1},{"_id":0})

            id_con = int(dato_id['id_cont']) +1 if dato_id['id_cont'] else 300000000

            #print("ya no tan jodido")
            #print(trama)
            #print("ya no tan jodido")
            trama_ok =str(trama['c'])
            #print("**********************")
            #print(trama['c'])
            #print("**********************")
            transformado = trama_ok.split(',')
            longitud_trama = 1 if len(transformado)>=65 else 0

            print("**********************")
            print(transformado)
            print(longitud_trama)
            print("**********************")
            if longitud_trama==1:
                #procesar datos 
                if notificacion['imei']=="866782048942516" or notificacion['imei']=="860389052714546" or notificacion['imei']=="868428040102299":
                    vali =transformado
                    #idProgre=1
                    idProgre=id_con
                    
                    tele_dispositivo =14872


                    comparador1 = vali[65] if len(transformado)>65 else 0
                    comparador2 = vali[66] if len(transformado)>66 else 0

                    if(notificacion['imei']=="860389052714546"):
                        tele_dispositivo =14876
                        valorP =  0
                        lat = 0
                        lon =0
                    elif (notificacion['imei']=="868428040102299"):
                        tele_dispositivo =14873
                        valorP =  0
                        lat = 38.6458
                        lon = -121.3880
                    else:
                        valorP = 5 if int(comparador1)==1 else 0
                        lat = 35.7396
                        lon = -119.238

                    objetoV = {
                            "id": idProgre, 
                            "set_point": pasar_temp(convertir_a_float(vali[1])), 
                            "temp_supply_1": pasar_temp(convertir_a_float(vali[2])),
                            "temp_supply_2": pasar_temp(convertir_a_float(vali[3])),
                            "return_air": pasar_temp(convertir_a_float(vali[4])), 
                            "evaporation_coil": pasar_temp(convertir_a_float(vali[5])),
                            "condensation_coil": pasar_temp(convertir_a_float(vali[6])),
                            "compress_coil_1": pasar_temp(convertir_a_float(vali[7])),
                            "compress_coil_2": pasar_temp(convertir_a_float(vali[8])), 
                            "ambient_air": pasar_temp(convertir_a_float(vali[9])), 
                            "cargo_1_temp": pasar_temp(convertir_a_float(vali[10])),
                            "cargo_2_temp": pasar_temp(convertir_a_float(vali[11])), 
                            "cargo_3_temp": pasar_temp(convertir_a_float(vali[12])), 
                            "cargo_4_temp": pasar_temp(convertir_a_float(vali[13])), 
                            "relative_humidity": convertir_a_float(vali[14]), 
                            "avl": convertir_a_float(vali[15]), 
                            "suction_pressure": convertir_a_float(vali[16]), 
                            "discharge_pressure": convertir_a_float(vali[17]), 
                            "line_voltage": convertir_a_float(vali[18]), 
                            "line_frequency": convertir_a_float(vali[19]), 
                            "consumption_ph_1": convertir_a_float(vali[20]), 
                            "consumption_ph_2": convertir_a_float(vali[21]), 
                            "consumption_ph_3": convertir_a_float(vali[22]), 
                            "co2_reading": convertir_a_float(vali[23]), 
                            "o2_reading": convertir_a_float(vali[24]), 
                            "evaporator_speed": convertir_a_float(vali[25]), 
                            "condenser_speed": convertir_a_float(vali[26]),
                            "power_kwh": convertir_a_float(vali[27]),
                            "power_trip_reading": convertir_a_float(vali[28]),
                            "suction_temp": convertir_a_float(vali[29]),
                            "discharge_temp": convertir_a_float(vali[30]),
                            "supply_air_temp": convertir_a_float(vali[31]),
                            "return_air_temp": convertir_a_float(vali[32]),
                            "dl_battery_temp": convertir_a_float(vali[33]),
                            "dl_battery_charge": convertir_a_float(vali[34]),
                            "power_consumption": convertir_a_float(vali[35]),
                            "power_consumption_avg": convertir_a_float(vali[36]),
                            "alarm_present": convertir_a_float(vali[37]),
                            "capacity_load": convertir_a_float(vali[38]),
                            "power_state": convertir_a_float(vali[39]), 
                            "controlling_mode": vali[40],
                            "humidity_control": convertir_a_float(vali[41]),
                            "humidity_set_point": convertir_a_float(vali[42]),
                            "fresh_air_ex_mode": convertir_a_float(vali[43]),
                            "fresh_air_ex_rate": convertir_a_float(vali[44]),
                            "fresh_air_ex_delay": convertir_a_float(vali[45]),
                            "set_point_o2": convertir_a_float(vali[46]),
                            "set_point_co2": convertir_a_float(vali[47]),
                            "defrost_term_temp": convertir_a_float(vali[48]),
                            "defrost_interval": convertir_a_float(vali[49]),
                            "water_cooled_conde": convertir_a_float(vali[50]),
                            "usda_trip": convertir_a_float(vali[51]),
                            "evaporator_exp_valve": convertir_a_float(vali[52]),
                            "suction_mod_valve": convertir_a_float(vali[53]),
                            "hot_gas_valve": convertir_a_float(vali[54]),
                            "economizer_valve": convertir_a_float(vali[55]),
                            "ethylene": convertir_a_float(vali[56]),
                            "stateProcess": valorP ,
                            "stateInyection": vali[64],
                            #$document['stateProcess']==5.00 vali[57]
                            "timerOfProcess": convertir_a_float(0),
                            "battery_voltage": convertir_a_float(0),
                            "power_trip_duration":convertir_a_float(0),
                            "modelo": "THERMOKING",
                            "latitud": lat,
                            "longitud":  lon,
                            "created_at": trama['fecha'],
                            "telemetria_id": tele_dispositivo,
                            "inyeccion_etileno": 0,
                            "defrost_prueba": 0,
                            "ripener_prueba": 0,
                            "sp_ethyleno": convertir_a_float(vali[61]),
                            "inyeccion_hora": convertir_a_float(vali[58]),
                            "inyeccion_pwm": convertir_a_float(vali[63]),
                            "extra_1": 0,
                            "extra_2": 0,
                            "extra_3": 0,
                            "extra_4": 0,
                            "extra_5": 0,
                            "imei":trama['i'],
                            "tiempo_paso":comparador2,
                            "device":vali[0]

                    }
                    print(objetoV)
                    #conectar a la base de datos 
                    unidad_collection3 = conexion_externa("madurador")
                    await unidad_collection3.insert_one(objetoV)
                    #actualizar estado a 0 
                    await unidad_collection.update_one({"fecha": trama['fecha']},{"$set":{"estado":0}})
                    await dispositivos_collection.update_one({"imei": trama['i']},{"$set":{"id_cont":idProgre}})
                    cnx = mysql.connector.connect(
                        host= "localhost",
                        user= "ztrack2023",
                        passwd= "lpmp2018",
                        database="zgroupztrack"
                    )

                    curB = cnx.cursor()
                    update_old_salary = (
                    "UPDATE contenedores SET ultima_fecha = %s ,set_point = %s ,temp_supply_1= %s ,return_air= %s"
                    ", ambient_air= %s ,relative_humidity= %s ,avl = %s , defrost_prueba = %s , ripener_prueba = %s , ethylene = %s"
                    " , set_point_co2 = %s , co2_reading = %s , humidity_set_point = %s , sp_ethyleno = %s , compress_coil_1 = %s "
                    ", power_state = %s , evaporation_coil = %s , controlling_mode = %s , stateProcess = %s ,cargo_1_temp = %s "
                    ", cargo_2_temp = %s , cargo_3_temp = %s , cargo_4_temp = %s , fresh_air_ex_mode = %s  WHERE estado = 1 AND telemetria_id = %s  ")
                    curB.execute(update_old_salary, (trama['fecha'], objetoV['set_point'],objetoV['temp_supply_1'], 
                                                        objetoV['return_air'], objetoV['ambient_air'], objetoV['relative_humidity'], 
                                                        objetoV['avl'], objetoV['inyeccion_pwm'], objetoV['inyeccion_hora'], 
                                                        objetoV['ethylene'], objetoV['set_point_co2'], objetoV['co2_reading'], 
                                                        objetoV['humidity_set_point'], objetoV['sp_ethyleno'],objetoV['compress_coil_1'], 
                                                        objetoV['power_state'],objetoV['evaporation_coil'],objetoV['controlling_mode'],
                                                        objetoV['stateProcess'], objetoV['cargo_1_temp'], objetoV['cargo_2_temp'],
                                                        objetoV['cargo_3_temp'], objetoV['cargo_4_temp'], objetoV['fresh_air_ex_mode'],objetoV['telemetria_id']  ))
                    cnx.commit()





            



        dispositivos.append(notificacion)
    return dispositivos

                        