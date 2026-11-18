import simulador as sim
import identificacion as id
import numpy as np

_b = None
_c = None

def tayloraprox(f0,x0,x):
    "aproximacion de taylor de segundo orden"
    return f0 + _b*(x-x0) + 0.5*_c*(x-x0)**2

def comparar(fx,fx0,taylorx,epsilon):
    c = (fx-fx0)/(taylorx-fx0)
    #print(f"c vale:{c}")
    return c>=0 and c<=epsilon
    

def min(x0,nombre_parametro:str,varref,timeref,salida: str,h,tol,nmax,r0,epsilon=None):
    n=0
    residuo=1.0
    epsilon=1.0
    
    global _b,_c

    while residuo >tol and n<nmax and x0>0:
        dxmas={nombre_parametro:x0+h}
        dxmenos={nombre_parametro:x0-h}
        dx0={nombre_parametro:x0}

        varmas = sim.simular(dxmas,timeref,salida)
        var0 = sim.simular(dx0,timeref,salida)
        varmenos = sim.simular(dxmenos,timeref,salida)

        resmas = id.fobj(varref, timeref,varmas)
        resmenos = id.fobj(varref,timeref,varmenos)
        res0 = id.fobj(varref,timeref,var0)

        _b,_c = id.coef_taylor(resmas,res0,resmenos,h)
        residuo = id.fobj(varref,timeref,var0)
        
        if _c>0:
            term_avance =_b/_c
        else:
            term_avance =_b*3
        if r0 < abs(term_avance):
            lim=x0-r0*np.sign(term_avance)
            dlim={nombre_parametro:lim}
            varx=sim.simular(dlim,timeref,salida)
            taylorx=tayloraprox(res0,x0,lim)
            resx=id.fobj(varref,timeref,varx)
            #print(f"Caution ha intentado salir de la zona de confort,avance:{term_avance}")
            if comparar(resx,res0,taylorx,epsilon):
                #print(f"No problem, se parece un puñao ")
                r0=r0*1.1
                term_avance=r0*np.sign(term_avance)
            else:
                #print(f"Loco que no se parece me quedo en el borde")
                term_avance=r0*np.sign(term_avance)
        #print(term_avance)
        x0=x0-term_avance
        n+=1

    return x0+term_avance


