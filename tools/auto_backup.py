
import shutil
import os
import datetime

def run_backup():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    backup_dir = f"backups/VIC_Backup_{timestamp}"
    
    # Archivos críticos
    targets = [
        "brain/datasets/training_data.jsonl",
        "brain/datasets/live_status.json",
        "reports/"
    ]
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        
    print(f"[*] Iniciando respaldo de Vertex Intelligence Core...")
    
    for item in targets:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.copytree(item, os.path.join(backup_dir, os.path.basename(item)))
            else:
                shutil.copy2(item, backup_dir)
    
    print(f"[+] Respaldo completado en: {backup_dir}")

if __name__ == "__main__":
    run_backup()