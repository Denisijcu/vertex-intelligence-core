import json
import os

# Aseguramos que la ruta sea relativa al proyecto
DB_PATH = os.path.join("brain", "datasets", "live_status.json")

def update_db(key, value):
    data = get_db() # Usamos la función segura para leer
    data[key] = value
    
    # Creamos la carpeta si no existe
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    with open(DB_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def get_db():
    if not os.path.exists(DB_PATH):
        return {}
    
    try:
        with open(DB_PATH, 'r') as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        # Si el archivo está corrupto o bloqueado, devolvemos un dict vacío
        return {}