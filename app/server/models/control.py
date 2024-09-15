from typing import Optional,List
from datetime import  datetime
from pydantic import BaseModel, Field

class ControlSchema(BaseModel):
    
    imei :str = Field(...)
    estado : Optional[int] |None =1
    fecha_creacion : Optional[datetime] |None = datetime.now()
    comando : Optional[str] |None = "No especificado"
    dispositivo : Optional[str] |None = "FAIL"
    ultimo_evento : Optional[str] |None = "SIN REGISTRO "
    user :Optional[str] |None ="default"
    status : Optional[int] |None =1
    humedad :int =Field(...)
    co2 :float =Field(...)
    temperatura :float =Field(...)
    etileno :int =Field(...)
    horas :int =Field(...)
    #incio de control +10 minutos de proceso
    inicio_control :Optional[datetime] |None =None
    fin_control :Optional[datetime] |None =None
    tiempo_inicio_cero :Optional[datetime] |None =None
    tiempo_continuo_cero :Optional[datetime] |None =None
    veces_cero :Optional[int] |None =0
    veces_reset :Optional[int] |None =0
    tiempo_desface_inicio :Optional[datetime] |None =None
    tiempo_desface_continuo :Optional[datetime] |None =None
    hora_ultima_inyeccion : Optional[datetime] |None =None
    lista_evento : Optional[List] |None =None
    titulo : Optional[str] |None = "RIPENING MODE ACTIVATED, PLEASE WAIT FOR THE PROCESS TO COMPLETE "
    descripcion : str = Field(...)
    flujometro : str = Field(...)
    producto : str = Field(...)
    class Config:
        json_schema_extra = {
            "example": {
                "imei":"123456789123458",
                #"comando": "MANUAL_RIPE(17.80,90,120,5.00)",
                "humedad":90,
                "co2":5,
                "temperatura":18.5,
                "etileno":120,
                "horas":24,
                "descripcion" : "PROCESO PARA QUIMICA SUIZA 12/12/2024",
                "flujometro" : "2",
                "producto":"PLATANO COLOMBIANO "

            }
        }

#respuesta cuando todo esta bien
def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }

#respuesta cuando algo sale mal 
def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}

