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
<div class="toc"><ul class="toc-item"><li><span><a href="#problem-1" data-toc-modified-id="problem-1-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>problem 1</a></span></li><li><span><a href="#Problem-2" data-toc-modified-id="Problem-2-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Problem 2</a></span></li><li><span><a href="#Problem-3" data-toc-modified-id="Problem-3-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Problem 3</a></span></li><li><span><a href="#Question-4" data-toc-modified-id="Question-4-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Question 4</a></span></li><li><span><a href="#Question-5" data-toc-modified-id="Question-5-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Question 5</a></span></li><li><span><a href="#Question-6" data-toc-modified-id="Question-6-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Question 6</a></span></li></ul></div>

```{code-cell}
from IPython.display import Image
from numpy import exp
```

**ATSC 301 Final – December 16, 2010**

**Answer all six questions (65 points total) and show all your work
(note weights in parenthesis). Sketches are particularly helpful in
assessing partial credit. If you are stumped over one part of a
multipart question and need that intermediate result, make up a likely
number and continue, explaining what you’re doing. Put your name on the
Planck diagram and hand that in if there is information on it that would
help interpret your answer**

+++

### problem 1

+++

-   1-(4) An atmosphere with an absorber density profile
    $\rho=\rho_0 \exp (-z/H)$ has mass absorption coefficient of
    $k_\lambda=0.01\ m^2/kg$ at $\lambda=10\ \mu m$. Given
    $\rho_0=0.05\ kg/m^3$ and H= 5 km, find:

    -   \(2) The total absorber mass in $kg/m^2$

    -   \(2) The monochromatic vertical optical depth $\tau_\lambda$ between 2 km
        and the top of the atmosphere.

```{code-cell}
rho0 = 0.05
H = 5000
klambda = 0.01
# Integrate the hydorstatic equation from 0 to infty
tot_massA = rho0 * H
# integrate from 2 km to infty
tauB = rho0 * H * klambda * exp(-2 / 5.0)
print("A) {tot_massA:}\nB) {tauB:}".format_map(locals()))
```

### Problem 2

+++

-   \(18) Radar

    -   2A-\(6) A doppler radar with a wavelength of 5 cm and a PRF of 800 sends out
        a pulse pair and receives the following phase information. Find the
        smallest inbound (into the radar) and outbound (away from the radar)
        radial wind speeds that are consistent with this pulse pair, explaining
        your reasoning.

```{code-cell}
Image("figures/f2010_polar.png")
```

* Mr = $\Delta \phi/360.*\lambda*PRF/2$

```
  In [10]: 160./360.*5.e-2*800./2.
  Out[10]: 8.8888888888888893  m/s
```

+++

-   (4)  $d = M_r/PRF$ and
    $\frac{\phi_2 - \phi_1}{2 \pi} = \frac{ 2d}{\lambda}$ Explain
    qualitatively why these two equations makes sense, defining each of the
    terms with units.

```
% d is the distance moved by the reflector, in meters
% M_r is the radial windspeed in m/s, positive into the radar
% PRF is the pulse repitition frequency, in Hz

% So the velocity seen by the radar $M_R$ is just the distance moved, d, divided by the time over
% which it moved, which is 1/PRF

% phi_1 and phi_2 are the phase angles of the first and second pulses, in radians
% lambda is the radar wavelength, in meters  so 2d/lambda is the fraction of one wavelength
% that fits into the extra roundtrip distance that the light travels from the radar.
% One wavelength is equivalent to a phase shift of 2pi, so a fraction of a wavelength
% produces a fraction of 2pi for a phase shift
```

+++

    -   \(4) Find the maximum unambiguous velocity and range for this radar and
        use them to explain what is meant by the “doppler dilemma”

```
% In [44]: MRU =3.e8/(2*800)
% Out[44]: 187500.0  meters

% In [47]: MRmax=0.05*800/4.
% Out[47]: 10.0 m/s

% The doppler dilemma is that you can't simultaneously adjust the radar PRF to extend the
% maximum range (which requires the longest possible PRF), and the maximum detectable
% velocity (because that requires the shortest possible PRF).
```

    -   \(4) The returned power from target increases from +5 to +35 dbm,

        i\) what is the corresponding percentage increase in the returned power
        measured in dbm?

        ii\) what is the corresponding percentage increase in returned power in
        miliwatts?

        iii\) based on this why are decibels a convenient unit for reporting
        radar returns?

