import time
import numpy as np
import scipy as sp
import pandas as pd
import simulador
import generarfmu
import agents
import identificacion
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# --- Problema ---
parametros = "Cd"
salida = "Theta"
L=0.4
m=0.005
A=(0.004**2)*np.pi
#cd_real = 0.7                         # con el que se generan los datos de prueba
#timeref = np.linspace(0, 10, 1001)    # paso 0.01 s exacto

# --- Optimizador ---
h = 1e-4          # paso de las diferencias finitas
tol = 1e-8        # se para cuando el paso es menor que tol*(1+|Cd|)
nitermax = 70
r0 = 0.25          # radio inicial de la region de confianza

# --- Multistart ---
num_agentes = 8
rango = (0.1, 3.0)


if __name__ == "__main__":
    generarfmu.asegurar_fmu()
    simulador.cargar()
    df = pd.read_csv('Pendulo_bola_porexpan_theta.txt',sep=r'\s+',decimal=",")
    timeref = df["t"].to_numpy()
    timeref = timeref[:182]
    thetaref = df["theta"].to_numpy()
    thetaref= thetaref[:182]
    #thetaref = simulador.simular({parametros: cd_real}, timeref, salida)
    plt.plot(timeref,thetaref)
    plt.show()
    t0 = time.perf_counter()
    x0s, resultados = agents.multistart(
        num_agentes=num_agentes, rango=rango,
        nombre_parametro=parametros, varref=thetaref, timeref=timeref, salida=salida,
        h=h, tol=tol, nmax=nitermax, r0=r0, modo="aleatorio")
    print(f"Tiempo total: {time.perf_counter() - t0:.1f} s")

    for x0, (Cd_final,residuo) in zip(x0s, resultados):
        print(f"x0 = {x0:.3f}  ->  {Cd_final}")

        #plt.semilogy(residuo)
        plt.plot(residuo)
        plt.xlabel("Iteración")
        plt.ylabel("Residuo")
    cds_finales = [r[0] for r in resultados]
    print(f"Media de valores fianles = {sp.stats.trim_mean(cds_finales,0.2)}")
    print(f"Desviación típica de valores finales={np.std(cds_finales)}")
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.show()
    Cd=np.linspace(0.1,2,101)
    fobj=np.zeros(len(Cd))
    for i in range(len(Cd)):
        var =simulador.simular({"Cd":Cd[i]},timeref,salida)
        fobj[i]=identificacion.fobj(thetaref,timeref,var)
    plt.plot(Cd,fobj)
    plt.show()
    
    simulador.cerrar()