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


def ultimos_tres_dias():
    # Crear una lista para almacenar los últimos tres días
    dias = []
    
    # Obtener la fecha actual
    hoy = datetime.now()
    
    # Obtener los últimos tres días
    for i in range(1, 4):
        dia = hoy - timedelta(days=i)
        # Formatear cada fecha en el formato "dd-mm-yyyy"
        dias.append(dia.strftime('%d-%m-%Y'))
    
    return dias
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


def bd_gene_1(imei):
    fet =datetime.now()
    #part = fet.strftime('%d_%m_%Y')
    part = fet.strftime('_%m_%Y')
    colect ="pre_1_"+imei+part
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


def procesar_fecha_fila(utc,fechaI,fechaF="0"):
    terrible = 0 ; 
    #print(fechaI)
    #print(fechaF)
    if(utc!=300):
        #terrible =300-utc
        terrible =utc-300
    #print(terrible)
    #print(utc)
    if(fechaF=="0"):
        fechaIx=  datetime.fromisoformat(fechaI)-timedelta(hours=12)+timedelta(minutes=terrible)
        fechaFx = datetime.fromisoformat(fechaI)+timedelta(minutes=terrible)
        #aqui pedir 
    else:
        fechaIx=  datetime.fromisoformat(fechaI)+timedelta(minutes=terrible)
        fechaFx = datetime.fromisoformat(fechaF)+timedelta(minutes=terrible)
    data = [fechaIx,fechaFx]
    #print(data)
    return data

#funcion meses optimizada para generadores 
def oMeses(dispositivo,fecha_inicio=0, fecha_fin=0):
    meses = []
    if fecha_inicio==0 or  fecha_fin==0 :
        #se entinede que solo hay que pedir el periodo actual 
        meses.append(bd_gene_1(dispositivo))
        return  meses 
    else :
        inicio = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M:%S')
        fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%S')
        # Iterar sobre los meses en el rango
        while inicio <= fin:
            # Agregar el mes actual a la lista
            meses.append("pre_1_"+dispositivo+"_"+str(inicio.strftime('%m'))+inicio.strftime('_%Y'))
            # Avanzar al siguiente mes
            inicio += timedelta(days=32)
            inicio = inicio.replace(day=1)
        return meses


async def procesar_tabla_datos(notificacion_data: dict) -> dict:
    fet_actual =datetime.now()
    if(notificacion_data['fechaF']=="0" and notificacion_data['fechaI']=="0"):
        fecha_formateada = fet_actual.strftime("%Y-%m-%dT%H:%M:%S")
        fech = procesar_fecha_fila(notificacion_data['utc'],fecha_formateada)
        periodos =oMeses(notificacion_data['imei'])
        #bconsultas =oMeses(notificacion_data['device'],notificacion_data['ultima'],notificacion_data['ultima'])
    else : 
        fech = procesar_fecha_fila(notificacion_data['utc'],notificacion_data['fechaI'],notificacion_data['fechaF'])
        #bconsultas =oMeses(notificacion_data['device'],notificacion_data['fechaI'],notificacion_data['fechaF'])
        periodos =oMeses(notificacion_data['imei'],notificacion_data['fechaI'],notificacion_data['fechaF'])
    #diferencial =[ periodos , {"created_at": {"$gte": fech[0]}},{"created_at": {"$lte": fech[1]}}]
    #return diferencial
    
    if len(periodos)==1 :
        #print(periodos)
        #declaramos la busqueda en el rango establecido 
        tabla=[]
        data_collection = collection(periodos[0])
        diferencial =[{"fecha_r": {"$gte": fech[0]}},{"fecha_r": {"$lte": fech[1]}}]
        pip = [{"$match": {"$and":diferencial}}]
        async for concepto_ot in data_collection.aggregate(pip):
            #print(concepto_ot)
            tabla.append(concepto_ot)
        return tabla
    else :
        return 0



