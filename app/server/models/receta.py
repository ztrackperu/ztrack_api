from typing import Optional,List
from datetime import  datetime
from pydantic import BaseModel, Field

class RecetaSchema(BaseModel):
    id :Optional[int] |None =0
    fecha_crea:Optional[datetime] |None = datetime.now()
    fecha_edit : Optional[datetime] |None =None
    user_crea : Optional[int] |None =0
    user_edit : Optional[int] |None =0
    temperatura_homogenizacion : float  = Field(...)
    humedad_homogenizacion : float  = Field(...)
    temperatura_ripener : float  = Field(...)
    etileno_ripener : float  = Field(...)
    co2_ripener : float  = Field(...)
    humedad_ripener : float  = Field(...)
    horas_ripener : float  = Field(...)
    ventilacion : float  = Field(...)
    temperatura_ventilacion : float  = Field(...)
    temperatura_producto : float  = Field(...)
    estado : Optional[int] |None =1
    nombre_receta : Optional[str] |None = "default"


    class Config:
        json_schema_extra = {
            "example": {
                "id":0,
                "temperatura_homogenizacion": 75.0,
                "humedad_homogenizacion": 85.0,
                "temperatura_ripener": 65.0,
                "etileno_ripener": 120.0,
                "co2_ripener": 3.0,
                "humedad_ripener": 90.0,
                "horas_ripener": 18.0,
                "ventilacion": 200.0,
                "temperatura_producto": 10.5,
                "temperatura_ventilacion" : 14,

                "nombre_receta": "Banano tropical"

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

