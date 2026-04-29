import json
from server.database import collection ,collectionTotal
from bson import regex
from datetime import datetime, timedelta, timezone
from fastapi_pagination.ext.motor import paginate
from typing import Dict, List, Optional, Any
import mysql.connector

def bd_oficial(imei="",periodo=""):
    per_actual = datetime.now().year
    bd_ok ="STARCOOL_OFICIAL_"+str(per_actual)
    #if imei!=""and periodo!="" :
    if imei!="" :
        bd_ok = str(imei)+"_"+bd_ok
    return bd_ok


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


#va para tunel 
async def ultimo_estado_dispositivos_starcool() -> Dict[str, Any]:
    """
    Último estado de cada dispositivo según S_IMEI_MES_AÑO.
    Incluye resumen por estado (online/wait/offline), campos elementales, power_state on/off
    y en_rango (return_air ±5 respecto a set_point). Pensado para mostrar en tabla.
    """   
    
    data_proceso_actual = collection(bd_gene("dispositivos"))
    dispositivos: List[Dict[str, Any]] = []
    ahora_gmt5 = _ahora_gmt5()

    async for notificacion in data_proceso_actual.find({"estado": 1}, {"_id": 0, "imei": 1,"ultimo_dato":1}):
        print("notificacion")
        print(notificacion)

        
        imei = notificacion.get("imei")
        if not imei:
            continue
        coll_oficial = collection(bd_oficial(imei))

        ultimo = await coll_oficial.find_one(
            {},
            {"_id": 0},
            sort=[("_id", -1)]   # O(1) con el índice _id que ya existe por defecto
        )
        fecha_ultima: Optional[datetime] = ultimo.get("fecha") if ultimo else None
        fecha_gmt5 = _fecha_ultima_como_gmt5(fecha_ultima)
        estado_conexion = _calcular_estado_conexion(fecha_ultima)

        if fecha_gmt5 is not None:
            minutos_desde = (ahora_gmt5 - fecha_gmt5).total_seconds() / 60
            ultima_actualizacion = fecha_ultima.isoformat() if fecha_ultima else None
        else:
            minutos_desde = None
            ultima_actualizacion = None

        if ultimo:
            dato = _filtrar_campos_elementales(ultimo)
            # created_at puede venir como fecha; normalizar a ISO
            if dato.get("created_at") is None and fecha_ultima:
                dato["created_at"] = fecha_ultima.isoformat()
            elif isinstance(dato.get("created_at"), datetime):
                dato["created_at"] = dato["created_at"].isoformat()
            power_state = ultimo.get("power_state")
            dato["power_state_texto"] = "on" if power_state == 1 else "off"
            dato["en_rango"] = _calcular_en_rango(ultimo.get("set_point"), ultimo.get("return_air"))
            en_defrost = _calcular_en_defrost(
                ultimo.get("set_point"),
                ultimo.get("temp_supply_1"),
                ultimo.get("return_air"),
                ultimo.get("evaporation_coil"),
            )
        else:
            dato = {k: None for k in _CAMPOS_ULTIMO_ESTADO}
            dato["power_state_texto"] = None
            dato["en_rango"] = None
            en_defrost = None

        dispositivos.append({
            "imei": imei,
            "estado_conexion": estado_conexion,
            "ultima_actualizacion": ultima_actualizacion,
            "minutos_desde_ultimo_dato": round(minutos_desde, 1) if minutos_desde is not None else None,
            "power_state_texto": dato.pop("power_state_texto"),
            "en_rango": dato.pop("en_rango"),
            "en_defrost": en_defrost,
            "ultimo_dato": dato,
        })

    # Resumen para tabla (todas las fechas/horas consideradas en GMT-5)
    online = sum(1 for d in dispositivos if d["estado_conexion"] == "online")
    wait = sum(1 for d in dispositivos if d["estado_conexion"] == "wait")
    offline = sum(1 for d in dispositivos if d["estado_conexion"] == "offline")
    en_defrost_count = sum(1 for d in dispositivos if d.get("en_defrost") is True)
    power_on_count = sum(1 for d in dispositivos if d.get("power_state_texto") == "on")
    power_off_count = sum(1 for d in dispositivos if d.get("power_state_texto") == "off")

    return {
        "resumen": {
            "total_dispositivos": len(dispositivos),
            "online": online,
            "wait": wait,
            "offline": offline,
            "en_defrost": en_defrost_count,
            "power_on": power_on_count,
            "power_off": power_off_count,
            "zona_horaria": "GMT-5",
        },
        "dispositivos": dispositivos,
    }

GMT5 = timezone(timedelta(hours=-5))


def _fecha_ultima_como_gmt5(fecha_ultima: Optional[datetime]) -> Optional[datetime]:
    """Interpreta la fecha almacenada (naive) como GMT-5 para comparar con ahora en GMT-5."""
    if fecha_ultima is None:
        return None
    if fecha_ultima.tzinfo is not None:
        return fecha_ultima
    return fecha_ultima.replace(tzinfo=GMT5)

def _calcular_estado_conexion(fecha_ultima: Optional[datetime]) -> str:
    """online <= 30 min, wait 30 min - 24 h, offline > 24 h. Fechas en GMT-5."""
    fecha_gmt5 = _fecha_ultima_como_gmt5(fecha_ultima)
    if fecha_gmt5 is None:
        return "offline"
    ahora = _ahora_gmt5()
    delta = ahora - fecha_gmt5
    minutos = delta.total_seconds() / 60
    if minutos <= 30:
        return "online"
    if minutos <= 24 * 60:
        return "wait"
    return "offline"

_CAMPOS_ULTIMO_ESTADO = [
    "temp_supply_1", "return_air", "evaporation_coil", "condensation_coil", "compress_coil_1",
    "co2_reading", "o2_reading", "cargo_1_temp", "cargo_2_temp", "cargo_3_temp", "cargo_4_temp",
    "power_kwh", "numero_alarma", "sp_ethyleno", "set_point_o2", "set_point_co2",
    "power_state", "capacity_load", "telemetria_id", "created_at", "longitud", "latitud", "set_point",
]

def _calcular_en_defrost(set_point: Any, temp_supply_1: Any, return_air: Any, evaporation_coil: Any) -> bool:
    """True si en_defrost."""
    try:
        sp = float(set_point)
        ts = float(temp_supply_1)
        ra = float(return_air)
        ec = float(evaporation_coil)
        return sp <= ts <= ra <= ec
    except (ValueError, TypeError):
        return False

def _calcular_en_rango(val: Any, set_point_val: Any, margen: float = 5.0) -> bool:
    """True si val está dentro de ±margen respecto a set_point."""
    try:
        v = float(val)
        sp = float(set_point_val)
        return abs(v - sp) <= margen
    except (ValueError, TypeError):
        return False

def _filtrar_campos_elementales(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Deja solo los campos elementales; fechas a ISO string."""
    out = {}
    for k in _CAMPOS_ULTIMO_ESTADO:
        v = doc.get(k)
        if isinstance(v, datetime):
            v = v.isoformat()
        out[k] = v
    return out

def _ahora_gmt5() -> datetime:
    """Ahora en GMT-5."""
    return datetime.now(GMT5)





