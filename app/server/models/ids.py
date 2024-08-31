from typing import Optional,List
from datetime import  datetime
from pydantic import BaseModel, Field

class IdSchema(BaseModel):

    receta_id : Optional[int] |None =0
    proceso_id : Optional[int] |None =0
    comando_id : Optional[int] |None =0
    supervisado_id : Optional[int] |None =0


    class Config:
        json_schema_extra = {
            "example": {
                "receta_id": 75.0,
                "proceso_id": 85.0,
                "comando_id": 65.0
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

