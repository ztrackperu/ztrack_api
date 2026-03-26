

procesadora_peru=["867858038371947"]
#leer el archivo test_cerro.json
with open('test_cerro.json', 'r') as file:
    data = json.load(file)
    datos = []
    for item in data:
        print(item)
        #si el item['c'] es None, entonces no procesar
        if item['c'] is None:
            continue
        #si el item['c'] es not None, entonces procesar
        else:
            print("procesando")
            print(item['c'])
            print("**********************")
            # c normlamente tiene esta etsrcutura LOSU1770730,20.00,25.50,401.00,22.10,24.30,25.90,41.80,400.00,24.00,401.00,401.00,401.00,401.00,67,401,401.00,401.00,446,60,6.00,5.80,5.90,401.00,401.00,60,0,14.00,4.00,401.00,401.00,25.50,22.10,401.00,0.00,1.92,0.00,0,53,1,1,1,85,0,401,401.00,401.00,401.00,18.00,6,0,0,255,255,255,255,0.00,0,0,0,0,0,0,0.00,0,0,0",
            # entonces se debe separar por comas y obtener el valor de la posicion 65
            transformado = item['c'].split(',')
            #verificar que tenga 70 elementos  de er menor completra con 0 en el array transformado
            while len(transformado) < 70:
                transformado.append('0')
            imei = procesadora_peru[0]
            tele_dispositivo =15029
            valorP =  0
            lat = -12.09858
            lon = -77.01155

            objetoV = {
                "id": 1, 
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
                "power_state":convertir_a_float(con_h( vali[39],vali[14])), 
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
                "created_at": item['fecha'],
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
                "imei":imei,
                "tiempo_paso":0,
                "device":vali[0]

            }
            #acumular los datos en un array
            datos.append(objetoV)

    #guardar los datos en un archivo json
    with open('datos_cerro_prieto_antiguo.json', 'w') as file:
        json.dump(datos, file)


            









