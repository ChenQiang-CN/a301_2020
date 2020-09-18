---
jupytext:
  encoding: '# -*- coding: utf-8 -*-'
  text_representation:
    extension: .md
    format_name: myst
    format_version: '0.8'
    jupytext_version: 1.5.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

+++ {"toc": true}

<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#Question-1" data-toc-modified-id="Question-1-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Question 1</a></span><ul class="toc-item"><li><span><a href="#Question-1a-solution" data-toc-modified-id="Question-1a-solution-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Question 1a solution</a></span></li><li><span><a href="#Question-1b-solution" data-toc-modified-id="Question-1b-solution-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Question 1b solution</a></span></li><li><span><a href="#Question-1c-solution:" data-toc-modified-id="Question-1c-solution:-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Question 1c solution:</a></span></li></ul></li><li><span><a href="#Question-2" data-toc-modified-id="Question-2-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Question 2</a></span><ul class="toc-item"><li><span><a href="#Question-2a-solution" data-toc-modified-id="Question-2a-solution-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Question 2a solution</a></span></li><li><span><a href="#Question-2b-solution" data-toc-modified-id="Question-2b-solution-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Question 2b solution</a></span></li></ul></li><li><span><a href="#Question-3" data-toc-modified-id="Question-3-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Question 3</a></span><ul class="toc-item"><li><span><a href="#Question-3-solution" data-toc-modified-id="Question-3-solution-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>Question 3 solution</a></span></li></ul></li><li><span><a href="#Question-4" data-toc-modified-id="Question-4-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Question 4</a></span><ul class="toc-item"><li><span><a href="#Question-4-solution" data-toc-modified-id="Question-4-solution-4.1"><span class="toc-item-num">4.1&nbsp;&nbsp;</span>Question 4 solution</a></span></li></ul></li></ul></div>

```{code-cell}
import numpy as np

import a301.radiation
```

# Question 1

+++

 - (10) A satellite orbiting at an altitude of 36000 km observes the
    surface in a thermal channel with a wavelength range of
    $8\ \mu m < \lambda < 10\ \mu m$.

      - Assuming that the atmosphere has density scale height of
        $H_\rho=10$ km and a surface air density of $\rho_{air}=1$
        and that the absorber has mass absorption coefficient of
        $k_\lambda = 3 \times 10^{-2}\ m^2/kg$ at $\lambda=9\ \mu m$
        and a mixing ratio $6 \times 10^{-3}$ kg/kg, find the vertical
        optical thickness $\tau$ and transmittance of the atmosphere
        directly beneath the satellite

      - If the surface is black with a temperature of 300 K, and the
        atmosphere has an average temperature of 270 K, find the

          - radiance observed by the satellite in at 9 $\mu m$

          - brightness temperature of the pixel in Kelvin for that
            radiance

      - Given a pixel size 2 $km^2$, what is the flux, in , reaching
        the satellite in this channel?


+++

## Question 1a solution

Assuming that the atmosphere has density scale height of
$H_\rho=10$ km and a surface air density of $\rho_{air}=1$
and that the absorber has mass absorption coefficient of
$k_\lambda = 3 \times 10^{-2}\ m^2/kg$ at $\lambda=9\ \mu m$
and a mixing ratio $6 \times 10^{-3}$ kg/kg, find the vertical
optical thickness $\tau$ and transmittance of the atmosphere
directly beneath the satellite

+++

$$\rho_{atm} = \rho_0 \exp \left ( -z/H \right )$$

$$H=10\ km$$

$$\tau = \int_0^{3.6e6}k \rho_0 \exp (-z/H ) r_{mix} dz$$

$$\tau = -H k \exp(-z^\prime/H ) \rho_0 r_{mix}  \big \rvert_0^{3.6e6} =0 - (-Hk \rho_0 r_{mix})=H k \rho_0 r_{mix} $$

$$t=\exp(-\tau)$$

```{code-cell}
H = 10000.0
k = 3.0e-2
rho0 = 1.0
rmix = 6.0e-3
tau = H * k * rho0 * rmix
t = np.exp(-tau)
print(f"optical thickness τ={tau} and transmittance t={t:5.2f}")
```