async def procesar_grafico_datos(notificacion_data: dict) -> dict:
    fet_actual =datetime.now()
    if(notificacion_data['fechaF']=="0" and notificacion_data['fechaI']=="0"):
        fecha_formateada = fet_actual.strftime("%Y-%m-%dT%H:%M:%S")
        fech = procesar_fecha_fila(notificacion_data['utc'],fecha_formateada)
        periodos =oMeses(notificacion_data['imei'])
        #bconsultas =oMeses(notificacion_data['device'],notificacion_data['ultima'],notificacion_data['ultima'])
    else : 
        fech = procesar_fecha_fila(notificacion_data['utc'],notificacion_data['fechaI'],notificacion_data['fechaF'])
        #bconsultas =oMeses(notificacion_data['device'],notificacion_data['fechaI'],notificacion_data['fechaF'])
        periodos =oMeses(notificacion_data['imei'],notificacion_data['fechaI'],notificacion_data['fechaF'])
    #diferencial =[ periodos , {"created_at": {"$gte": fech[0]}},{"created_at": {"$lte": fech[1]}}]
    #return diferencial
    
    if len(periodos)==1 :
        #print(periodos)
        #declaramos la busqueda en el rango establecido 
        tabla=[]
        data_collection = collection(periodos[0])
        diferencial =[{"fecha_r": {"$gte": fech[0]}},{"fecha_r": {"$lte": fech[1]}}]
        pip = [{"$match": {"$and":diferencial}}]
        #array para juntar datos 
        fecha =[]
        bateria =[]
        voltaje =[]
        combustible = []
        rpm=[]
        motor=[]
        frecuencia = []


        async for concepto_ot in data_collection.aggregate(pip):
            #print(concepto_ot)
            fecha.append(concepto_ot['fecha_r'])
            bateria.append(concepto_ot['Dv_Battery'])
            voltaje.append(concepto_ot['Dv_Voltage'])
            combustible.append(concepto_ot['Dv_Fuel'])
            rpm.append(concepto_ot['Dv_rpm'])
            motor.append(concepto_ot['Dv_Water'])
            frecuencia.append(concepto_ot['Dv_Frequency'])

        return {"fecha":fecha,"bateria":bateria,"voltaje":voltaje,"combustible":combustible,"rpm":rpm,"motor":motor,"frecuencia":frecuencia}
    else :
        return 0
    



async def procesar_gps_datos(notificacion_data: dict) -> dict:
    fet_actual =datetime.now()
    if(notificacion_data['fechaF']=="0" and notificacion_data['fechaI']=="0"):
        fecha_formateada = fet_actual.strftime("%Y-%m-%dT%H:%M:%S")
        fech = procesar_fecha_fila(notificacion_data['utc'],fecha_formateada)
        periodos =oMeses(notificacion_data['imei'])
        #bconsultas =oMeses(notificacion_data['device'],notificacion_data['ultima'],notificacion_data['ultima'])
    else : 
        fech = procesar_fecha_fila(notificacion_data['utc'],notificacion_data['fechaI'],notificacion_data['fechaF'])
        #bconsultas =oMeses(notificacion_data['device'],notificacion_data['fechaI'],notificacion_data['fechaF'])
        periodos =oMeses(notificacion_data['imei'],notificacion_data['fechaI'],notificacion_data['fechaF'])
    #diferencial =[ periodos , {"created_at": {"$gte": fech[0]}},{"created_at": {"$lte": fech[1]}}]
    #return diferencial
    
    if len(periodos)==1 :
        #print(periodos)
        #declaramos la busqueda en el rango establecido 
        tabla=[]
        data_collection = collection(periodos[0])
        diferencial =[{"fecha_r": {"$gte": fech[0]}},{"fecha_r": {"$lte": fech[1]}}]
        pip = [{"$match": {"$and":diferencial}}]
        #array para juntar datos 
        fecha =[]
        latitud =[]
        longitud =[]
        direccion = []
        velocidad=[]



        async for concepto_ot in data_collection.aggregate(pip):
            #print(concepto_ot)
            fecha.append(concepto_ot['fecha_r'])
            latitud.append(concepto_ot['latitud'])
            longitud.append(concepto_ot['longitud'])
            direccion.append(concepto_ot['direccion'])
            velocidad.append(concepto_ot['velocidad'])


        return {"fecha":fecha,"latitud":latitud,"longitud":longitud,"direccion":direccion,"velocidad":velocidad}
    else :
        return 0

#procesar datos en tiempo real ,y de froma constante de generador 
#live_generador
async def live_generador():
    notificacions=[]
    dispositivos_collection = collection(bd_gene('dispositivos'))
    generador_collection =collection(bd_gene('genset'))
    async for mad in dispositivos_collection.find({"estado":1},{"_id":0}):
        notificacions.append(mad)
        print(mad['imei'])
        dat = await procesar_genset(mad['imei'])
    return notificacions



