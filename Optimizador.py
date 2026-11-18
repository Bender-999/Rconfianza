import simulador as sim
import identificacion as id
import numpy as np

_b = None
_c = None

def tayloraprox(f0,x0,x):
    "aproximacion de taylor de segundo orden"
    return f0 + _b*(x-x0) + 0.5*_c*(x-x0)**2

def comparar(fx,fx0,taylorx):
    c = (fx-fx0)/(taylorx-fx0)
    #print(f"c vale:{c}")
    #return c>=0 and c<=epsilon
    return c
    

def mini(x0,nombre_parametro:str,varref,timeref,salida: str,h,tol,nmax,r0,r0max=None):
    n=0
    residuo=1.0
    residuolist=np.zeros(nmax)
    if r0max==None:
        r0max=4*r0
    global _b,_c

    while residuo >tol and n<nmax:
        dxmas={nombre_parametro:x0+h}
        dxmenos={nombre_parametro:x0-h}
        dx0={nombre_parametro:x0}

        varmas = sim.simular(dxmas,timeref,salida)
        var0 = sim.simular(dx0,timeref,salida)
        varmenos = sim.simular(dxmenos,timeref,salida)

        resmas = id.fobj(varref, timeref,varmas)
        resmenos = id.fobj(varref,timeref,varmenos)
        res0 = id.fobj(varref,timeref,var0)
        residuo = id.fobj(varref,timeref,var0)
        residuolist[n]=residuo
        if residuo<tol:
            break

        _b,_c = id.coef_taylor(resmas,res0,resmenos,h)
        
        
        if _c>0:
            term_avance =_b/_c
        else:
            term_avance =r0*np.sign(_b)
        if r0 < abs(term_avance):
            lim=x0-r0*np.sign(term_avance)
            if lim<=0:
                lim=0
            dlim={nombre_parametro:lim}
            varx=sim.simular(dlim,timeref,salida)
            taylorx=tayloraprox(res0,x0,lim)
            resx=id.fobj(varref,timeref,varx)
            #print(f"Caution ha intentado salir de la zona de confort,avance:{term_avance}")
            r=comparar(resx,res0,taylorx)
            if r<=0.05:
                #poor model --> shrink radius
                r0=r0/4
                term_avance=0
            elif r>=0.9:
                r0=min(2*r0,r0max)
                term_avance=r0*np.sign(term_avance)
            else:
                term_avance=r0*np.sign(term_avance)
        #print(term_avance)
        
        x0=x0-term_avance
        if x0<=0:
            x0=0
        n+=1
    residuolist = residuolist[:(n+1)]
    return x0,residuolist


