import sys

import math
import numpy as np
import pandas as pd

# Scipy
import scipy as sp
from scipy import special
from scipy.fft import fft2, ifft2

file_name = sys.argv[1]
fp = open(file_name)
inputMode = pd.read_csv(fp, delimiter='\t', encoding='latin1')

# The transverse profile of a Hermite-Gaussian mode
def hermiteGauss2D(m,n,x,y,w0):
    x,y=np.meshgrid(x,y)
    return special.eval_hermite(m,np.sqrt(2)*x/w0)*special.eval_hermite(n,np.sqrt(2)*y/w0)*np.exp(-(x**2+y**2)/(w0**2))


# The impulse response function
def Ht(lam, xa,ya,xo,yo, z=500):
    xt,yt = np.meshgrid(np.append(xo[0]-np.flip(xa[1:]), xo[:]-xa[0]),
                        np.append(yo[0]-np.flip(ya[1:]), yo[:]-ya[0]))
    rt = np.sqrt(xt**2+yt**2+z**2)
    return np.exp(1j*2*math.pi/lam*rt)/(2*math.pi*(rt**2))*z*(1/rt-1j*2*math.pi/lam)
# The mode after propagation
def So(lam, xa,ya,xo,yo,Ua,z=500):
    N = xa.shape[0]
    U=np.pad(Ua,((0,N-1),(0,N-1)))      # Padding intial input mode with zeros
    Ho = Ht(lam, xa,ya,xo,yo,z)         # Applying the impulse response function
    St=ifft2(fft2(U)*fft2(Ho))*((L/N)**2)   # Convolution by means of FFT
    return St[N-1:,N-1:]

# Overlap between the original mode and the propagated mode
def Overlap(Ua,So):
    return abs(abs(np.sum(Ua*np.conjugate(So)))**2/np.sum(Ua*np.conjugate(Ua))/np.sum(So*np.conjugate(So)))
# Expression of the overlap for Gaussian mode
def OverlapGauss(z,zR):
    return (abs(1+1/(1+(z/zR)**2) + 1j*z*zR/(z**2+zR**2))**-2)*4/(1+(z/zR)**2)


print("Calculating the overlap between the original mode and the propagated mode ...")
for ii in range(len(inputMode)):
    # Simulation parameters
    N = int(inputMode.iloc[ii]['N'])                        # Number of grid points
    L = inputMode.iloc[ii]['L']                             # The size of simulated square domain
    # The input beam
    w0 = inputMode.iloc[ii]['w0']                           # the beam waist in micrometer
    lam = inputMode.iloc[ii]['lam']                         # The wavelength in micrometer
    # parameters specific to Hermite-Gaussian mode
    m = int(inputMode.iloc[ii]['m'])
    n = int(inputMode.iloc[ii]['n'])
    # Physical simulation parameter
    dist = inputMode.iloc[ii]['dist']                       # Propagation distance

    # The grid of the aperture
    xa = np.linspace(-L/2,L/2-L/N,N)
    ya = np.linspace(-L/2,L/2-L/N,N)

    # The grid of the observation plane
    xo = np.linspace(-L/2,L/2-L/N,N)
    yo = np.linspace(-L/2,L/2-L/N,N)


    # the mode
    print("Input: wavelength: "+ str(lam)+"um, " +"waist: "+ str(w0)+ "um, " + "Hermite-Gaussian " + "(" + str(m) + "," + str(n) + ") mode")

    # The Hermite-Gaussian beam
    Ua = hermiteGauss2D(m, n, xa, ya, w0)

    # The simulated propagating beam
    SoHG = So(lam, xa, ya, xo, yo, Ua, z=dist)

    # Overlap
    ov = Overlap(Ua, SoHG)
    print("Overlap after " + str(dist / 1000) + "mm of propagation: " + '{0:.4f}'.format(ov))

    # Case of Gaussian Beam
    if (m == 0 and n == 0):
        predOv = OverlapGauss(dist, zR=math.pi * w0 ** 2 / lam)
        print("Discrepancy with analytical value for Gaussian mode: " + '{0:.2f}'.format(
            200 * abs(predOv - ov) / (predOv + ov)) + "%")







