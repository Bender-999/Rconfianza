import simulador as sim
import identificacion as id


def tayloraprox(b,c,f0,x0,x):
    "aproximacion de taylor de segundo orden"
    return f0 + b*(x-x0) + 0.5*c*(x-x0)**2

def comparacion(fx,fx0,taylorx,taylorx0,epsilon):
    c = abs(fx-fx0)/abs(taylorx-taylorx0)
    if c<=epsilon or c>=epsilon:
        return False

def min():



def multistart(num_agentes,lista):
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=num_agentes) as ex:
        resultados =list(ex.map(min,lista))
    print resultados