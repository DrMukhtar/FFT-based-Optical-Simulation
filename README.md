FFT-based simulation of beam propagation
=================================  
Musawwadah Mukhtar, PhD  
https://github.com/DrMukhtar  
https://linkedin.com/in/drmukhtar/

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

4. Function `Overlap` returns the overlap as the squared dot product between the initial mode and the propagated mode.

5. Function `OverlapGauss` returns the expected overlap for the case of Gaussian mode.

We make the simulation more realistic by choosing $\mu$m as unit for spatial parameters. Typically, `lam` is around one and w0 is around a hundred; we have tested the simulations for `N=1000` and `L=200`.

# Discussion

The case of the $(0,0)$ mode can be used to verify the quality of the method. The overlap between the initial mode and the propagated mode yields 

$$
\frac{4\left(1+s^{2}\right)}{\left|2+s^{2}-js\right|^{2}},
$$

where $s=\text{dist}/z_{R}$ and $j=\sqrt{-1}$. Figure 1 depicts the overlaps for different propagation distances obtained from both simulation and analytical results; `lam=1.55`, `w0=40`. As shown if Fig. 2, the discrepancy is weak for distance smaller than the Rayleigh length ($\pi\text{w0}^{2}/\text{lam}$).

| ![image](img1.png) |
|:--:|
| Figure 1: The overlap between the initial mode and the propagated mode obtained from the simulation (points) and analytical results (line). |

| ![image](img1.png) |
|:--:|
| Figure 2: The corresponding discrepancy; distance is normalized by the Rayleigh length (3.24 mm). |

Besides, FFT is efficient for N being multiple of small prime numbers [^2], $O(N\log N)$. For this simulation method, the FFT applied to grids of $(2N-1)\times(2N-1)$ points. When N is a multiple of small prime numbers, $(2N-1)$ unlikely fulfills the condition. The effect would not be tangible for $N$ around 1000. It would be interesting to study the efficiency of the method for high value of $N$. 


# Conclusion
We have successfully developed numerical simulation of beam propagation based on method presented in Ref. [^1]. We have calculated the overlap between the original mode and the propagated mode. We have also verified the result with the analytical result for the case of Gaussian beam with excellent agreement.

For future work, we can attempt to include the effect of medium represented by its refraction index. We can also examine the efficiency of the numerical methods with increasing number of grid points. 

# References
[^1]: F.Shen and A. Wang, *Applied optics* **45**, 102-1110 (2006).  
[^2]: J. W. Cooley and J. W. Tukey, Mathematics of Computation 19, 297-301 (1965).

