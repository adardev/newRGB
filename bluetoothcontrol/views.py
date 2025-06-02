from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import serial
import serial.tools.list_ports
from time import sleep
import threading

SERIAL_PORTS = ['COM3']
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
def mover_angulo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            angulo = data.get('angulo')

            if not isinstance(angulo, int) or not (0 <= angulo <= 180):
                return JsonResponse({'status': 'error', 'message': 'Ángulo fuera de rango (0-180)'}, status=400)

            comando = f"A{angulo}\n"
            with serial_lock:
                if ser and ser.is_open:
                    ser.write(comando.encode())
                    sleep(0.1)
                    return JsonResponse({'status': 'success', 'message': f'Servo movido a {angulo}°'})
                elif conectar_arduino():
                    return mover_angulo(request)
                else:
                    return JsonResponse({'status': 'error', 'message': 'Arduino no conectado'}, status=503)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@csrf_exempt
def secuencia(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            angulos = data.get('secuencia', [])

            if not isinstance(angulos, list) or len(angulos) != 4:
                return JsonResponse({'status': 'error', 'message': 'Se requieren exactamente 4 ángulos'}, status=400)
            if any(not isinstance(a, int) or not (0 <= a <= 180) for a in angulos):
                return JsonResponse({'status': 'error', 'message': 'Ángulos inválidos (0-180)'}, status=400)

            comando = "S" + ",".join(str(a) for a in angulos) + "\n"
            with serial_lock:
                if ser and ser.is_open:
                    ser.write(comando.encode())
                    sleep(0.1)
                    return JsonResponse({'status': 'success', 'message': 'Secuencia enviada'})
                elif conectar_arduino():
                    return secuencia(request)
                else:
                    return JsonResponse({'status': 'error', 'message': 'Arduino no conectado'}, status=503)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def index(request):
    return render(request, 'bluetoothcontrol/index.html')
