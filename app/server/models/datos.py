from typing import Optional,List
from datetime import  datetime
from pydantic import BaseModel, Field

class DatosSchema(BaseModel):
    dato: str = Field(...)
    estado: Optional[int] | None =1
    #fecha: Optional[datetime] | None =datetime.now()
    #size: Optional[int] | None =3200
    class Config:
        json_schema_extra = {
            "example": {
                "d": "Aqui va todo lo que se necesita insertar",
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

