import json
from server.database import collection ,collectionTotal
from bson import regex
from datetime import datetime,timedelta
from fastapi_pagination.ext.motor import paginate
import mysql.connector


#dir = "GPRMC,225556.00,A,1200.76343,S,07706.36069,W,0.037,,191124,,,A*7C"

lat_neg = 0
lon_neg = 0

#  GPRMC,164308.00,A,1133.40415,S,07716.12044,W,28.161,134.48,221124,,,A*59

def procesar_gps(tra):
    elementos_gps = tra.split(',')
    if len(elementos_gps)==13 :
        #evaluamos si el dato es "A" continuamos , sino completamos con puro 0 el array
        if elementos_gps[2]=="A":
            #realizar el proceso de gps
            velocidad =0
            direccion=None
            fecha_gps =None
            #1133.40415
            val_lat = float(elementos_gps[3])
            #07716.12044
            val_lon = float(elementos_gps[5])
            #11
            int_lat = int(val_lat / 100)
            #77
            int_lon = int(val_lon / 100)

            #1133.40415-1100  = 33.40415
            seg_lat = val_lat - (int_lat*100)
            #7716.12044-7700  = 16.12044  
            seg_lon = val_lon - (int_lon*100)

            #33.40415/60  =0.55673583
            seg_lat = seg_lat / 60
            #16.12044/60 = 0.268674
            seg_lon = seg_lon / 60

            #11.5567358
            #77.268674
            lat_final = round(float(int_lat) + seg_lat , 8)
            lon_final = round(float(int_lon) + seg_lon , 8)
            if elementos_gps[4]=="S" or elementos_gps[4]=="s" :
                lat_final=lat_final*(-1)
            if elementos_gps[6]=="W" or elementos_gps[4]=="w" :
                lon_final=lon_final*(-1)
            if elementos_gps[7] :
                velocidad = float(elementos_gps[7])
                velocidad = round(velocidad * 1.852,2)
            if elementos_gps[8] :
                direccion=float(elementos_gps[8])
            if elementos_gps[1] and elementos_gps[9]:
                fecha_gps =str(elementos_gps[9])+"_"+str(elementos_gps[1])
            
            r=[lat_final,lon_final,velocidad,direccion,fecha_gps]
        else :
            r=[None,None,None,None,None]
    else :
        r=[None,None,None,None,None]
    return r

def bd_gene(imei):
    fet =datetime.now()
    #part = fet.strftime('%d_%m_%Y')
    part = fet.strftime('_%m_%Y')
    colect ="G_"+imei+part
    return colect
 
def procesar_d00(text):
    # Dividir el texto en elementos separados por comas
    hex_elements = text.split(',')
    if len(hex_elements)==20 :
        # Convertir cada elemento hexadecimal a decimal
        decimal_array = [int(hex_elem, 16) for hex_elem in hex_elements]
    else :
        decimal_array=0
    
    return decimal_array

def array_datos_genset(ar):
    if ar==None :
        #llenar array e puros ceros 
        ar=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #establecer un objeto para procesar : 
    genset = {
        "Tr_Timer1":ar[0]/1,
        "Tr_Timer2":ar[1]/1,
        "Rt_Voltage":ar[2]/10,
        "Rt_Battery":ar[3]/100,
        "Rt_Water":ar[4]/10,
        "Rt_Frequency":ar[5]/10,
        "Rt_Fuel":ar[6]/10,
        "Rt_Voltaje2":ar[7]/10,
        "Rt_Rotor":ar[8]/10,
        "Rt_Field":ar[9]/10,
        "Dv_Setting":ar[10]/1,
        "Dv_Alarm":ar[11]/1,
        "Dv_Message":ar[12]/1,
        "Dv_Mode":ar[13]/1,
        "Dv_Fuel":ar[14]/10,
        "Dv_Voltage":ar[15]/10,
        "Dv_Frequency":ar[16]/10,
        "Dv_Battery":ar[17]/10,
        "Dv_Water":ar[18]/10,
        "Dv_rpm":ar[19]/1
    }
    print(genset)
    return  genset



