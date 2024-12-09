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
* fixed simulation parameters: number of points grid ($N$) and size of the gride ($L$) in one dimension;
* input beam parameters:beam waist (w)), orders ($m, n$) of the Hermite-Gaussian mode, and potical wavelength (lam);
* physical simulation parameter: propagation distance (dist).

For every instance, it will show the overlap between the original mode and the propagated mode. Here is an example:  

```
Input: wavelength: 1.55um, waist: 40.0um, Hermite-Gaussian (2,2) mode  
Overlap after 0.5mm of propagation: 0.9598 
```


# Numerical method

| ![image](img1.png) |
|:--:|
| The overlap between the initial mode and the propagated mode obtained from the simulation (points) and analytical results (line) |
# Conclusion

# References
[^1]: F.Shen and A. Wang, *Applied optics* **45**, 102-1110 (2006).
