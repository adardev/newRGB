import serial
import requests

arduino = serial.Serial('COM3', 9600)  # Ajusta COM3 según tu sistema
url = "http://127.0.0.1:8000/api/sensores/"  # O IP pública

while True:
    try:
        line = arduino.readline().decode().strip()
        print("Recibido:", line)

        payload = dict(x.split('=') for x in line.split('&'))
        print("Enviando a servidor:", payload)

        response = requests.get(url, params=payload)
        print("Estado servidor:", response.status_code)

    except Exception as e:
        print("Error:", e)