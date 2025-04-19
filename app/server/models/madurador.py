from typing import Optional,List
from pydantic import BaseModel, Field
from datetime import  datetime

class IntegracionZtrackSchema(BaseModel):
    temp_supply_1: Optional[float] | None =None
    temp_supply_2: Optional[float] | None =None
    return_air: Optional[float] | None =None
    evaporation_coil: Optional[float] | None =None
    condensation_coil: Optional[float] | None =None
    compress_coil_1: Optional[float] | None =None
    compress_coil_2: Optional[float] | None =None
    ambient_air: Optional[float] | None =None
    cargo_1_temp: Optional[float] | None =None
    cargo_2_temp: Optional[float] | None =None
    cargo_3_temp: Optional[float] | None =None
    cargo_4_temp: Optional[float] | None =None
    relative_humidity: Optional[float] | None =None
    avl: Optional[float] | None =None
    suction_pressure: Optional[float] | None =None
    discharge_pressure: Optional[float] | None =None
    line_voltage: Optional[float] | None =None
    line_frequency: Optional[float] | None =None
    consumption_ph_1: Optional[float] | None =None
    consumption_ph_2: Optional[float] | None =None
    consumption_ph_3: Optional[float] | None =None
    co2_reading: Optional[float] | None =None
    o2_reading: Optional[float] | None =None
    evaporator_speed: Optional[float] | None =None
    condenser_speed: Optional[float] | None =None
    battery_voltage: Optional[float] | None =None
    power_kwh: Optional[float] | None =None
    power_trip_reading: Optional[float] | None =None
    power_trip_duration: Optional[float] | None =None
    suction_temp: Optional[float] | None =None
    discharge_temp: Optional[float] | None =None
    supply_air_temp: Optional[float] | None =None
    return_air_temp: Optional[float] | None =None
    dl_battery_temp: Optional[float] | None =None
    dl_battery_charge: Optional[float] | None =None
    power_consumption: Optional[float] | None =None
    power_consumption_avg: Optional[float] | None =None
    suction_pressure_2: Optional[float] | None =None
    suction_temp_2: Optional[float] | None =None
    alarm_present: Optional[float] | None =None
    set_point: Optional[float] | None =None
    capacity_load: Optional[float] | None =None
    power_state: Optional[float] | None =None
    controlling_mode: Optional[float] | None =None
    humidity_control: Optional[float] | None =None
    humidity_set_point: Optional[float] | None =None
    fresh_air_ex_mode: Optional[float] | None =None
    fresh_air_ex_rate: Optional[float] | None =None
    fresh_air_ex_delay: Optional[float] | None =None
    set_point_o2: Optional[float] | None =None
    set_point_co2: Optional[float] | None =None
    defrost_term_temp: Optional[float] | None =None
    defrost_interval: Optional[float] | None =None
    water_cooled_conde: Optional[float] | None =None
    usda_trip: Optional[float] | None =None
    evaporator_exp_valve: Optional[float] | None =None
    suction_mod_valve: Optional[float] | None =None
    hot_gas_valve: Optional[float] | None =None
    economizer_valve: Optional[float] | None =None
    numero_alarma: Optional[float] | None =None
    alarma_01: Optional[float] | None =None
    alarma_02: Optional[float] | None =None
    alarma_03: Optional[float] | None =None
    alarma_04: Optional[float] | None =None
    alarma_05: Optional[float] | None =None
    alarma_06: Optional[float] | None =None
    alarma_07: Optional[float] | None =None
    alarma_08: Optional[float] | None =None
    alarma_09: Optional[float] | None =None
    alarma_10: Optional[float] | None =None
    lecturas_erradas: Optional[str] | None =None
    imei: Optional[str] | None =None
    ip: Optional[str] | None =None
    device: Optional[str] | None =None
    fecha: Optional[datetime] | None =None
    created_at: Optional[datetime] | None =None
    telemetria_id: Optional[float] | None =None
    sp_ethyleno: Optional[float] | None =None
    stateProcess: Optional[float] | None =None
    inyeccion_pwm: Optional[float] | None =None
    longitud: Optional[float] | None =None
    latitud: Optional[float] | None =None
    ethylene: Optional[float] | None =None
    class Config:
        json_schema_extra = {
            "example": {
                "device": "ZGRU9015808",

            }
        }




class SolicitudMaduradorSchema(BaseModel):
    device:str = Field(...)
    ultima: str = Field(...)
    fechaI: Optional[str] | None ="0"
    fechaF: Optional[str] | None ="0"
    page: Optional[int] | None =1
    size: Optional[int] | None =3200
    empresa: Optional[int] | None =22
    class Config:
        json_schema_extra = {
            "example": {
                "device": "ZGRU9015808",
                "ultima": "2024-05-18T10:11:04",
                "fechaI": "2024-04-18T11:11:04",
                "fechaF": "2024-04-18T13:11:04", 
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

class DatosMadurador(BaseModel):
    id:int = Field(...)
    return_air: float = Field(...)