+++

### Problem 3

+++

-   \(10) Equilibrium temperature

    Suppose an atmosphere with a broadband (longwave) absorption optical
    depth of $\tau=1$ also absorbs 10% of the net shortwave flux, so
    that $S_0$ is 350 at the top of the atmosphere and 315 at
    the surface. If the surface is black in both the visible and the
    infrared, write down two equations for flux balance at the top of
    the atmosphere and the surface and find the resulting values of the
    equilibrium average surface $T_{sfc}$ (K) and atmospheric
    temperature $T_{atm}$ (K) that would produce those atmospheric and
    surface fluxes.

+++

%\includegraphics[width=0.4\textwidth]{up_down.png}

```
% Tr=exp(-1.666) = 0.19
% eps=1 - Tr = 1 - 0.19 = 0.81
% sigma=5.67e-8


% Top balance: -350 + Fatm + Tr*Fsfc = 0
% bot balance: -315 - Fatm + Fsfc = 0

% add:  Fsfc = 665/(1 + Tr) = 665/1.19 = 559 w/m^2
% In [19]: (559/sigma)**0.25
% Out[19]: 315.10637330185858

% sub in
% Fsfc - Fatm = 315
% Fsfc = 559 so
% Fatm = 559 - 315 = 244 = epsilon*sigma*Tatm**4.

% epsilon = 0.81 so
%   Tatm = 270 K
%  Tsfc = (551/sigma)**0.25  = 313.97 K
%In [21]: (244./(sigma*0.81))**0.25
%Out[21]: Tatm=269.97928145585706
```

```{code-cell}
sigma = 5.67e-8
epsilon = 0.81
Tatm = (244 / (sigma * epsilon)) ** 0.25
Tsfc = (551 / sigma) ** 0.25
print(f"{Tatm, Tsfc}")
```

### Question 4

+++


-   \(15) A satellite orbiting at an altitude of 800 km observes the surface
    in a thermal channel with a wavelength range of
    $10\ \mu m < \lambda < 12\ \mu m$. It looks down at the surface at a
    viewing angle of 30 degrees, as shown in this figure

    Questions:

    -   Field of view (4):

        i\) Define the solid angle, $\omega$, of a telescope’s field of view

        ii\) Use that definition to show with the help of a sketch why the solid
        angle subtended by a pixel underneath the satellite is given to a very
        good approximation by

        $$\Delta \omega = \frac{area }{R^2}$$

        where $area$ is the area of a pixel $R$ is the height of the
        satellite above the surface.

```
% The solid angle of a field of  view is just the
% area subtended by the field of view on the unit sphere.
% If the satellite is a distance R above the surface In spherical coordinates,
% is a rectangle of area  equal to
% R \times d \phi \times R \times sin \theta d \theta in the infitesimal limit.
% If theta is small, then sin theta ~ theta
%x
```

        Next, given an average optical thickness of $\tau=1$ in this
        channel, a total pixel area of 4 $km^2$ at for a pixel directly
        underneath the satellite, a mean atmospheric temperature of 260
        K and a temperature for the black surface of 300 K and an
        orbital height of $R= 800$ km, find:

    -   \(1) The field of view of the satellite, in sr

    -   \(4) The approximate flux (in $W\,m^{-2}$) in the channel

    -   \(3) The brightness temperature (in K)

    -   \(3) Now suppose the satellite scanner points at a zenith angle of 60
        degrees instead of 30 degrees. Does the observed brightness temperature
        increase or decrease? Explain.

