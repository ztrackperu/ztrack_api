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
    colect ="D_"+imei+part
    return colect

def validar_tipo(dato,tipo,json_v):
    res=None
    if(tipo==1):
        if(json_v['power_state']==dato):
            res="ok"
    elif(tipo==2):
        if(json_v['power_state']==dato):
            res="ok"
    elif(tipo==3):
        if(json_v['set_point_co2']==dato):
            res="ok"
    elif(tipo==4):
        if(json_v['sp_ethyleno']==dato):
            res="ok"
    elif(tipo==5):
        if(json_v['inyeccion_hora']==dato):
            res="ok"
    elif(tipo==6):
        if(json_v['humidity_set_point']==dato):
            res="ok"
    elif(tipo==7):
        if(json_v['set_point']==dato):
            res="ok"
    elif(tipo==8):
        if(json_v['avl']==dato):
            res="ok"
    elif(tipo==9):
        if(json_v['avl']==dato):
            res="ok"
    elif(tipo==10):
        if(json_v['controlling_mode']==dato):
            res="ok"
    #elif(tipo==11):
        #if(json_v['power_sate']==dato):
            #res="ok"
    elif(tipo==12):
        if(json_v['fresh_air_mode']==dato):
            res="ok"
    else:
        res=None
    return res
   
async def camposol_datos() : 
    telemetrias = [15096,15100]
    


async def validar_comando():
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
    control_collection = collection(bd_gene("control"))
    notificacions = []
    fecha_actual =datetime.now()
    fecha_modificada = fecha_actual - timedelta(hours=1)


    #consultamos con mysql los datos en cuestion para validarlos de forma automatica
    async for notificacion in control_collection.find({"$or":[{"status":1},{"status":2}] },{"_id":0}):
        #print(notificacion)
        valor =validar_tipo(notificacion['dato'],notificacion['tipo'],obj_vali)
        if valor=="ok":
            #actualizar status a 3 y estado a 0 
            actualizar_comando = await control_collection.update_one({"id": notificacion['id']},{"$set":{"estado": 0,"status":3,"fecha_ejecucion":fecha_actual}})
        else:
            if fecha_modificada>notificacion['fecha_creacion'] :
                #cancelar comando
                actualizar_comando = await control_collection.update_one({"id": notificacion['id']},{"$set":{"estado": 0,"status":4,"fecha_ejecucion":fecha_actual}})
        #notificacion['_id']=0
        notificacions.append(notificacion)

    return notificacions


async def validar_comando_pabecsa():
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
    curB.execute(consulta_J, (14952,))
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
    control_collection = collection(bd_gene("control"))
    notificacions = []
    fecha_actual =datetime.now()
    fecha_modificada = fecha_actual - timedelta(hours=1)


    #consultamos con mysql los datos en cuestion para validarlos de forma automatica
    async for notificacion in control_collection.find({"$or":[{"status":1},{"status":2}] },{"_id":0}):
        #print(notificacion)
        valor =validar_tipo(notificacion['dato'],notificacion['tipo'],obj_vali)
        if valor=="ok":
            #actualizar status a 3 y estado a 0 
            actualizar_comando = await control_collection.update_one({"id": notificacion['id']},{"$set":{"estado": 0,"status":3,"fecha_ejecucion":fecha_actual}})
        else:
            if fecha_modificada>notificacion['fecha_creacion'] :
                #cancelar comando
                actualizar_comando = await control_collection.update_one({"id": notificacion['id']},{"$set":{"estado": 0,"status":4,"fecha_ejecucion":fecha_actual}})
        #notificacion['_id']=0
        notificacions.append(notificacion)

    return notificacions



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
    verificar_dispositivo = await dispositivos_collection.update_one({"imei": ztrack_data['i'],"estado":1},{"$set":{"ultimo_dato":fet}}) if Hay_dispositivo else await dispositivos_collection.insert_one({"imei":ztrack_data['i'],"estado":1,"fecha":fet})
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
datosDepurar = [
    32752,-32752, 3275.2, -3275.2, 327.52,-327.52, 32767, -32767, 3276.7, -3276.7, 327.67, -327.67,32766, -32766 , 3276.6, -3276.6, 327.66, -327.66,
    32765, -32765, 3276.5, -3276.5, 327.65, -327.65,32764, -32764, 3276.4, -3276.4, 327.64, -327.64,32763, -32763, 3276.3, -3276.3, 327.63, -327.63,
    32762, -32762, 3276.2, -3276.2, 327.62, -327.62, 32761, -32761, 3276.1, -3276.1, 327.61, -327.61,32760, -32760, 3276.0, -3276.0, 327.60, -327.60,
    32759, -32759, 3275.9, -3275.9, 327.59, -327.59,32751, -32751, 3275.1, -3275.1, 327.51, -327.51,-3277,-3276.9,-38.5,25.4,255,18559
]
def depurar_coincidencia(dato, datosDepurar=datosDepurar):
    if dato in datosDepurar:
        return None
    else:
        return dato

def procesar_texto(texto):
    # Dividir el texto en partes separadas por "_"
    partes = texto.split("_") 
    # Convertir cada parte a mayúsculas para capitalizar las palabras
    partes_capitalizadas = [parte.capitalize() for parte in partes]   
    # Unir las partes con espacios en blanco
    texto_procesado = " ".join(partes_capitalizadas) 
    return texto_procesado

# import all you need from fastapi-pagination

async def config(empresa :int):
    notificacions=[]
    database =collection["config_ztrack"]
    empresa_config= database.get_collection("empresa_config")
    async for mad in empresa_config.find({"user_id":empresa},{"_id":0}):
        notificacions.append(mad)
    #se debe extraer el primir resultado
    return notificacions[0]

async def data_madurador(notificacion_data: dict) -> dict:
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




#async def add_notificacion(notificacion_data: dict) -> dict:
    #aqui envia el json a mongo y lo inserta
    #notificacion = await notificacion_collection.insert_one(notificacion_data)
    #aqui busca el dato obtenido para mostrarlo como respuesta
    #new_notificacion = await notificacion_collection.find_one({"_id": notificacion.inserted_id})
    #return notificacion_helper(new_notificacion)   

                        
async def obtener_madurador() -> dict:
    bd = "ZGRU9015808_5_2024"
    database = collection[bd]
    print(bd)
    madurador = database.get_collection("madurador")
    notificacions = []
    pip = [
            { 
                "$and": [
                    {"created_at": {"$gte": datetime.fromisoformat("2024-05-07T00:00:00.000Z")}},
                    {"created_at": {"$lte": datetime.fromisoformat("2024-05-09T23:59:59.999Z")}}
                    ]
            },
            {"_id":0}
        ]  
    async for mad in madurador.find({ "$and": [{"created_at": {"$gte": datetime.fromisoformat("2024-05-07T00:00:00.000Z")}},{"created_at": {"$lte": datetime.fromisoformat("2024-05-09T23:59:59.999Z")}}]},{"_id":0}):
        notificacions.append(mad)
    return  notificacions




