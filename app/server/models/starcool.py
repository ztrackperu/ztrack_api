from typing import Optional,List
from datetime import  datetime
from pydantic import BaseModel, Field

class StarcoolSchema(BaseModel):
    i :str = Field(...)
    d00: Optional[str] | None =None
    d01: Optional[str] | None =None
    d02: Optional[str] | None =None
    d03: Optional[str] | None =None
    d04: Optional[str] | None =None
    gps: Optional[str] | None =None
    estado: Optional[int] | None =1
    #fecha: Optional[datetime] | None =datetime.now()
    #size: Optional[int] | None =3200
    class Config:
        json_schema_extra = {
            "example": {
                "i":"aqui av el IMEI",
                "d00": "Aqui va los datos d de los sensores starcool",
                "d01": "Aqui va los datos d1 de los sensores starcool",
                "d02": "Aqui va los datos d2 de los sensores starcool",
                "d03": "Aqui va los datos d3 de los sensores starcool",
                "d04": "Aqui va los datos d4 de los sensores starcool",
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

