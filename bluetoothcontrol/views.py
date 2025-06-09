from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import serial
import serial.tools.list_ports
from time import sleep
import threading

SERIAL_PORTS = ['COM5', 'COM7']
BAUDRATE = 9600
ser = None
serial_lock = threading.Lock()

def conectar_arduino():
    global ser
    for port in SERIAL_PORTS:
        try:
            with serial_lock:
                if ser and ser.is_open:
                    ser.close()
                ser = serial.Serial(port, BAUDRATE, timeout=2)
                sleep(2)
                print(f"✅ Conectado al puerto: {port}")
                return True
        except Exception as e:
            print(f"❌ Error en {port}: {str(e)}")
    print("⚠️ No se pudo conectar a ningún puerto.")
    return False

conectar_arduino()

@csrf_exempt
def enviar_rgb(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            r = data.get('r', 0)
            v = data.get('v', 1)
            d = data.get('d', 1)

            comando = f"{r},{v},{d}\n"
            if ser and ser.is_open:
                try:
                    with serial_lock:
                        ser.write(comando.encode())
                        sleep(0.1)
                        return JsonResponse({
                            'status': 'success',
                            'message': 'Comando enviado',
                            'comando': comando.strip()
                        })
                except Exception as e:
                    print(f"❌ Error al enviar: {str(e)}")
                    if conectar_arduino():
                        return enviar_rgb(request)
                    return JsonResponse({'status': 'error', 'message': 'Error de conexión serial'}, status=500)
            else:
                if conectar_arduino():
                    return enviar_rgb(request)
                return JsonResponse({'status': 'error', 'message': 'Arduino no conectado'}, status=503)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def index(request):
    return render(request, 'bluetoothcontrol/index.html')

#Code del UBIDOTS integrador

import requests

UBIDOTS_TOKEN = "BBUS-zJ4HFFCnJRWVC82VHNXUSi73aRLKil"  # Sustituye con tu token de Ubidots
DEVICE_LABEL = "arduino"  # O el nombre de tu dispositivo

payload = {
    "Temperatura": 25.5,
    "HumedadAmbiente": 60.0,
    "HumedadTierra": 60.0,
    "Foco": 60.0,
    "Ventilador": 60.0,
    "Bomba": 60.0
}

url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"
headers = {
    "X-Auth-Token": UBIDOTS_TOKEN,
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status:", response.status_code)
print("Respuesta:", response.text)

#Code para transferir de ARDUINO a DJANGO

from django.http import JsonResponse

def recibir_datos(request):
    temp = request.GET.get("temp")
    hum_amb = request.GET.get("hum_amb")
    hum_tierra = request.GET.get("hum_tierra")
    foco = request.GET.get("foco")
    ventilador = request.GET.get("ventilador")
    bomba = request.GET.get("bomba")

    # Aquí puedes guardar en base de datos, registrar, etc.
    print(f"TEMP: {temp} | HAMB: {hum_amb} | HT: {hum_tierra} | F:{foco} V:{ventilador} B:{bomba}")

    return JsonResponse({"status": "ok"})
