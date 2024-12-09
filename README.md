FFT-based simulation of beam propagation
=================================  
Musawwadah Mukhtar, PhD  
https://github.com/DrMukhtar  

Here I present the simulation of beam propagation based on a scientific paper "Fast-Fourier-transform based numerical integration method for the Rayleigh-Sommerfeld formula"[^1].

While optical simulation software such as OpticStudio already provides most of the simulation need, some application of coherent beam shaping of the wavefront most probably requires specific simulation tools. This is the case for the beam shaping application at the company Cailabs where I worked for a while. The code presented here gives an overview of my work that I can share to open public.

As a simplest representative example, I present here a simulation of a Hermite-Gaussian mode after certain propagation distance in free space. We then compute the overlap between the original mode and the propagated mode; in case of Gaussian beam, the script also computes the discrepancy with the analytical value.


# Practical information
This repository contains the processing script and a configuration file. The processing script is written in Python (BeamPropagation.py) and the configuration file is provided as csv file (example: input.csv). To the script in terminal  
`
python3 BeamPropagation.py input.csv
`

The csv file conains the following parameters:
* fixed simulation parameters: number of points grid ($N$) and size of the gride ($L$) along each dimension;
* input beam parameters:beam waist (w)), orders ($m, n$) of the Hermite-Gaussian mode, and potical wavelength (lam);
* physical simulation parameter: propagation distance (dist).

For every instance, it will show the overlap between the original mode and the propagated mode. Here is an example:  

```
Input: wavelength: 1.55um, waist: 40.0um, Hermite-Gaussian (2,2) mode  
Overlap after 0.5mm of propagation: 0.9598 
```

For Gaussian mode ($m=0, n=0$), it also shows the discrepancy with the analytical value. Here is an example:

```
Input: wavelength: 1.55um, waist: 40.0um, Hermite-Gaussian (0,0) mode  
Overlap after 0.5mm of propagation: 0.9941   
Discrepancy with analytical value for Gaussian mode: 0.00%
```

# Numerical method

We have developed the script based on the Fast-Fourier-Transform (FFT) based direct integration numerical method presented in section 3 of Ref. [^1]. The propagated mode is computed as a discrete linear convolution between initial mode and the impulse response. Both initial mode and the propagated mode are sampled to $N\times N$ equidistant grids of size $L\times L$. The impulse response depends on the optical wavelength and the propagation distance. 

The script contains five(5) functions:

1. Function `hermiteGauss2D` returns the sampled initial Hermite Gaussian mode centered at the center of the grids.

2. Function `Ht` returns the impulse response as $(2N-1)\times(2N-1)$ matrix (see Eq. 2 in the mentioned reference).

3. Function $So$ returns the simulated propagated mode. It involves padding the initial mode into $(2N-1)\times(2N-1)$ equidistant grids (noted $U$) and then convoluting it with the impulse response matrix (noted $H$) by means of a two-dimensional FFT (noted FFT2 and IFFT2 for its inverse). The simulated propagated mode is given by the $N\times N$ lower right submatrix of the following 

$$
S=\text{IFFT2}\left[\text{FFT2}\left(U\right)\cdot\times\text{FFT2}\left(H\right)\right]\left(L/N\right)^{2}.
$$

4. Function `\text{Overlap}` returns the overlap as the squared dot product between the initial mode and the propagated mode.

5. Function `\text{OverlapGauss}` returns the expected overlap for the case of Gaussian mode.

We make the simulation more realistic by choosing \text{\ensuremath{\mu}m} as unit for spatial parameters. Typically, `lam` is around one and w0 is around a hundred; we have tested the simulations for N=1000 and L=200.

| ![image](img1.png) |
|:--:|
| The overlap between the initial mode and the propagated mode obtained from the simulation (points) and analytical results (line) |
# Conclusion

# References
[^1]: F.Shen and A. Wang, *Applied optics* **45**, 102-1110 (2006).
