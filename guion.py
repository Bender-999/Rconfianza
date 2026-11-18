import time
import numpy as np
import scipy as sp
import simulador
import generarfmu
import agents
import matplotlib.pyplot as plt

# --- Problema ---
parametros = "Cd"
salida = "Theta"
cd_real = 0.7                         # con el que se generan los datos de prueba
timeref = np.linspace(0, 10, 1001)    # paso 0.01 s exacto

# --- Optimizador ---
h = 1e-4          # paso de las diferencias finitas
tol = 1e-6        # se para cuando el paso es menor que tol*(1+|Cd|)
nitermax = 70
r0 = 0.25          # radio inicial de la region de confianza

# --- Multistart ---
num_agentes = 8
rango = (0.2, 3.0)


if __name__ == "__main__":
    generarfmu.asegurar_fmu()
    simulador.cargar()
    thetaref = simulador.simular({parametros: cd_real}, timeref, salida)

    t0 = time.perf_counter()
    x0s, resultados = agents.multistart(
        num_agentes=num_agentes, rango=rango,
        nombre_parametro=parametros, varref=thetaref, timeref=timeref, salida=salida,
        h=h, tol=tol, nmax=nitermax, r0=r0, modo="lineal")
    print(f"Tiempo total: {time.perf_counter() - t0:.1f} s")

    for x0, (Cd_final,residuo) in zip(x0s, resultados):
        print(f"x0 = {x0:.3f}  ->  {Cd_final}")

        plt.semilogy(residuo)
        plt.plot(residuo)
        plt.xlabel("Iteración")
        plt.ylabel("Residuo")
    cds_finales = [r[0] for r in resultados]
    print(f"Media de valores fianles = {sp.stats.trim_mean(cds_finales,0.2)}")
    print(f"Desviación típica de valores finales={np.std(cds_finales)}")
    plt.show()

    simulador.cerrar()