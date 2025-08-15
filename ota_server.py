from flask import Flask, send_file, jsonify, request
import os
import csv
from datetime import datetime
import hashlib

app = Flask(__name__)

# Configuración
FIRMWARE_DIR = 'firmware'
CSV_FILE = 'firmware_versions.csv'
PORT = 8000

# Crear directorio de firmware si no existe
if not os.path.exists(FIRMWARE_DIR):
    os.makedirs(FIRMWARE_DIR)

# Crear CSV si no existe
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'version', 'filename', 'size_bytes', 'md5_hash', 'download_count'])

def log_firmware_info(filename):
    """Registra información del firmware en CSV"""
    filepath = os.path.join(FIRMWARE_DIR, filename)
    if os.path.exists(filepath):
        # Calcular MD5
        with open(filepath, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        
        # Obtener tamaño
        size = os.path.getsize(filepath)
        
        # Escribir en CSV
        with open(CSV_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().isoformat(),
                '1.0.0',  # Versión por defecto
                filename,
                size,
                file_hash,
                0  # Contador inicial
            ])

def update_download_count(filename):
    """Actualiza el contador de descargas"""
    rows = []
    with open(CSV_FILE, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    # Actualizar contador para el archivo más reciente
    for i in range(len(rows)-1, 0, -1):  # Buscar desde el final
        if len(rows[i]) > 1 and rows[i][2] == filename:
            rows[i][5] = str(int(rows[i][5]) + 1)
            break
    
    # Escribir de vuelta
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

@app.route('/')
def index():
    return jsonify({
        'message': 'ESP32 OTA Server',
        'endpoints': {
            'firmware': '/firmware/<filename>',
            'upload': '/upload',
            'versions': '/versions'
        }
    })

@app.route('/firmware/<filename>')
def download_firmware(filename):
    """Endpoint para descargar firmware"""
    filepath = os.path.join(FIRMWARE_DIR, filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'Firmware not found'}), 404
    
    # Actualizar contador de descargas
    update_download_count(filename)
    
    print(f"[OTA] Serving firmware: {filename}")
    return send_file(filepath, as_attachment=True, download_name=filename)

@app.route('/upload', methods=['POST'])
def upload_firmware():
    """Endpoint para subir firmware"""
    if 'firmware' not in request.files:
        return jsonify({'error': 'No firmware file provided'}), 400
    
    file = request.files['firmware']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.endswith('.bin'):
        filename = file.filename
        filepath = os.path.join(FIRMWARE_DIR, filename)
        file.save(filepath)
        
        # Registrar en CSV
        log_firmware_info(filename)
        
        return jsonify({
            'message': 'Firmware uploaded successfully',
            'filename': filename,
            'download_url': f'http://localhost:{PORT}/firmware/{filename}'
        })
    
    return jsonify({'error': 'Invalid file type. Only .bin files allowed'}), 400

@app.route('/versions')
def get_versions():
    """Endpoint para ver versiones disponibles"""
    versions = []
    
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            versions = list(reader)
    
    return jsonify(versions)

# Agregar al final del archivo, reemplazar la línea app.run:
if __name__ == '__main__':
    print(f"\n=== ESP32 OTA Server ===")
    print(f"Server running on: http://localhost:{PORT}")
    print(f"Firmware directory: {os.path.abspath(FIRMWARE_DIR)}")
    print(f"CSV log file: {os.path.abspath(CSV_FILE)}")
    print(f"\nEndpoints:")
    print(f"  - GET  /                    : Server info")
    print(f"  - GET  /firmware/<filename> : Download firmware")
    print(f"  - POST /upload              : Upload firmware")
    print(f"  - GET  /versions            : List versions")
    print(f"\nTo upload firmware: curl -X POST -F 'firmware=@your_firmware.bin' http://localhost:{PORT}/upload")
    print(f"="*50)
    
    # Para Render, usar PORT del environment
    port = int(os.environ.get('PORT', PORT))
    app.run(host='0.0.0.0', port=port, debug=False)