import scipy as sp

def fobj(varref,timeref,var,varc=None):
    #si no se ha introducido o es 0 la varcaracterística, la defino como la inicial.
    if varc is None:
        varc=varref[0]
    error = (varref-var)**2
    return sp.integrate.trapezoid(error,timeref)/((varc**2)*(timeref[-1]-timeref[0]))

def coef_taylor(resmas,res0,resmenos,h):
    #coeficiendes de la aproximacion de taylor
    b=(resmas - resmenos)/(2*h)
    c=(resmas - 2*res0 + resmenos)/(h**2)
    return b,c
