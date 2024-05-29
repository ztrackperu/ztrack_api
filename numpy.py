from datetime import datetime
import numpy as np

def agregar_datos_por_intervalo(json_data, interval_minutes=10):
    # Extraer los datos del JSON
    data = json_data["graph"]
    created_at = data["created_at"]["data"]
    return_air = data["return_air"]["data"]
    
    # Convertir las fechas a objetos datetime
    created_at = [datetime.fromisoformat(date_str) for date_str in created_at]
    
    # Inicializar variables para el bucle
    current_time = created_at[0]
    current_interval_end = current_time + timedelta(minutes=interval_minutes)
    current_array = []
    final_data = []
    last_return_air = None
    
    # Iterar sobre los datos
    for time, ra in zip(created_at, return_air):
        # Si estamos dentro del intervalo actual
        if time < current_interval_end:
            # Si es el primer elemento o la variación de return_air es superior al 5%
            if last_return_air is None or (last_return_air * 0.05) < abs(ra - last_return_air):
                current_array.append({"time": time.isoformat(), "return_air": ra})
            last_return_air = ra
        else:
            # Agregar el array actual al resultado final
            final_data.append(current_array)
            # Iniciar un nuevo array para el nuevo intervalo
            current_array = [{"time": time.isoformat(), "return_air": ra}]
            # Actualizar el tiempo del nuevo intervalo
            current_time = time
            current_interval_end = current_time + timedelta(minutes=interval_minutes)
            last_return_air = ra
    
    # Agregar el último intervalo al resultado final
    final_data.append(current_array)
    
    return final_data