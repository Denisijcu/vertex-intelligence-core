import os
import json
from core.database import update_db

def ingest_all_writeups():
    raw_path = "brain/datasets/raw_writeups/"
    training_path = "brain/datasets/training_data.jsonl"
    
    # Aseguramos que existan las rutas
    if not os.path.exists(raw_path):
        os.makedirs(raw_path)
    
    print(f"[*] Escaneando nuevos datos en {raw_path}...")
    
    writeups_ingested = 0
    with open(training_path, "a", encoding="utf-8") as f_out:
        for filename in os.listdir(raw_path):
            if filename.endswith(".md") or filename.endswith(".txt"):
                file_path = os.path.join(raw_path, filename)
                with open(file_path, "r", encoding="utf-8") as f_in:
                    content = f_in.read()
                    # Creamos un bloque de datos para el entrenamiento/RAG
                    entry = {
                        "source": filename,
                        "content": content,
                        "timestamp": str(os.path.getmtime(file_path))
                    }
                    f_out.write(json.dumps(entry) + "\n")
                    writeups_ingested += 1
                
                # Opcional: mover el archivo a una carpeta de 'procesados'
                print(f"[+] '{filename}' indexado correctamente.")

    # Actualizar la base de datos para que el Dashboard lo sepa
    update_db("system_memory", {
        "files_indexed": writeups_ingested,
        "last_update": str(os.getpid())
    })
    print(f"--- Proceso completado. {writeups_ingested} lecciones aprendidas ---")

if __name__ == "__main__":
    ingest_all_writeups()