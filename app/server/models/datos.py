from typing import Optional,List
from datetime import  datetime
from pydantic import BaseModel, Field

class DatosSchema(BaseModel):
    i :str = Field(...)
    d: Optional[str] | None =None
    d1: Optional[str] | None =None
    d2: Optional[str] | None =None
    d3: Optional[str] | None =None
    d4: Optional[str] | None =None
    d5: Optional[str] | None =None
    d6: Optional[str] | None =None
    d7: Optional[str] | None =None
    d8: Optional[str] | None =None
    d9: Optional[str] | None =None
    d10: Optional[str] | None =None

    g: Optional[str] | None =None
    #a: Optional[str] | None =None
    c: Optional[str] | None =None

    estado: Optional[int] | None =1
    #fecha: Optional[datetime] | None =datetime.now()
    #size: Optional[int] | None =3200
    class Config:
        json_schema_extra = {
            "example": {
                "i":"aqui av el IMEI",
                "d": "Aqui va los datos d de los sensores",
                "d1": "Aqui va los datos d1 de los sensores",
                "d2": "Aqui va los datos d2 de los sensores",
                "d3": "Aqui va los datos d3 de los sensores",
                "d4": "Aqui va los datos d4 de los sensores",
                "d5": "Aqui va los datos d5 de los sensores",
                "d6": "Aqui va los datos d6 de los sensores",
                "d7": "Aqui va los datos d7 de los sensores",
                "d8": "Aqui va los datos d8 de los sensores",
                "d9": "Aqui va los datos d9 de los sensores",
                "d10": "Aqui va los datos d10 de los sensores",

                "g": "Aqui va el GPS",
                #"a": "Aqui va las alarmas",
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

