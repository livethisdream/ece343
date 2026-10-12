import numpy as np
import sympy as sp


def find_gamma_l(zl):
    # given normalized load impedance and normalized source impedance, find reflection coefficient
    gl = (zl -1)/(zl + 1)
    return gl


def find_zin(gl, zs):
    # given reflection coefficient and normalized source impedance, determine input impedance, such that:
    #   abs(Gamma_L) = abs(z_s + jX -1 ) / abs(z_s +jx +1)
    x = sp.Symbol('x', real=True)
    sols = sp.solve(abs(gl) - (abs(zs + sp.I*x -1 ) / abs(zs + sp.I*x +1)),x)
    zin = [zs + sp.I*sols[i] for i in range(len(sols))]
    return zin

def find_l(zl,zin):
    bl = sp.Symbol('bl', real=True)
    sol = [0]*len(zin)
    for i in range(len(zin)):
        rin=sp.re(zin[i])
        xin=sp.im(zin[i])
        rl=sp.re(zl)
        xl=sp.im(zl)
        sol[i] = (sp.atan((rin-rl)/((rin*xl)+(rl*xin)))/(2*np.pi))
        while sol[i] < 0:
            sol[i] = sol[i] + 0.5
    return sol

if __name__ == "__main__":
    zl = 0.678+sp.I*0.352
    zs=1
    gl = find_gamma_l(zl)
    print("Reflection coefficient is " + str(abs(gl)) + " at " + str(sp.deg(sp.arg(gl)).evalf()) + " deg")
    print("")
    zin = find_zin(gl,zs)
    print("Zin values are: " )
    print(zin)
    print("")
    l = find_l(zl,zin)
    print("Line lengths are:")
    print(l)