```
from a301lib.radiation import Blambda,planckInvert
import numpy as np
omega=4./(800.**2.)
meters = 11.e-6
temp=260.
planck_atm=Blambda(meters,temp)
temp=300.
planck_sfc=Blambda(meters,temp)
mu=np.cos(30.*np.pi/180.)
Tr=np.exp(-1./mu)
sat_rad=planck_sfc*Tr + planck_atm*(1. - Tr)
tbright=planckInvert(sat_rad,meters)
delLambda=2.e-6
flux=sat_rad*omega*delLambda

print("running finalq4")
print("planck_atm: ",planck_atm,planckInvert(planck_atm,meters))
print("planck_sfc: ",planck_sfc,planckInvert(planck_sfc,meters))
print("radiance at 11 microns: ",planckwavelen(meters,290))
print("sat_rad=planck_sfc*Tr + planck_atm*(1. - Tr)",sat_rad)
print("Flux= ",sat_rad*delLambda*omega)
print("tbright: ",tbright)

mu=np.cos(60.*np.pi/180.)
Tr=np.exp(-1./mu)
sat_rad=planck_sfc*Tr + planck_atm*(1. - Tr)
print("at 60 deg, sat_rad= ",sat_rad*1.e-6)
tbright=planckInvert(sat_rad,meters)
print("at 60 deg, tbright= ",tbright)


% running finalq4
% planck_atm:  4864221.78654 260.355376839
% planck_sfc:  9573226.86713 300.392861741
% radiance at 11 microns:  8222076.64541
% sat_rad=planck_sfc*Tr + planck_atm*(1. - Tr) 6348273.67855
% tbright:  274.78569349

```

+++

### Question 5

+++

-   \(10) Water vapor

    Suppose someone gives you a matlab function that returns the total
    optical depth of the atmosphere at a frequency 175 GHz, as well as
    vertical soundings of water vapor concentration, temperature and
    pressure:

```
        function tau=calc_tau(temp,press,h2o)
        %Gven vertical profiles of temperature (K), pressure (Pa)
        %and vapor concentration (kg/m^3), return the vertical
        %optical depth at each level.  row 1 is the lowest layer in
        %atmosphere, and row(end) is the highest
```

    Explain how you would use this information to solve the
    Schwartzchild equation and predict the radiance observed by a
    satellite at that frequency looking straight down at the ocean
    (which can be assumed to be a blackbody with temperature $T_{sfc}$).
    In your explanation, provide pseudo-code (code which can be
    translated into matlab statements, but don’t actually have to be
    legal matlab). Assume that I know what the math functions exp,
    log, etc. are, but explain all other functions (diff, flipud, etc.,
    and your own functions)

    Make sure your code:

    -   Calculates the transmission as a function of height

            Step 1, calculate the vertical profile of optical depth with height

            the_tau=calc_tau(temp,press,h2o)

            and use equation 25 to get the transmission

            the_trans=exp(-the_tau)

    -   Calculates the vertical weighting function

        The vertical weight function is given by equation 26:

        $$W=\frac{ dTr}{dz} dz = dTr$$

        or in python

             W=diff(the_trans)

    -   Uses the weighting function and the temperature profile to
        calculate the upward radiance

        We need to get the total transmission an add the surface
        contribution to the contribution from each layer following
        equation 29)

             trans_tot= exp(-tau(end))
             the_rad = trans_tot*planck(Tsfc,freq) + sum(planck(temp,freq).*W)

+++

### Question 6

+++

-   \(8) Radiation

    In this course we have worked with the following quantities (among
    others):

    For each of these four quantities state:

    -   Its name including units (in the case of multiple names,
        anything that’s appeared in a textbook describing the quantity
        is ok, as long as you’re clear on what it is)

    -   How it is measured or derived, along with any assumptions that
        need to be made in obtaining it

    -   What it is used for (remote sensing, climatology, etc.), with a
        specific example


    -   I$_\lambda$

```
%
% monochromatic radiance (W/m^2/sr/micron)
% power received on a perpendicular unit area from a specific
%  direction, in a specific field of view, in a given wavelength range
%used in remote sensing problems because it gives the directional
%dependence of the radiation and is conserved with distance in a vacumn
%
```
    -   $F = I_\lambda \Delta \lambda \Delta \omega$

