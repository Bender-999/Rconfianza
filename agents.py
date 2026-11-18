# multistart.py
import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor

import simulador
import Optimizador

# Configuración común a todas las tareas. Cada proceso trabajador tiene su propia copia,
# que rellena _preparar_trabajador al arrancar.
_cfg = None


def _preparar_trabajador(cfg):
    """Se ejecuta UNA vez en cada proceso trabajador, antes de recibir tareas."""
    global _cfg
    _cfg = cfg
    simulador.cargar()          # cada proceso necesita su propia instancia de la FMU


def _tarea(x0):
    """Una tarea: optimiza desde x0 con la configuración común."""
    c = _cfg
    # ↓ ÚNICA línea que depende de tu Optimizador.min: el orden tiene que ser el de su definición
    return Optimizador.min(x0, c["nombre_parametro"], c["varref"], c["timeref"], c["salida"],
                           c["h"], c["tol"], c["nmax"], c["r0"])


def puntos_iniciales(rango, n, modo="lineal", semilla=0):
    """n valores iniciales en [rango[0], rango[1]], repartidos ('lineal') o al azar ('aleatorio')."""
    if modo == "aleatorio":
        rng = np.random.default_rng(semilla)
        return rng.uniform(rango[0], rango[1], n)
    return np.linspace(rango[0], rango[1], n)


def multistart(num_agentes, rango, nombre_parametro, varref, timeref, salida,
               h, tol, nmax, r0, modo="lineal", semilla=0):
    """Lanza Optimizador.min desde num_agentes puntos iniciales en paralelo.

    Devuelve (x0s, resultados): los puntos iniciales y lo que devolvió min() para cada uno.
    Llamar solo desde dentro de un if __name__ == "__main__":
    """
    x0s = puntos_iniciales(rango, num_agentes, modo, semilla)

    cfg = {"nombre_parametro": nombre_parametro, "varref": varref, "timeref": timeref,
           "salida": salida, "h": h, "tol": tol, "nmax": nmax, "r0": r0}

    nucleos = os.cpu_count() or 2  
    print(f"Numero de nucleos:{nucleos} ")                     # cpu_count() puede devolver None
    n_procesos = min(num_agentes, max(1, nucleos - 1))

    with ProcessPoolExecutor(max_workers=n_procesos,
                             initializer=_preparar_trabajador,
                             initargs=(cfg,)) as ex:
        resultados = list(ex.map(_tarea, x0s))

    return x0s, resultados