async def procesar_maersk():
    fet =datetime.now()
    imei = "863576046753492"
    #aqui capturamos al coleccion y procesamos los datos 
    data_collection = collection(bd_gene(imei))
    #pasamos todo a nueva base de datos D_MAERSK_11_2024
    proceso_collection =collection(bd_gene("MAERSK"))
    id_cole =collection(bd_gene("id_gene"))
    notificacions=[]
    cont_config = 0 
    cont_on =0
    cont_off =0
    cont_fail =0
    dato_id =await id_cole.find_one({'seguimiento':'maersk'},{"_id":0})
    if dato_id['fecha_procesada'] :
       busqueda = {"$and": [{"fecha_procesada": {"$lte": dato_id['fecha_procesada']}},{"estado":1}]}
    else :
        busqueda ={"estado":1}

    async for notificacion in data_collection.find(busqueda,{"_id":0}).sort({"fecha":1}):
        if notificacion['d01'] and  notificacion['d02'] and  notificacion['d03'] and  notificacion['d04'] and  notificacion['i'] :
            #config
            #de momento no procesar 
            cont_config+=1
        elif  notificacion['d00'] and  notificacion['d09'] and  notificacion['i'] :
            #invocar la funcion de resuelve d00 donde estan todo los datos 
            proceso_uno = procesar_d00(notificacion['d00'])
            if proceso_uno : 
                #aqui va la conversion si todo esta bien 
                proceso_dos = array_datos_genset(proceso_uno)
                #añadimos la hora a array 
                proceso_dos['fecha_r']=notificacion['fecha']
                proceso_dos['on_off']=1
                #procesar gps 
                proceso_gps = procesar_gps(notificacion['gps'])
                if proceso_gps :
                    #r=[seg_lat,seg_lon,velocidad,direccion,fecha_gps]
                    proceso_dos['latitud']=proceso_gps[0]
                    proceso_dos['longitud']=proceso_gps[1]
                    proceso_dos['velocidad']=proceso_gps[2]
                    proceso_dos['direccion']=proceso_gps[3]
                    proceso_dos['fecha_gps']=proceso_gps[4]
                    proceso_dos['link_mapa']="maps.google.com/?q=" + str(proceso_dos['latitud']) + "," + str(proceso_dos['longitud'])

                
                #realizar consulta de datos 
                #dato_id =await id_cole.find_one({'seguimiento':'maersk'},{"_id":0})
                if dato_id :
                    proceso_dos['_id']=dato_id['maersk']+1
                    #actualizamos
                    notificacion_1 = await id_cole.update_one(
                     {'seguimiento':'maersk'}, {"$set": {"maersk":proceso_dos['_id'],"fecha_procesada":proceso_dos['fecha_r'] }}
                    )
                else :
                    proceso_dos['_id']=1
                    #crear
                    notificacion_1 = await id_cole.insert_one({'maersk':proceso_dos['_id'],'seguimiento':'maersk',"fecha_procesada":proceso_dos['fecha_r'] })

                cont_on+=1
                #enviar data a repositorio final 
                notificacion = await proceso_collection.insert_one(proceso_dos)
            else :
                cont_fail=+1


        elif notificacion['gps'] and notificacion['d00']==None and  notificacion['d09']==None and notificacion['d01']==None and  notificacion['d02']==None and  notificacion['d03']==None and  notificacion['d04']==None and  notificacion['i'] : 
            proceso_dos = array_datos_genset(notificacion['d00'])
            proceso_dos['fecha_r']=notificacion['fecha']
            proceso_dos['on_off']=0
            proceso_gps = procesar_gps(notificacion['gps'])
            if proceso_gps :
                #r=[seg_lat,seg_lon,velocidad,direccion,fecha_gps]
                proceso_dos['latitud']=proceso_gps[0]
                proceso_dos['longitud']=proceso_gps[1]
                proceso_dos['velocidad']=proceso_gps[2]
                proceso_dos['direccion']=proceso_gps[3]
                proceso_dos['fecha_gps']=proceso_gps[4]
                proceso_dos['link_mapa']="maps.google.com/?q=" + str(proceso_dos['latitud']) + "," + str(proceso_dos['longitud'])

            #enviar data a repositorio final 
            #realizar consulta de datos 
            #dato_id =await id_cole.find_one({'seguimiento':'maersk'},{"_id":0})
            if dato_id :
                proceso_dos['_id']=dato_id['maersk']+1
                #actualizamos
                notificacion_1 = await id_cole.update_one(
                    {'seguimiento':'maersk'}, {"$set": {"maersk":proceso_dos['_id'],"fecha_procesada":proceso_dos['fecha_r'] }}
                )
            else :
                proceso_dos['_id']=1
                #crear
                notificacion_1 = await id_cole.insert_one({'maersk':proceso_dos['_id'],'seguimiento':'maersk',"fecha_procesada":proceso_dos['fecha_r'] })
            cont_off+=1

        else :
            cont_fail=+1

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