```
%
% total flux (W/m^2) arriving in a satellite channel
%  power crossing a surface from a narrow field of view in a wavelength
%   range
% assumption:  parallel beam/narrow field of view, plus narrow channel
% application -- how much energy is reaching a satellite in a particular
%   channel
%
%
```
    -   $F_\lambda = \pi I_\lambda$
```
%
% monochromatic flux (W/m^2/micron)
%  power crossing a perpendicular unit area from all directions in a hemisphere,
%  assumption:  isotropic radiance I_\lambda independent of direction
%  application -- heating rate due to photons in a particular wavelength
%
```

    -   $F = \sigma T^4$
```
%
%  broad band emitted flux (W/m^2)
%  the perpendicular component of the power emitted from a black surface of unit area into a hemisphere
%   from all wavelengths
% application -- heating/cooling rates of surface
%
```


**Useful Equations:**

<span>2</span>

------------------------------------------------------------------------

$~$

$~$

$$\begin{aligned}
  \label{eq:nu}
  \nu &=& c / \lambda\\
   E &=& h \nu\end{aligned}$$

$$\label{eq:omega}
  d \omega = \sin \theta d\theta d\phi = -d\mu d\phi$$

$$\label{eq:cos}
  S = S_0 \cos(\theta)$$

$$\label{eq:conservation}
  a_\lambda + r_\lambda + t_\lambda = 1$$

$$\label{eq:intensity}
  I_\lambda = \frac{\delta F}{\delta \omega \delta \lambda}$$

$$\label{planck}
B_\lambda(T)  = \frac{h c^2}{\lambda^5 \left [ \exp (h c/(\lambda k_B T )) -1 \right ] }$$

$$\label{eq:pi}
  F_{\lambda\,BB} = \pi B_\lambda$$

$$\label{eq:stefan}
  F_{BB}=\sigma T^4$$

$$\label{eq:fluxdiv}
  \frac{dT}{dt} = \frac{-1}{\rho c_{pd}} \frac{dF_n}{dz}$$

$$\label{eq:taylor}
  F_\lambda(T) \approx F_{\lambda\, 0} + \left .\frac{dF_\lambda}{dT}  \right |_{T_0,\lambda} \!\!\! (T - T_0) + \ldots$$

$$\label{eq:exp}
  \exp(x) = 1 + x +  \frac{x^2}{2} + \frac{3^2}{3!} + \ldots$$

$$\sin(\theta) = \theta - \frac{\theta^3}{3!} + \frac{\theta^5}{5!} + \ldots$$

$$\cos(\theta) = 1 -  \frac{\theta^2}{2!} + \frac{\theta^4}{4!} + \ldots$$

$~$

------------------------------------------------------------------------

$~$

$~$

Beer’s law for extinction: $$\begin{aligned}
  \label{eq:extinct}
\frac{dI_\lambda}{I_\lambda}  & = & - \kappa_{\lambda\, s} \rho_{g} ds -
                    \kappa_{\lambda\,a } \rho_{g} ds \nonumber\\
        &=& - \kappa_{\lambda e} \rho_{g} ds\end{aligned}$$ (assuming
$\rho_{a}$=$\rho_{s}$=$\rho_{g}$).

$~$

Hydrostatic equation:

$$\label{eq:hydro}
  dp = -\rho_d\, g\, dz$$

$~$

Equation of state

$$\label{eq:state}
  p = R_d \rho_d T$$

$~$

absorption optical thickness:

$$\label{eq:tauThick}
  \tau(s_1, s_2 ) = \int_{s_1}^{s_2} \beta_a\, ds^\prime$$

where $\beta_a$=$\rho_{absorber} \kappa$

vertical optical thickness:

$$\label{eq:tauup}
  \tau(z_1, z_2 ) = \int_{z_1}^{z_{2}} \beta_a\, dz^\prime$$

$~$

Vertical optical thickness for downward radiation at the surface:

$$\label{eq:taudown1}
  \tau^{\downarrow}(0,z) = \int_0^z \beta_a \, dz^\prime$$

$~$

Vertical optical depth for upward radiation at the top of the
atmosphere:

$$\label{eq:taudown2}
  \tau^{\uparrow}(z,z_T) = \int_z^{z_T} \beta_a \, dz^\prime$$

