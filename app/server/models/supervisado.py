from typing import Optional,List
from datetime import  datetime
from pydantic import BaseModel, Field

class SupervisadoSchema(BaseModel):
    id :  Optional[int] |None =0
    fecha_creacion : Optional[datetime] |None = datetime.now()
    fecha_final : Optional[datetime] |None = None
    temperatura : Optional[float] | None =None
    sp_co2 : Optional[float] | None =None
    sp_etileno : Optional[int] | None =None
    sp_humedad : Optional[int] | None =None
    estado :  Optional[int] |None =1
    ultima_ejecucion : Optional[datetime] |None =None
    tipo : Optional[int] |None =2 #1 homogenizacion , 2 maduracion , 3 ventilacion y 4 cooling

    class Config:
        json_schema_extra = {
            "example": {
                "id":0,
                "fecha_creacion": "2024-08-17T01:43:11",
                "fecha_final": "2024-08-17T19:43:11",
                "temperatura": 15.40,
                "sp_co2": 5.00,
                "sp_etileno": 120,
                "sp_humedad": 90,
                "estado": 1,
                "ultima_ejecucion": "2024-08-17T16:43:11",
                "tipo": 2,

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

