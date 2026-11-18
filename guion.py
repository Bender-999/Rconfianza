import time
import numpy as np
import simulador
import generarfmu
import agents

parametros="Cd"
salida="Theta"
tol=1e-5
h=1e-2
nitermax=50
r0=1
timeref = np.linspace(0,10,10001)
#Multistart
num_agentes=5


if __name__=="__main__":
    generarfmu.asegurar_fmu()
    simulador.cargar()
    thetaref = simulador.simular({"Cd":0.7},timeref,salida)

    t0 = time.perf_counter()
    x0s, resultados = agents.multistart(
        num_agentes=5, rango=(0.2, 2.0),
        nombre_parametro="Cd", varref=thetaref, timeref=timeref, salida=salida,
        h=1e-4, tol=1e-3, nmax=50, r0=0.5, modo="aleatorio")
    print(f"Tiempo total: {time.perf_counter() - t0:.1f} s")

    for x0, r in zip(x0s, resultados):
        print(f"x0 = {x0:.3f}  ->  {r}")

    simulador.cerrar()