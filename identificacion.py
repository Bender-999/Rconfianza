import numpy as np
import scipy as sp

def funcobj(varref,timeref,var,varc=None):
    #si no se ha introducido o es 0 la varcaracterística, la defino como la inicial.
    if varc is None:
        varc=varref[0]
    error = (varref-var)**2
    return sp.integrate. (error,timeref)/((varc**2)*(timeref[-1]-timeref[0]))