Liebniz’ rule:

$$\begin{aligned}
  \label{eq:taudown}
 \frac{ d \tau^{\uparrow}(z,z_T)}{dz} &=& - \beta_a \\
 \frac{ d \tau^{\downarrow}(0,z)}{dz} &=&  \beta_a \end{aligned}$$

$~$

Transmission functions (plane parallel atmosphere):

$$\begin{aligned}
Tr^\uparrow (z, z_T) &=& \exp ( - \tau^{\uparrow}(z,z_T)/\mu ) \nonumber\\
Tr^\downarrow (0, z) &=& \exp ( - \tau^{\downarrow}(0,z)/\mu )\end{aligned}$$

$~$

Weighting functions:

$$\begin{aligned}
W^\uparrow (z) &=& \frac{dTr^\uparrow (z,z_T)}{dz} =  \frac{\beta_a (z)}{\mu} Tr^\uparrow (z,z_T)   \nonumber\\
W^\downarrow (z) &=& - \frac{dTr^\downarrow (0,z)}{dz} =  \frac{\beta_a (z)}{\mu} Tr^\downarrow (0,z)   \nonumber\\\end{aligned}$$

$~$

Schwarzchild’s equation

$$\label{eq:schwarz}
  dI = -I\, \beta_a\, ds + B_{\lambda}(s) \, \beta_a \, ds$$

$~$

Some integrated forms of (\[eq:schwarz\]):

$~$

Downwelling intensity at the surface:

$$\label{eq:top1}
  I^\downarrow (0,\mu) = I^\downarrow (z_T,\mu) \, Tr_T + \int_0^{z_T} B(z)\, W^\downarrow (z,\mu)\,dz$$

$~$

Upwelling intensity at the top of the atmosphere:

$$\label{eq:top2}
  I^\uparrow (z_T,\mu) = I^\uparrow (0,\mu) \, Tr_T + \int_0^{z_T} B(z)\, W^\uparrow (z,\mu)\,dz$$

$~$

In terms of transmission

$$\label{eq:top3}
  I^\uparrow (z,\mu) = I^\uparrow (0,\mu) \, Tr(0,z) + \int_0^{z} B(z^\prime)\, dTr(z^\prime,z)$$

$~$

In terms of the temperature profile (assuming a black surface and no
temperature jump between surface and bottom of the atmosphere):

$$\label{eq:top4}
  I^\uparrow (z_T,\mu) = I^\uparrow (0,\mu) + \int_0^{z_T} a(z) \frac{dB}{dz} \, dz$$

Radar

Rayleigh scattering $$\label{eq:scatter}
  \frac{I}{I_0} \propto \frac{D^6}{\lambda^4}$$

$$\label{eq:radar}
  \mathrm{Returned\ power} \propto |k^2| \frac{Z}{r^2}$$

where $|k^2| \approx 0.2$ for ice and 0.9 for liquid water.

$$\label{eq:Z}
  Z = \int_0^\infty n(D) D^6 dD$$

Z-R relationship

$$\label{eq:zr}
  Z = 300 RR^{1.4}$$

(rain, RR in mm/hr, Z in $mm^6/m^3$)

$$\label{eq:range}
  MUR = \frac{c}{2 \cdot \mathrm{PRF}}$$

Doppler radar

$$\Delta \nu = \frac{2\,M_r}{\lambda}$$

$$\label{eq:phase}
\frac{\Delta \phi} {2 \pi} = \frac{ 2d}{\lambda} = \frac{ 2 T_r M_r}{\lambda}$$

$$\label{eq:mrmax}
  M_{r\,max} = \lambda \cdot \mathrm{PRF}/4$$

------------------------------------------------------------------------

$~$

Useful constants:

$~$

$c_{pd}=1004$ ,

$\sigma=5.67 \times  10^{-8}$

$k_b = 1.381  \times 10^{-23}$

$c=3 \times 10^{8}$

$h=6.626 \times 10^{-34}$

$\pi \approx 3.14159$

$R_d=287 \un{J\,kg^{-1}\,K^{-1}}$

```{code-cell}

```