## Question 1b solution
- If the surface is black with a temperature of 300 K, and the
        atmosphere has an average temperature of 270 K, find the

          - radiance observed by the satellite in at 9 $\mu m$

          - brightness temperature of the pixel in Kelvin for that
            radiance

+++

$$L_{atm}= B(300)*\exp(-\tau) + (1 - \exp(-\tau))*B(270)$$

```{code-cell}
t = np.exp(-tau)
e = 1 - t
L270 = a301.radiation.calc_radiance(9.0e-6, 270)
L300 = a301.radiation.calc_radiance(9.0e-6, 300)
Lsat = t * L300 + e * L270
print(Lsat)
Tbright = a301.radiation.planck_invert(9.0e-6, Lsat)
print(f"radiance is {Lsat*1.e-6:5.2f} W/m^2/microns/sr")
print(f"brightness temperature is {Tbright:5.2f} K")
```

## Question 1c solution:
- Given a pixel size 2 $km^2$, what is the flux, in , reaching
    the satellite in this channel?


+++

$\Delta \omega = A/R^2 = 2/36000^2. = 1.54 \times 10^{-9}$ sr

$E = L \Delta \omega \,\Delta \lambda  = 6.15\ W\,m^2\,\mu^{-1} m \times 1.54 \times 10^{-9} \times 2$

```{code-cell}
Eout = 6.15 * 1.54e-9 * 2
print(f"flux in channel is {Eout:5.2g} W/m^2")
```

# Question 2

## Question 2a solution

- (3) A cone has a spreading angle of 35 degrees between its
      center and its side. What is its subtended solid angle?

$$\omega = \int_0^{2\pi} \int_0^{35} \sin \theta d\theta d\phi = 2\pi (-\cos \theta \big \rvert_0^{35}) = 2 \pi (1 - \cos(35))$$

```{code-cell}
omega = 2 * np.pi * (1 - np.cos(35 * np.pi / 180.0))
print(f"solid angle = {omega:5.2f} sr")
```


## Question 2b solution

- (3) Assuming that radiance is independent of the distance $d$
      between an instrument and a surface, show that the flux from the
      surface decreases as $1/d^2$

Given  a narrow field of view of a pixel the radiance is:

$$E \approx L \Delta \omega$$

where $\Delta \omega = A/d^2$ with A the area of the pixel.  Since $L$ is constant, $E \propto 1/d^2$

+++

# Question 3

Integrate the Schwartzchild equation for constant temperature

## Question 3 solution

1. We know the emission from an infinitesimally thin layer:

   $$ dL_{emission} = B_{\lambda} (T_{layer}) de_\lambda = B_{\lambda} (T_{layer}) d\tau_\lambda$$


2. Add the gain from $dL_{emission}$ to the loss from $dL_{absorption}$ to get
   the **Schwartzchild equation** without scattering:

   $$  dL_{\lambda,absorption} + dL_{\lambda,emission}  = -L_\lambda\, d\tau_\lambda + B_\lambda (T_{layer})\, d\tau_\lambda $$

3.  We can rewrite :eq:$schwart1$ as:

    $$  \frac{dL_\lambda}{d\tau_\lambda} = -L_\lambda + B_\lambda (T_{layer})$$

4. In class I used change of variables to derived the following: if the temperature $T_{layer}$  (and hence $B_\lambda(T_{layer})$) is constant with height and the radiance arriving at the base of the layer is $L_{\lambda 0} = B_{\lambda} T_{skin}$ for a black surface with $e_\lambda = 1$, then the total radiance exiting the top of the layer is $L_{\lambda}$ where:

   $$ \int_{L_{\lambda 0}}^{L_\lambda} \frac{dL^\prime_\lambda}{L^\prime_\lambda -
           B_\lambda} = - \int_{0}^{\tau_{T}} d\tau^\prime $$

   Where the limits of integration run from just above the black surface (where the radiance from
   the surface is $L_{\lambda 0}$) and $\tau=0$ to the top of the layer, (where the radiance is $L_\lambda$) and the optical thickness is $\tau_{\lambda T}$.

   To integrate this, make the change of variables:




