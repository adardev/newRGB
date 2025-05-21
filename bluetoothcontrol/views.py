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
                with serial_lock:
                    ser.write(comando.encode())
                    sleep(0.1)
                return JsonResponse({
                    'status': 'success',
                    'message': 'Comando enviado',
                    'comando': comando.strip()
                })
            else:
                if conectar_arduino():
                    return enviar_rgb(request)
                return JsonResponse({'status': 'error', 'message': 'Arduino no conectado'}, status=503)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@csrf_exempt
def mover_angulo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            angulo = int(data.get('angulo'))

            if 0 <= angulo <= 180:
                comando = f"A{angulo}\n"
                if ser and ser.is_open:
                    with serial_lock:
                        ser.write(comando.encode())
                        sleep(0.1)
                    return JsonResponse({
                        'status': 'success',
                        'message': f'Servo movido a {angulo}°',
                        'comando': comando.strip()
                    })
                else:
                    if conectar_arduino():
                        return mover_angulo(request)
                    return JsonResponse({'status': 'error', 'message': 'Arduino no conectado'}, status=503)
            else:
                return JsonResponse({'status': 'error', 'message': 'Ángulo fuera de rango (0-180)'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@csrf_exempt
def secuencia(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            secuencia = data.get('secuencia', [])
            if not isinstance(secuencia, list) or len(secuencia) != 4:
                return JsonResponse({'status': 'error', 'message': 'Se deben proporcionar exactamente 4 ángulos'}, status=400)

            for ang in secuencia:
                if not (0 <= int(ang) <= 180):
                    return JsonResponse({'status': 'error', 'message': 'Todos los ángulos deben estar entre 0 y 180'}, status=400)

            comando = "S" + ",".join(str(a) for a in secuencia) + "\n"  # Por ejemplo: S30,60,90,120
            if ser and ser.is_open:
                with serial_lock:
                    ser.write(comando.encode())
                    sleep(0.1)
                return JsonResponse({
                    'status': 'success',
                    'message': 'Secuencia enviada',
                    'comando': comando.strip()
                })
            else:
                if conectar_arduino():
                    return secuencia(request)
                return JsonResponse({'status': 'error', 'message': 'Arduino no conectado'}, status=503)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def index(request):
    return render(request, 'bluetoothcontrol/index.html')