from typing import Optional,List
from datetime import  datetime
from pydantic import BaseModel, Field

class DatosSchema(BaseModel):
    i :str = Field(...)
    d: Optional[str] | None =None
    g: Optional[str]  =None
    a: Optional[str] | None =None
    c: Optional[str] | None =None

    estado: Optional[int] | None =1
    #fecha: Optional[datetime] | None =datetime.now()
    #size: Optional[int] | None =3200
    class Config:
        json_schema_extra = {
            "example": {
                "i":"aqui av el IMEI",
                "d": "Aqui va los datos de los sensores",
                "g": "Aqui va el GPS",
                "a": "Aqui va las alarmas",
                "c": "Aqui va  la configuracion",
                "estado": 1,
                #"fecha": "2024-04-18T11:11:04",
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