\begin{align}
  U^\prime &= L^\prime_\lambda - B_\lambda \\
  dU^\prime &= dL^\prime_\lambda\\
  \frac{dL^\prime_\lambda}{L^\prime_\lambda -
   B_\lambda} &= \frac{dU^\prime}{U^\prime} = d\ln U^\prime
\end{align}



   where I have made use of the fact that $dB_\lambda = 0$ since the temperature is constant.

   This means that we can now solve this by integrating a perfect differential:

   $$
     \int_{U_0}^U d\ln U^\prime = \ln \left (\frac{U}{U_0} \right ) =  \ln \left (\frac{L_\lambda - B_\lambda}{L_{\lambda 0} - B_\lambda} \right ) = - \tau_{\lambda T} $$

   Taking the $\exp$ of both sides:

   $$   L_\lambda - B_\lambda = (L_{\lambda 0} - B_\lambda) \exp (-\tau_{\lambda T}) $$


   or rearranging and recognizing that the transmittance is $\hat{t_\lambda} = \exp(-\tau_{\lambda T} )$:

   $$  L_\lambda = L_{\lambda 0} \exp( -\tau_{\lambda T}  ) + B_\lambda (T_{layer})(1- \exp( -\tau_{\lambda T} )) $$


   $$   L_\lambda = L_{\lambda 0} \hat{t}_{\lambda}  + B_\lambda (T_{layer})(1- \hat{t}_{\lambda}) $$

   $$ L_\lambda = L_{\lambda 0}  \hat{t}_{\lambda} + B_\lambda (T_{layer})a_\lambda $$

5. so bringing in Kirchoff's law, the radiance exiting the top of the isothermal layer of thickness $\Delta \tau$ is:

   $$  L_\lambda = L_{\lambda 0}  \hat{t}_{\lambda} + e_\lambda B_\lambda $$


+++

# Question 4

+++

- Pyresample (10)

Consider the following code:

    from pyresample import  SwathDefinition, kd_tree, geometry
    proj_params = get_proj_params(m5_file)
    swath_def = SwathDefinition(lons_5km, lats_5km)
    area_def_lr=swath_def.compute_optimal_bb_area(proj_dict=proj_params)
    area_def_lr.name="ir wv retrieval modis 5 km resolution (lr=low resolution)"
    area_def_lr.area_id='modis_ir_wv'
    area_def_lr.job_id = area_def_lr.area_id
    fill_value=-9999.
    image_wv_ir = kd_tree.resample_nearest(swath_def, wv_ir_scaled.ravel(),
                                      area_def_lr, radius_of_influence=5000,
                                          nprocs=2,fill_value=fill_value)
    image_wv_ir[image_wv_ir < -9000]=np.nan
    print(f'\ndump area definition:\n{area_def_lr}\n')
    print((f'\nx and y pixel dimensions in meters:'
           f'\n{area_def_lr.pixel_size_x}\n{area_def_lr.pixel_size_y}\n'))

In the context of this snippet, explain what the following objects
(i.e. their type, what some of their attributes are, etc.) and how
they are used to map a satellite image:

+++

## Question 4 solution

- proj\_params

dictionary holding parameters for a map projection that
can be used by pyproj to map lat/lon to x/y: datum, lat\_0, lon\_0
name of projection etc.

- swath\_def

object of type pyresample.geometry.SwathDefinition that holds data and
functions needed to convert modis pixel lat/lon values to x,y -- pass as input
to kd_tree_resample_nearest

- area\_def\_lr

object of type pyresample.geometry.AreaDefinition that holds x,y array information
like number of rows, number of columns and image extent in x and y.

- wv\_ir\_scaled.ravel()

water vapor data scaled to units of cm in the column and converted to a 1-dimensional
vector using the ravel method.

- kd\_tree.resample\_nearest

function that takes water vapor values and sorts them onto an x,y grid based on
their lat/lon values from the swath\_def object.  This is the mapped image.

```{code-cell}
!pwd
```

```{code-cell}

```
