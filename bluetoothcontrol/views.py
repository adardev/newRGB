from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import serial
import serial.tools.list_ports
from time import sleep
import threading

# Configuración
SERIAL_PORTS = ['COM5', 'COM6']  # USB y Bluetooth
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
                sleep(2)  # Tiempo inicialización
                print(f"Conexión exitosa con {port}")
                return True
        except Exception as e:
            print(f"Error en {port}: {str(e)}")
    
    print("No se pudo conectar a ningún puerto")
    return False

# Intenta conectar al iniciar
conectar_arduino()

@csrf_exempt
def enviar_rgb(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            r = data.get('r', 0)
            g = data.get('g', 0)
            b = data.get('b', 0)
            
            comando = f"R{r},G{g},B{b}\n"
            print(f"Enviando: {comando.strip()}")
            
            # Intenta enviar
            if ser and ser.is_open:
                try:
                    with serial_lock:
                        ser.write(comando.encode())
                        sleep(0.1)  # Espera breve
                        return JsonResponse({
                            'status': 'success',
                            'message': 'Comando enviado',
                            'comando': comando.strip()
                        })
                except Exception as e:
                    print(f"Error al enviar: {str(e)}")
                    if conectar_arduino():  # Reintenta
                        return enviar_rgb(request)
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Error de conexión serial'
                    }, status=500)
            else:
                if conectar_arduino():
                    return enviar_rgb(request)
                return JsonResponse({
                    'status': 'error',
                    'message': 'Arduino no conectado'
                }, status=503)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'JSON inválido'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Método no permitido'
    }, status=405)

def index(request):
    return render(request, 'bluetoothcontrol/index.html')