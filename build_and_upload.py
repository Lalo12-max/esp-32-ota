import subprocess
import requests
import os
import shutil
from datetime import datetime

def run_command(cmd, cwd=None):
    """Ejecuta un comando y retorna el resultado"""
    print(f"Ejecutando: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def upload_firmware(firmware_path, server_url="http://localhost:8000"):
    """Sube el firmware al servidor OTA"""
    try:
        with open(firmware_path, 'rb') as f:
            files = {'firmware': f}
            response = requests.post(f"{server_url}/upload", files=files)
            if response.status_code == 200:
                print(f"Firmware subido exitosamente: {response.json()}")
                return True
            else:
                print(f"Error subiendo firmware: {response.text}")
                return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("=== ESP32 OTA Build and Upload Script ===")
    
    # 1. Compilar el proyecto
    print("\n1. Compilando proyecto...")
    if not run_command("idf.py build"):
        print("Error en la compilación")
        return
    
    # 2. Copiar firmware compilado
    firmware_source = "build/esp32_ota_example.bin"
    firmware_dest = "esp32_ota_firmware.bin"
    
    if os.path.exists(firmware_source):
        shutil.copy2(firmware_source, firmware_dest)
        print(f"Firmware copiado a {firmware_dest}")
    else:
        print(f"No se encontró el firmware en {firmware_source}")
        return
    
    # 3. Subir al servidor OTA
    print("\n2. Subiendo firmware al servidor OTA...")
    if upload_firmware(firmware_dest):
        print("¡Firmware listo para OTA!")
    else:
        print("Error subiendo firmware")
    
    print("\n=== Proceso completado ===")
    print("Ahora puedes:")
    print("1. Flashear el firmware inicial: idf.py -p PUERTO flash monitor")
    print("2. El ESP32 se conectará a WiFi y descargará la actualización")
    print("3. Los logs se mostrarán en el monitor serie")

if __name__ == "__main__":
    main()