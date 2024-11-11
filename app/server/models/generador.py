from typing import Optional,List
from datetime import  datetime
from pydantic import BaseModel, Field

class GeneradorSchema(BaseModel):
    i :str = Field(...)
    d00: Optional[str] | None =None
    d01: Optional[str] | None =None
    d02: Optional[str] | None =None
    d03: Optional[str] | None =None
    d04: Optional[str] | None =None
    d05: Optional[str] | None =None
    r01: Optional[str] | None =None
    r02: Optional[str] | None =None
    gps: Optional[str] | None =None
    estado: Optional[int] | None =1
    #fecha: Optional[datetime] | None =datetime.now()
    #size: Optional[int] | None =3200
    class Config:
        json_schema_extra = {
            "example": {
                "i":"aqui av el IMEI",
                "d00": "Aqui va los datos d de los sensores",
                "d01": "Aqui va los datos d1 de los sensores",
                "d02": "Aqui va los datos d2 de los sensores",
                "d03": "Aqui va los datos d3 de los sensores",
                "d04": "Aqui va los datos d4 de los sensores",
                "d05": "Aqui va los datos d5 de los sensores",
                "r01": "Aqui va los datos d6 de los sensores",
                "r02": "Aqui va los datos d7 de los sensores",
                "gps": "Aqui va el GPS",
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

