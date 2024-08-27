from typing import Optional,List
from datetime import  datetime
from pydantic import BaseModel, Field

class ProcesoSchema(BaseModel):
    id :Optional[int] |None =0
    fecha_crea:Optional[datetime] |None = datetime.now()
    fecha_edit : Optional[datetime] |None =None
    user_crea : Optional[int] |None =0
    user_edit : Optional[int] |None =0
    temperatura_homogenizacion : Optional[float] | None =20
    humedad_homogenizacion : Optional[float] | None =80
    temperatura_ripener : Optional[float] | None =20
    etileno_ripener : Optional[float] | None =120
    co2_ripener : Optional[float] | None =3.0
    humedad_ripener : Optional[float] | None =80
    horas_ripener : Optional[float] | None =24
    ventilacion : Optional[float] | None =200
    temperatura_ventilacion : Optional[float] | None =13
    temperatura_producto : Optional[float] | None =13
    estado : Optional[int] |None =1
    nombre_receta : Optional[str] |None = "default"
    id_receta :Optional[int] |None =1
    horas_homogenizacion :float  = Field(...)
    horas_maduracion : float  = Field(...)
    horas_ventilacion : float  = Field(...)
    horas_cooling : float  = Field(...)
    inicio_horas_homogenizacion :Optional[datetime] |None =None
    fin_horas_homogenizaion :Optional[datetime] |None =None
    inicio_horas_maduracion:Optional[datetime] |None =None
    fin_horas_maduracion :Optional[datetime] |None =None
    inicio_horas_ventilacion : Optional[datetime] |None =None
    fin_horas_ventilacion : Optional[datetime] |None =None
    inicio_horas_cooling :Optional[datetime] |None =None
    fin_horas_cooling :Optional[datetime] |None =None

    class Config:
        json_schema_extra = {
            "example": {
                "id":0,
                "horas_homogenizacion": 1.0,
                "horas_maduracion":2.0,
                "horas_ventilacion": 3.0,
                "horas_cooling": 4.0,
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

