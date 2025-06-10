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