async def procesar_genset(imei):
    generador_collection =collection(bd_gene('genset'))

    fet =datetime.now()
    #imei = "863576046753492"
    #aqui capturamos al coleccion y procesamos los datos 
    data_collection = collection(bd_gene(imei))
    #pasamos todo a nueva base de datos D_MAERSK_11_2024
    proceso_collection =collection(bd_gene_1(imei))
    id_cole =collection(bd_gene("id_gene"))
    notificacions=[]
    cont_config = 0 
    cont_on =0
    cont_off =0
    cont_fail =0
    dato_id_i =await id_cole.find_one({'seguimiento':imei},{"_id":0})
    if dato_id_i :
       busqueda = {"$and": [{"fecha": {"$gt": dato_id_i['fecha_procesada']}},{"estado":1}]}
    else :
        busqueda ={"estado":1}

    async for notificacion in data_collection.find(busqueda,{"_id":0}).sort({"fecha":1}):
        print("-----------------")
        print(bd_gene(imei))
        print("-----------------")
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
                dato_id =await id_cole.find_one({'seguimiento':imei},{"_id":0})
                if dato_id :
                    proceso_dos['_id']=dato_id['maersk']+1
                    #actualizamos
                    notificacion_1 = await id_cole.update_one(
                     {'seguimiento':imei}, {"$set": {"maersk":proceso_dos['_id'],"fecha_procesada":proceso_dos['fecha_r'] }}
                    )
                else :
                    proceso_dos['_id']=1
                    #crear
                    notificacion_1 = await id_cole.insert_one({'maersk':proceso_dos['_id'],'seguimiento':imei,"fecha_procesada":proceso_dos['fecha_r'] })

                cont_on+=1
                #enviar data a repositorio final 
                notificacion_ok = await proceso_collection.insert_one(proceso_dos)
                #despues de guardar la data , validar si existe registro Live , sino crearlo , y si existe actualizarlo 
                genset_id =await generador_collection.find_one({'imei':imei},{"_id":0})
                
                if genset_id :
                    del proceso_dos['_id']
                    notificacion_2 = await generador_collection.update_one(
                     {'imei':imei}, {"$set": proceso_dos}
                    )
                else :
                    del proceso_dos['_id']
                    proceso_dos['primera_conexion']=notificacion['fecha']
                    proceso_dos['generador']=None
                    proceso_dos['imei']=imei
                    proceso_dos['estado']=1
                    proceso_dos['descripcion']=None
                    proceso_dos['config']=None
                    notificacion_2 = await generador_collection.insert_one(proceso_dos)
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
            dato_id =await id_cole.find_one({'seguimiento':imei},{"_id":0})
            if dato_id :
                proceso_dos['_id']=dato_id['maersk']+1
                #actualizamos
                notificacion_1 = await id_cole.update_one(
                    {'seguimiento':imei}, {"$set": {"maersk":proceso_dos['_id'],"fecha_procesada":proceso_dos['fecha_r'] }}
                )
            else :
                proceso_dos['_id']=1
                #crear
                notificacion_1 = await id_cole.insert_one({'maersk':proceso_dos['_id'],'seguimiento':imei,"fecha_procesada":proceso_dos['fecha_r'] })      
                #enviar data a repositorio final 
            notificacion_ok = await proceso_collection.insert_one(proceso_dos)
            #despues de guardar la data , validar si existe registro Live , sino crearlo , y si existe actualizarlo 
            genset_id =await generador_collection.find_one({'imei':imei},{"_id":0})
            
            if genset_id :
                del proceso_dos['_id']
                notificacion_2 = await generador_collection.update_one(
                    {'imei':imei}, {"$set": proceso_dos}
                )
            else :
                del proceso_dos['_id']
                proceso_dos['primera_conexion']=notificacion['fecha']
                proceso_dos['generador']=None
                proceso_dos['imei']=imei
                proceso_dos['estado']=1
                proceso_dos['descripcion']=None
                proceso_dos['config']=None
                notificacion_2 = await generador_collection.insert_one(proceso_dos)
            
            cont_off+=1

        else :
            cont_fail=+1

        print(notificacion)
        notificacions.append(notificacion)
    return  [cont_config ,cont_on ,cont_off , cont_fail ,notificacions]








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
    dato_id_i =await id_cole.find_one({'seguimiento':'maersk'},{"_id":0})
    if dato_id_i :
       busqueda = {"$and": [{"fecha": {"$gt": dato_id_i['fecha_procesada']}},{"estado":1}]}
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
                dato_id =await id_cole.find_one({'seguimiento':'maersk'},{"_id":0})
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
            dato_id =await id_cole.find_one({'seguimiento':'maersk'},{"_id":0})
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



