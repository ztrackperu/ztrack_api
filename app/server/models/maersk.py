from typing import Optional,List
from datetime import  datetime
from pydantic import BaseModel, Field

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

class SolicitudGeneradorSchema(BaseModel):
    #device:str = Field(...)
    #ultima: str = Field(...)
    imei:str
    fechaI: Optional[str] | None ="0"
    fechaF: Optional[str] | None ="0"
    #page: Optional[int] | None =1
    #size: Optional[int] | None =5000
    #empresa: Optional[int] | None =22
    utc: Optional[int] | None =300
    
    class Config:
        json_schema_extra = {
            "example": {
                "fechaI": "2024-04-18T11:11:04",
                "fechaF": "2024-04-18T13:11:04", 
                "imei":"863576046753492"

            }
        }