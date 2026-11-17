import shutil
import fmpy
import config

def fmu_al_dia():
    if not config.FMU.exists(): #Compruebo si existe
        return False
    #Compruebo si ha cambiado caulquier .mo de la libreria
    return config.FMU.stat().st_mtime > max(n.stat().st_mtime for n in config.LIB.parent.rglob("*.mo"))

def generar_fmu():
    import OMPython
    #Creo la carpeta Build si no existe.
    config.BUILD.mkdir(parents=True,exist_ok=True)
    #Creo la carpeta de trabajo OMC si no existe.
    config.OMC_WORK.mkdir(parents=True,exist_ok=True)
    # creo objeto de OPenModelica y le digo que trabaje en la carpeta que cree en OMC_WORK
    mod = OMPython.ModelicaSystemOMC(work_directory=config.OMC_WORK.as_posix()) 
    #cargo el modelo, y con las librerias, con build = False no compila el .exe
    mod.model(model_name= config.MODELO, libraries= ["Modelica", config.LIB.as_posix()], build= False)
    #convierto el .mo a fmu
    M2F = mod.convertMo2Fmu()
    #copio el fmu a la carpeta build
    shutil.copy(M2F.as_posix(),config.FMU)

def carpeta_al_dia():
    if not config.XML.exists(): #Compruebo si existe
        return False
    #Compruebo si desde el ultimo cambio del .fmu se ha descomprimido 
    return config.XML.stat().st_mtime > config.FMU.stat().st_mtime

def descomprimir():
    #Borra la carpeta vieja y/o descomprime.
    shutil.rmtree(config.UNZIP.as_posix(),ignore_errors=True)
    fmpy.extract(config.FMU,unzipdir=config.UNZIP)
    config.XML.touch()

def asegurar_fmu():
    if not fmu_al_dia():
        print("El .fmu no está actualizado, procedo a actualizarlo")
        generar_fmu()
    print(".fmu actualizado ✅")
    if not carpeta_al_dia():
        print("La carpeta del modelo no está actualizada, borro la vieja y descomprimo la nueva ")
        descomprimir()
    print("Carpeta actualizada ✅")


if __name__ == "__main__":
    asegurar_fmu()