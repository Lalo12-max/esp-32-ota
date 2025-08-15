import os
import shutil
import subprocess
import requests
import json
from datetime import datetime

class OTADeployment:
    def __init__(self):
        self.project_dir = os.getcwd()
        self.build_dir = os.path.join(self.project_dir, 'build')
        self.firmware_dir = os.path.join(self.project_dir, 'firmware')
        self.binary_name = 'mqtt_ssl.bin'
        self.firmware_name = 'esp32_ota_firmware.bin'
        
    def build_project(self):
        """Compila el proyecto ESP32"""
        print("🔨 Compilando proyecto ESP32...")
        try:
            result = subprocess.run(['idf.py', 'build'], 
                                  capture_output=True, text=True, cwd=self.project_dir)
            if result.returncode == 0:
                print("✅ Compilación exitosa")
                return True
            else:
                print(f"❌ Error en compilación: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error ejecutando idf.py: {e}")
            return False
    
    def copy_firmware(self):
        """Copia el firmware compilado al directorio de firmware"""
        print("📁 Copiando firmware...")
        
        # Crear directorio firmware si no existe
        os.makedirs(self.firmware_dir, exist_ok=True)
        
        source_path = os.path.join(self.build_dir, self.binary_name)
        dest_path = os.path.join(self.firmware_dir, self.firmware_name)
        
        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
            print(f"✅ Firmware copiado: {dest_path}")
            return True
        else:
            print(f"❌ No se encontró el archivo: {source_path}")
            return False
    
    def start_local_server(self):
        """Inicia el servidor OTA local"""
        print("🚀 Iniciando servidor OTA local...")
        try:
            subprocess.Popen(['python', 'ota_server.py'], cwd=self.project_dir)
            print("✅ Servidor iniciado en http://localhost:8000")
            return True
        except Exception as e:
            print(f"❌ Error iniciando servidor: {e}")
            return False
    
    def deploy_to_railway(self):
        """Despliega a Railway (requiere railway CLI)"""
        print("🚂 Desplegando a Railway...")
        try:
            # Verificar si railway CLI está instalado
            subprocess.run(['railway', '--version'], capture_output=True, check=True)
            
            # Desplegar
            result = subprocess.run(['railway', 'up'], 
                                  capture_output=True, text=True, cwd=self.project_dir)
            if result.returncode == 0:
                print("✅ Desplegado exitosamente a Railway")
                return True
            else:
                print(f"❌ Error en despliegue: {result.stderr}")
                return False
        except subprocess.CalledProcessError:
            print("❌ Railway CLI no está instalado. Instala con: npm install -g @railway/cli")
            return False
        except Exception as e:
            print(f"❌ Error en despliegue: {e}")
            return False
    
    def full_deployment(self, deploy_cloud=False):
        """Proceso completo de deployment"""
        print("🎯 Iniciando proceso completo de deployment...")
        print(f"📅 Timestamp: {datetime.now().isoformat()}")
        
        steps = [
            ("Compilar proyecto", self.build_project),
            ("Copiar firmware", self.copy_firmware),
        ]
        
        if deploy_cloud:
            steps.append(("Desplegar a Railway", self.deploy_to_railway))
        else:
            steps.append(("Iniciar servidor local", self.start_local_server))
        
        for step_name, step_func in steps:
            print(f"\n📋 {step_name}...")
            if not step_func():
                print(f"❌ Falló en: {step_name}")
                return False
        
        print("\n🎉 ¡Deployment completado exitosamente!")
        return True

if __name__ == "__main__":
    import sys
    
    deployer = OTADeployment()
    
    # Verificar argumentos
    deploy_cloud = '--cloud' in sys.argv or '-c' in sys.argv
    
    print("=" * 50)
    print("🚀 ESP32 OTA Deployment Automation")
    print("=" * 50)
    
    if deploy_cloud:
        print("☁️  Modo: Despliegue en la nube (Railway)")
    else:
        print("🏠 Modo: Servidor local")
    
    deployer.full_deployment(deploy_cloud=deploy_cloud)


# Agregar método para Render
def deploy_to_render(self):
    """Instrucciones para desplegar a Render"""
    print("🎨 Para desplegar a Render:")
    print("1. Sube tu código a GitHub")
    print("2. Ve a render.com y crea una cuenta")
    print("3. Conecta tu repositorio")
    print("4. Configura como Web Service")
    print("5. Build Command: pip install -r requirements.txt")
    print("6. Start Command: python ota_server.py")
    print("✅ Render es 100% gratuito para siempre")
    return True