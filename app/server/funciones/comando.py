import json
from server.database import collection ,collectionTotal ,conexion_externa
from bson import regex
from datetime import datetime,timedelta


def bd_gene(imei):
    fet =datetime.now()
    #part = fet.strftime('%d_%m_%Y')
    part = fet.strftime('_%m_%Y')
    colect ="D_"+imei+part
    return colect
async def GuardarComandos(ztrack_data: dict) -> dict:
    #dat = ztrack_data['fecha']
    #print(ztrack_data)
    data_collection = collection(bd_gene("control"))
    notificacion = await data_collection.insert_one(ztrack_data)
    new_notificacion = await data_collection.find_one({"_id": notificacion.inserted_id},{"_id":0})
    return new_notificacion

async def RetrieveComandos(imei: str):
    notificacions = []
    print("me voy a casa")
    print(imei)
    print("me voy a casa")
    data_collection = collection(bd_gene("control"))
    async for notificacion in data_collection.find({"imei":imei},{"_id":0}):
        notificacions.append(notificacion)
    return notificacions

def convertir_a_float(dato):
    if isinstance(dato, float):
        return dato
    try:
        float_value = float(dato)
        return float_value
    except ValueError:
        return None

async def ProcesarData():
    print("yamos jodidos")
    dispositivos=[]
    dispositivos_collection = collection(bd_gene("dispositivos"))
    async for notificacion in dispositivos_collection.find({"estado":1,"imei":"866782048942516"},{"_id":0}):
        #aqui procesamos 
        datos_dispositivo =bd_gene(notificacion['imei'])
        print(datos_dispositivo)
        unidad_collection = collection(datos_dispositivo)
        async for trama in unidad_collection.find({"estado":0},{"_id":0}):
            dato_id = await dispositivos_collection.find_one({"estado":1,"imei":"866782048942516"},{"_id":0})
            id_con = int(dato_id['id_cont']) +1 if dato_id['id_cont'] else 300000000

            #print("ya no tan jodido")
            #print(trama)
            #print("ya no tan jodido")
            trama_ok =str(trama['c'])
            #print("**********************")
            #print(trama['c'])
            #print("**********************")
            transformado = trama_ok.split(',')
            longitud_trama = 1 if len(transformado)==65 else 0

            print("**********************")
            print(transformado)
            print(longitud_trama)
            print("**********************")
            if longitud_trama==1:
                #procesar datos 
                if notificacion['imei']=="866782048942516":
                    vali =transformado
                    #idProgre=1
                    idProgre=id_con
                    tele_dispositivo =14872
                    objetoV = {
                            "id": idProgre,
                            "set_point": convertir_a_float(vali[1]), 
                            "temp_supply_1": convertir_a_float(vali[2]),
                            "temp_supply_2": convertir_a_float(vali[3]),
                            "return_air": convertir_a_float(vali[4]), 
                            "evaporation_coil": convertir_a_float(vali[5]),
                            "condensation_coil": convertir_a_float(vali[6]),
                            "compress_coil_1": convertir_a_float(vali[7]),
                            "compress_coil_2": convertir_a_float(vali[8]), 
                            "ambient_air": convertir_a_float(vali[9]), 
                            "cargo_1_temp": convertir_a_float(vali[10]),
                            "cargo_2_temp": convertir_a_float(vali[11]), 
                            "cargo_3_temp": convertir_a_float(vali[12]), 
                            "cargo_4_temp": convertir_a_float(vali[13]), 
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
                            "stateProcess": vali[1],
                            "stateInyection": vali[1],
                            "timerOfProcess": convertir_a_float(vali[1]),
                            "battery_voltage": convertir_a_float(vali[1]),
                            "power_trip_duration":convertir_a_float(vali[1]),
                            "modelo": vali[1],
                            "latitud": 35.7396,
                            "longitud":  -119.238,
                            "created_at": trama['fecha'],
                            "telemetria_id": tele_dispositivo,
                            "inyeccion_etileno": 0,
                            "defrost_prueba": 0,
                            "ripener_prueba": 0,
                            "sp_ethyleno": convertir_a_float(vali[1]),
                            "inyeccion_hora": convertir_a_float(vali[1]),
                            "inyeccion_pwm": convertir_a_float(vali[63]),
                            "extra_1": 0,
                            "extra_2": 0,
                            "extra_3": 0,
                            "extra_4": 0,
                            "extra_5": 0,
                            "imei":trama['i'],
                            "device":vali[0]

                    }
                    print(objetoV)
                    #conectar a la base de datos 
                    unidad_collection3 = conexion_externa("madurador")
                    await unidad_collection3.insert_one(objetoV)
                    #actualizar estado a 0 
                    await unidad_collection.update_one({"fecha": trama['fecha']},{"$set":{"estado":1}})
                    await dispositivos_collection.update_one({"imei": trama['i']},{"$set":{"id_cont":idProgre}})





            



        dispositivos.append(notificacion)
    return dispositivos

                        