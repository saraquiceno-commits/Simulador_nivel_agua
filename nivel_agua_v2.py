# Simulador de nivel de agua - Versión final
import rx
from rx import operators as ops
from rx.scheduler import ThreadPoolScheduler
import random
import time

nivel_actual = 50.0  # Nivel inicial en %
bomba_activa = False  # Estado inicial de la bomba

scheduler = ThreadPoolScheduler()

def simular_evento(_):
    global nivel_actual, bomba_activa

    # Simular evento aleatorio de entrada o salida
    evento = random.choice(["entrada", "salida"])
    cambio = random.uniform(1, 5)

    if evento == "entrada" and nivel_actual < 100:
        nivel_actual += cambio
    elif evento == "salida" and nivel_actual > 0:
        nivel_actual -= cambio

    # Asegurar que esté en el rango 0–100%
    nivel_actual = max(0, min(100, nivel_actual))

    # Control de bomba solo si cambia de estado
    if nivel_actual >= 80 and bomba_activa:
        bomba_activa = False
        print(f" Nivel de agua: {nivel_actual:.2f}% — ¡Detener bomba!")
    elif nivel_actual <= 20 and not bomba_activa:
        bomba_activa = True
        print(f" Nivel de agua: {nivel_actual:.2f}% — ¡Activar bomba!")
    else:
        estado = "ENCENDIDA" if bomba_activa else "APAGADA"
        print(f"Nivel actual: {nivel_actual:.2f}% | Bomba: {estado}")

# Ejecutar la simulación cada segundo
rx.interval(1.0).pipe(
    ops.observe_on(scheduler)
).subscribe(simular_evento)

print(" Iniciando simulación de nivel de agua con control de bomba...")
time.sleep(15)
print("Fin de la simulación.")