async def grafica_generador(notificacion_data: dict) -> dict:
        #pedir la ultima conexion 
    #ultima conexion pedir mes y año 
                                                                                                                                                                         
    #construir base de datos 
    #database = client.intranet
    per = notificacion_data['ultima'].split('T')
    #ARRAY 0 represnta la fecha y 1 la hora
    periodo = per[0].split('-')
    #periodo 0 , es el año , 1 es el mes , 2 es el dia 
    #armamos la base de datos 
    bd = notificacion_data['device']+"_"+str(int(periodo[1]))+"_"+periodo[0]
    database = client[bd]
    #print(bd)
    #print("olitas")
    #print(notificacion_data['empresa'])
    #print(notificacion_data['page'])
    #print(notificacion_data['size'])
    madurador = database.get_collection("madurador")
    #notificacion_collection = collection("notificaciones")
    page=notificacion_data['page']
    limit=notificacion_data['size']
    empresa =notificacion_data['empresa']
    #esquema para consultar data 
    dataConfig =await config(empresa)
    #print(dataConfig)
    #print(dataConfig['config_data'])
    #print(dataConfig['config_graph'])
    #result = madurador.find({ "$and": [{"created_at": {"$gte": datetime.fromisoformat("2024-05-07T00:00:00.000Z")}},{"created_at": {"$lte": datetime.fromisoformat("2024-05-09T23:59:59.999Z")}}]},{"_id":0})                                
    #esquema con agregation para mayor versatilidad
    if(notificacion_data['fechaF']=="0" and notificacion_data['fechaI']=="0"):
        fechaF = datetime.fromisoformat(notificacion_data['ultima'])
        one_day = timedelta(hours=12)
        fechaI = fechaF-one_day
        #print(certeza)
        #print(certeza1)
    else : 
        fechaI=datetime.fromisoformat(notificacion_data['fechaI'])
        fechaF=datetime.fromisoformat(notificacion_data['fechaF'])
    print(fechaI)
    print(fechaF)

    pip = [
        {"$match": {
                "$and":[
                    {"created_at": {"$gte": fechaI}},
                    {"created_at": {"$lte": fechaF}}
                ]
            }
        },  
        {"$project":dataConfig['config_data']},
        {"$skip" : (page-1)*limit},
        {"$limit" : limit},  
    ]

    #recorrer array y crear varaibles para insertar
    graph = dataConfig['config_graph']
    #print("baja")
    #print(graph)
    #print("alta")
    listas = {}
    cadena =[]
    for i in range(len(graph)):
        #print(graph[i]['label'])
        nombre_lista = f"{graph[i]['label']}"
        cadena.append(graph[i]['label'])
        lab = procesar_texto(graph[i]['label'])

        listas[nombre_lista] = {
            "data":[],
            "config":[lab,graph[i]['hidden'],graph[i]['color'],graph[i]['tipo']]
        }

    concepto_ots = []
    async for concepto_ot in madurador.aggregate(pip):
        #print(concepto_ot)
        concepto_ots.append(concepto_ot)
        for i in range(len(graph)):
           #dataConfig['config_graph'][i].append(concepto_ot[dataConfig['config_graph'][i]])
           #primerfiltro =depurar_coincidencia(concepto_ot[dato[i]])
           #if(primerfiltro!=None):
               #aqui evaluamos si sera filtro de temperatura , porcentaje , ety-avl, area
                #pu ="oli"
           
           dato =graph
           #print(dato)
           #listas[dato[i]].append(concepto_ot[dato[i]])
           listas[dato[i]['label']]["data"].append(depurar_coincidencia(concepto_ot[dato[i]['label']]))

           #print(concepto_ot[dato[i]])s
           #dato[i].append(concepto_ot[dato[i]])
        #print(concepto_ot['return_air'])
    #print(listas)
    listasT = {"graph":listas,"table":concepto_ots,"cadena":cadena}
    #print(listasT)

    return listasT


    


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

#busqueda de info por empresa_id
async def empresa(id: int) -> dict:
    generador_collection =collection(bd_gene('genset'))
    cont_on = 0
    cont_off =0
    notificacions = []
    async for notificacion in generador_collection.find({"empresa_id": int(id)},{"_id":0}):
        #print(notificacion)
        notificacions.append(notificacion)
        if notificacion['on_off']==0 :
            cont_off+=1
        else : 
            cont_on+=1

    datazo = ultimos_tres_dias()
    conjunto = {
        "genset" :notificacions,
        "condicion" : {
            "on":cont_on,
            "off":cont_off
        },
        "consumo":{
            "fechas":datazo,
            "datos":[0,0,0]
        },
        "general" :{
            "alarmas":0,
            "mensajes":0,
            "horas":0
        }
    }
    return conjunto

#busqueda de info por config

#busqueda de info por empresa_id
async def config(id: int) -> dict:
    generador_collection =collection(bd_gene('genset'))

    #print(id)
    #importante convertir a int cunado se busca a un dato por numero
    
    notificacion = await generador_collection.find_one({"config": int(id)},{"_id":0})
    #print(notificacion)
    if notificacion:
        return notificacion 






