from pathlib import Path

RAIZ = Path(__file__).resolve().parent

#Modelo
LIB = RAIZ.parent / "MiLibreria" / "package.mo"
MODELO = "MiLibreria.Mecanica.Pendulo_simple_planar"
NOMBRE= MODELO.split(".")[-1]

#FMU builder

BUILD = RAIZ / "build"
FMU = BUILD / f"{NOMBRE}.fmu"
UNZIP = BUILD / f"{NOMBRE}_fmu"
OMC_WORK = Path.home() / "omc_trabajo" / "identificacion"
XML = UNZIP / "modelDescription.xml"
#datos

DATOS = RAIZ / "datos"
RESULTADOS = RAIZ / "resultados"

if __name__ =="__main__":
    print(f"RAIZ = {RAIZ} : {RAIZ.exists()}")
    print(f"LIB = {LIB} : {LIB.exists()}")
    print(f"MODELO = {MODELO}")
    print(f"BUILD = {BUILD} : {BUILD.exists()}")
    print(f"FMU = {FMU} : {FMU.exists()}")
    print(f"UNZIP = {UNZIP} : {UNZIP.exists()}")
    print(f"OMC_WORK = {OMC_WORK}: {OMC_WORK.exists()}")
    print(f"DATOS = {DATOS} : {DATOS.exists()}")
    print(f"RESULTADOS = {RESULTADOS} : {RESULTADOS.exists()}")