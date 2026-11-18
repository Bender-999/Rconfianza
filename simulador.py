import fmpy
import numpy as np
import config

_md = None
_fmu = None

def cargar():
    #lee la descripcion descripcion e instancia la FMU.Una vez por ejecución
    global _fmu, _md
    _md = fmpy.read_model_description(config.UNZIP)
    _fmu=fmpy.instantiate_fmu(unzipdir=config.UNZIP,model_description=_md,fmi_type="ModelExchange")

def simular(parametros: dict, t: np.ndarray, salida: str) -> np.ndarray:
    
    """Simula la FMU y devuelve una variable en los instantes pedidos.

    Parameters
    ----------
    parametros : dict
        Parámetros del modelo, p. ej. {"Cd": 0.5}.
    t : np.ndarray
        Instantes [s] donde se quiere la salida. Equiespaciados, empezando en 0.
    salida : str
        Nombre de la variable del modelo a devolver, p. ej. "Theta".

    Returns
    -------
    np.ndarray
        Valores de `salida` en cada instante de `t`.
    """
    # Reinicio la simulacion antes de volver a simularla
    _fmu.reset()
    # Simula con los parametros dados, y salidas dadas, en el tiempo especificado
    res = fmpy.simulate_fmu(filename=config.UNZIP,model_description=_md,fmu_instance=_fmu,start_values=parametros,
                            start_time=t[0],stop_time=t[-1],output=[salida],relative_tolerance=1e-8,
                            output_interval=t[1]-t[0])
    #separamos salidas del tiempo
    res_salida = res[salida]
    t_sim = res["time"]
    #interpolacion de salidas en los puntos de tiempo dado
    resinterp = np.interp(t,t_sim,res_salida)
    return resinterp

def cerrar():
    # Libera la .dll
    _fmu.freeInstance()

#Pruebas de las funciones
if __name__=="__main__":
    import generarfmu as gfmu
    import time as tm
    import matplotlib.pyplot as plt 
    gfmu.asegurar_fmu()
    cargar()
    t = np.linspace(0,10,1001)
    Cd = [0.1,2]
    salida = "Theta"
    for cd in Cd:
        parametro={"Cd":cd}
        start = tm.perf_counter()
        theta = simular(parametro,t,salida)
        end = tm.perf_counter()
        elapsed=end-start
        print(f"Simulación con Cd={cd}, ha tardado en simular={elapsed} segundos")
        plt.plot(t,theta,label=f"Cd={cd}")
        plt.legend()
        
    plt.show()
    cerrar()
    