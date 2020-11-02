---
jupytext:
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---
(assign2_sol)=
# Assignment 2 - solutions

Chapter 2: A23, A24, A25, A26
Chapter 8: A2, A4

```{code-cell} ipython3
import numpy as np
import string
```

## 2-A23

What product of number density times absorption cross section is needed in order for 50% of the incident radiation to be absorbed by airborne volcanic ash over the following path length (km)?

Given Equation 2.31a:

$$
\begin{align}
E_{\text {transmitted}}&=E_{\text {incident}} \cdot \mathrm{e}^{-n \cdot b \cdot \Delta s}\\
t &= 0.5 = \mathrm{e}^{-n \cdot b \cdot \Delta s}
\end{align}
$$
What product of number density $n$ times absorption cross section  $b$ is needed in order for 50% of the incident radiation $E_{\text {incident}}$ to be absorbed by airborne volcanic ash over the following path length (km)?

(Note how I use the zip function to zip together 3 lists, then unzip them in the for loop
one at a time)

```{code-cell} ipython3
# path length in km
# 14 values
delta_s = (0.2,0.4,0.6,0.8,1.0,1.5,2.0,
           2.5,3.0,3.5,4.0,4.5,5.0,7.0)
letters = string.ascii_lowercase[:len(delta_s)]
# unpack the product of n x b
#
n_b= []

for the_delta in delta_s:
    the_prod = -np.log(0.5)/the_delta
    n_b.append(the_prod)
    
the_answer = zip(letters,delta_s,n_b)
for the_letter, the_delta, the_val in the_answer:
    print(f"{the_letter}) delta_s={the_delta} km,"
          f" --- nxb={the_val:5.3f} km^-1")
```

## 2-A24 

Given optical depth $\tau$ in the equation 2.31c

\$$E_{\text {transmitted}}=E_{\text {incident}} \cdot \mathrm{e}^{-\tau}$$

What fraction of incident radiation is transmitted through a volcanic ash cloud of optical depth:

```{code-cell} ipython3
tau =(0.2,0.5,0.7,1.0,1.5,3.0,
      4.0,5.0,6.0,7.0,10.0,15.0,20.0)
letters = string.ascii_lowercase[:len(tau)]
frac_list=[]
for the_tau in tau:
    the_frac = np.exp(-the_tau)
    frac_list.append(the_frac)
the_answer = zip(letters,tau,frac_list)
for the_letter, the_tau, the_frac in the_answer:
    print(f"{the_letter}) tau={the_tau},"
          f" --- transmissivity={the_frac:5.3f}")
```

## 2-A25 

given $\gamma = n \cdot b = k \cdot \rho$

Find the visial range $\Delta s$ such that the tranmissivity = 


$$
\begin{align}
t &= 0.02 = \exp ( -\gamma \cdot \Delta s) \\
\Delta s &= -\log(0.02)/\gamma\ (meters)
\end{align}
$$

```{code-cell} ipython3
gamma = (0.00001,0.00002,0.00005,0.0001,
         0.0002,0.0005,0.001,0.002,0.005,
         0.01,0.02,0.05)
gamma_km = np.array(gamma)*1.e3  #km^{-1}
letters = string.ascii_lowercase[:len(gamma_km)]
delta_list= []

for the_gamma in gamma_km:
    delta_s = -np.log(0.02)/the_gamma
    delta_list.append(delta_s)
the_answer = zip(letters,gamma_km,delta_list)
for the_letter, the_gamma, delta_s in the_answer:
    print(f"{the_letter}) gamma ={the_gamma} km^{-1},"
          f" --- Delta s={delta_s:5.3f} km")
```

## 2-A26 

(i) What is the value of solar downward direct radiative flux reaching the surface at the city from exercise A5 at noon on 4 July, given 20% coverage of cumulus (low) clouds.

+++

Eq. 2.5

$$
\delta_{S} \approx \Phi_{r} \cdot \cos \left[\frac{C \cdot\left(d-d_{r}\right)}{d_{y}}\right]
$$


Eq. 2.6:


$$
\begin{aligned}
\sin (\Psi)=& \sin (\phi) \cdot \sin \left(\delta_{S}\right)-\\
& \cos (\phi) \cdot \cos \left(\delta_{S}\right) \cdot \cos \left[\frac{C \cdot t_{U T C}}{t_{d}}+\lambda_{e}\right]
\end{aligned}
$$

+++

## Timezones/leap years/daylight savings time make dates/times complicated

For example, look at [this headache for daylight savings time folding](https://www.python.org/dev/peps/pep-0495/)
I would use the [arrow package](https://github.com/arrow-py/arrow) for real work

```{code-cell} ipython3
import datetime as dt
from math import asin,sin,cos,pi
import numpy as np
try:
    #
    # use the ephem package to find exact summer solstice
    #
    import ephem
except ModuleNotFoundError:
    pass
        

deg2rad=pi/180.
rad2deg=1./deg2rad

def find_deltas(the_date):
    """given a python datetime object (UTC)
       find the solar declination angle in degrees
       using Stull equation 2.5

       Parameters
       ----------
       
       the_date: datetime object with UTC timezone
       
       Returns
       -------
       
       deltas:  solar declination angle in degrees
    """
    the_year=the_date.year
    #
    # find the length of the year (leap or regular) in days by subtracting
    # two datetimes exactly 1 year apart -- jan 1, 0 hours, 0 minutes, 0 seconds
    # 
    year_start=dt.datetime(the_year,1,1,0,0,0,tzinfo=dt.timezone.utc)
    year_end=dt.datetime(the_year+1,1,1,0,0,0,tzinfo=dt.timezone.utc)
    year_length=(year_end - year_start).days
    print(f"this year has {year_length:6.3f} days")
    phir=23.44 #axis tilt in degrees from stull
    #
    # run the following if you have the ephem package
    # to get the exact solstice.  Make sure you get the
    # summer solstice by specifying solstice after May 31
    #
    try:
        approx_solstice = dt.datetime(2020,5,31)
        solstice=ephem.next_solstice(approx_solstice).datetime()
        solstice = solstice.astimezone(dt.timezone.utc)
    except:     
    #
    # otherwise use june 21
    #
        solstice = dt.datetime(2020,6,21,0,0,0,tzinfo=dt.timezone.utc)
    #number of days since the new year
    the_day=(the_date - year_start).days
    jan1=dt.datetime(the_date.year,1,1,0,0,0,tzinfo=dt.timezone.utc)
    solstice_day=(solstice - jan1).days
    #print('solstice has {} days'.format(solstice_day))
    fraction=(the_day - solstice_day)/year_length
    deltas=phir*cos(2*pi*fraction)
    return deltas
```

```{code-cell} ipython3
def find_elevation(the_date,the_lat,the_lon):
    """find the solar elevation for a location in degrees 
       datetime object with a UTC timezone representing
       local time, using Stull eqn. 2.6

       Parameters
       ----------
       the_date: datetime object
           time in UTC
       the_lat: float
           degrees North
       the_lon: float
           degrees East
           
       Returns
       -------
       
       elevation: float
          solar elevation in degrees
    """
    deltas=find_deltas(the_date)
    deltas=deltas*deg2rad
    phi= the_lat*deg2rad # latitude deg N
    lambda_e = the_lon*deg2rad #longitude, deg E
    #
    #  turn minutes into fractions of an hour
    #
    t_utc=the_date.hour + the_date.minute/60.
    print(f"the longitude: {the_lon:5.2f} deg E, hour in utc {t_utc}")
    #stull eqn 2.6
    sin_psi=sin(phi)*sin(deltas) - cos(phi)*cos(deltas)*cos(2*pi*t_utc/24. + lambda_e)
    elevation=asin(sin_psi)*rad2deg
    #write 0 if under the horizon
    if elevation < 0:
        elevation=0.
    return elevation
```

Start accumulating results in a dictionary for each part of A26.  We will key on the city
and each city will have its own dictionary.

```{code-cell} ipython3
#
# these time offsets are all standard time
# credit:  Marjolein Ribberink
#
coords={
    "Seattle":(47.6062, -122.3321,-8),
    "Corvallis":(44.5646, -123.2620,-8),
    "Boulder":(40.0150, -105.2705,-7),
    "Norman":(35.2226, -97.4395,-6),
    "Madison":(43.0731, -89.4012,-6),
    "Toronto":(43.6532, -79.3832,-5),
    "Montreal":(45.5017, -73.5673,-5),
    "Boston":(42.3601, -71.0589,-5),
    "NYC":(40.7128, -74.0060,-5),
    "University Park":(40.8148, -77.8653,-5),
    "Princeton":(40.3431, -74.6551,-5),
    "Washington DC":(38.9072, -77.0369,-5),
    "Raleigh":(35.7796, -78.6382,-5),
    "Tallahassee":(30.4383, -84.2807,-5),
    "Reading":(51.4543, -0.9781,0),
    "Toulouse":(43.6047, 1.4442,1),
    "Munchen":(48.1351, 11.5820,1),
    "Bergen":(60.3913, 5.3221,1),
    "Uppsala":(59.8586, 17.6389,1),
    "DeBilt":(52.1093, 5.1810,1),
    "Paris":(48.8566, 2.3522,1),
    "Tokyo":(35.6804, 139.7690,8),
    "Beijing":(39.9042, 116.4074,7),
    "Warsaw":(52.2297, 21.0122,1),
    "Madrid":(40.4168, 3.7038,1),
    "Melbourne":(-37.8136, 144.9631,10),
    "Vancouver":(49.2827, -123.1207,-8)
}

city_list = ['Vancouver','Reading','Norman']
results=dict()
for the_city in city_list:
    print(f"\n{the_city}\n")
    geocoords = coords[the_city]
    the_lat, the_lon, tz_offset = geocoords
    hour = 12 - tz_offset
    the_date = dt.datetime(2020,6,21,hour,0,0,tzinfo=dt.timezone.utc)
    elev=find_elevation(the_date,the_lat,the_lon)
    print(f"lat {the_lat:5.2f} deg N, solar elev {elev:5.2f} deg")
    results[the_city]={'elevation':elev}
print(f"\n{results}\n")
```

### 2-A26a 

find the flux at the surface given Stull 2.35

$$
T_{r}=(0.6+0.2 \sin \Psi)\left(1-0.4 \sigma_{H}\right)\left(1-0.7 \sigma_{M}\right)\left(1-0.4 \sigma_{L}\right)
$$

with $\sigma_L=0.2$

```{code-cell} ipython3
def find_Tr(elevation,sigma_h,sigma_m,sigma_l):
    """
    given a solar elevation and cloud fractions for 3 layers
    find the effective solar flux transmission
    
    Parameters
    ----------
    
    elevation: float
       solar elevation in degrees
    sigma_h, sigma_m,sigma_l: floats
       high, middle and low cloud fractions, 0 to 1
       
    Returns
    -------
    Tr: float
       the diffuse and direct flux transmission, 0 to 1
    """
    import numpy as np
    deg2rad = np.pi/180.
    elevation = elevation*deg2rad
    S0 = 1361
    Tr = (0.6 + 0.2*np.sin(elevation))*(1-0.4*sigma_h)*(1-0.7*sigma_m)*(1-0.4*sigma_l)
    print(f"cos(theta) factor is {np.sin(elevation):5.2f}")
    return Tr
```

```{code-cell} ipython3
for the_city, results_dict in results.items():
    print(f"\n{the_city}\n")
    geocoords = coords[the_city]
    the_lat, the_lon, tz_offset = geocoords
    hour = 12 - tz_offset
    the_date = dt.datetime(2020,6,21,hour,0,0,tzinfo=dt.timezone.utc)
    elev=find_elevation(the_date,the_lat,the_lon)
    sigma_h, sigma_m, sigma_l = 0, 0, 0.2
    Tr = find_Tr(elev,sigma_h,sigma_m,sigma_l)
    S0= -1361 #W/m^2
    downward_flux = S0*Tr
    print(f"high, middle, low cloud fractions: {sigma_h,sigma_m,sigma_l}")
    print(f"the diffuse/direct transmissin is {Tr:5.3f}")
    print(f"downward flux at the surface is {downward_flux:5.2f} W/m^2" )
    results[the_city]['downward_flux'] = downward_flux
    results[the_city]['high_med_low'] = (sigma_h,sigma_m,sigma_l)
print(f"\n{results}\n")
```

## 2-A26b

If the albedo is 0.5 in your town, what is the reflected solar flux at that same time

Stull 2.36
$$K_{\uparrow} = -A \cdot K_{\downarrow}$$

```{code-cell} ipython3
for the_city, results_dict in results.items():
    flux = results_dict['downward_flux']
    albedo = 0.5
    upward_flux = -albedo*flux
    print(f"{the_city}: {upward_flux:5.2f} W/m^2")
    results[the_city]['upward_sw'] = upward_flux
    results[the_city]['albedo'] = albedo
print(f"\n{results}\n")
```

### 2-A26c

What is the approx net longwave flux at the surface, according to Stull 2.39?

$$I^{*}=b \cdot\left(1-0.1 \sigma_{H}-0.3 \sigma_{M}-0.6 \sigma_{L}\right)$$

```{code-cell} ipython3
b = 98.5  #W/m^2
for the_city,results_dict in results.items():
    sigma_h, sigma_m, sigma_l = results_dict['high_med_low']
    Istar = b*(1 - 0.1*sigma_h -0.3*sigma_m - 0.6*sigma_l)
    results[the_city]['Istar']=Istar
    print(f"{the_city}: {Istar:5.2f} W/m^2")
print(f"\n{results}\n")
```

### 2-A26d

What is the net surface radiation according to Stull 2.40a

$$\mathbb{F}^{*}=-(1-A) \cdot S \cdot T_{r} \cdot \sin (\Psi)+I^{*}$$

Note that in the loop below I can add things to `results_dict`, and the changes "stick"
i.e. the for loop is giving me a reference to the original `results_dict`
not a copy

```{code-cell} ipython3
for the_city, results_dict in results.items():
    A = results_dict['albedo']
    downward_flux = results_dict['downward_flux']
    Istar = results_dict['Istar']
    net_sfc_flux = -(1 - A)*downward_flux + Istar
    print(f"{the_city}: {net_sfc_flux:5.2f} W/m^2")
    results_dict['net_sfc_flux'] = net_sfc_flux
print(f"\n{results}\n")
    
```

### 8-A2 

Find the blackbody radiance for the following sets of wavelength, temperature

```{code-cell} ipython3
from scipy.constants import c, h, k
#
# get Stull's c_1 and c_2 from fundamental constants
#
# c=2.99792458e+08  #m/s -- speed of light in vacuum
# h=6.62606876e-34  #J s  -- Planck's constant
# k=1.3806503e-23  # J/K  -- Boltzman's constant

c1 = 2. * h * c**2.
c2 = h * c / k
sigma = 2. * np.pi**5. * k**4. / (15 * h**3. * c**2.)

def calc_radiance(wavel, Temp):
    """
    Calculate the blackbody radiance
    
    Parameters
    ----------

      wavel: float or array
           wavelength (meters)

      Temp: float
           temperature (K)

    Returns
    -------

    Llambda:  float or arr
           monochromatic radiance (W/m^2/m/sr)
    """
    Llambda_val = c1 / (wavel**5. * (np.exp(c2 / (wavel * Temp)) - 1))
    return Llambda_val

def planck_invert(wavel, Lstar):
    """
    Calculate the brightness temperature
    
    Parameters
    ----------

      wavel: float
           wavelength (meters)

      Lstar: float or array
           Blackbody radiance (W/m^2/m/sr)
    Returns
    -------

    Tbright:  float or arr
           brightness temperature (K)
    """
    Tbright = c2 / (wavel * np.log(c1 / (wavel**5. * Lstar) + 1.))
    return Tbright
```

```{code-cell} ipython3
probset={
    "a":{'wavelen':14.7,'Tc':-60},
    "b":{'wavelen':14.4,'Tc':-60},
    "c":{'wavelen':14.0,'Tc':-30},
    "d":{'wavelen':13.7,'Tc':0},
    "e":{'wavelen':13.4,'Tc':5},
    "f":{'wavelen':12.7,'Tc':15},
    "g":{'wavelen':12.0,'Tc':25},
    "h":{'wavelen':11.0,'Tc':-5},
    "i":{'wavelen':9.7,'Tc':-15}
}

for letter, prob_vals in probset.items():
    Tk = prob_vals['Tc'] + 273.15
    wavelen = prob_vals['wavelen']*1.e-6
    Lbb = calc_radiance(wavelen,Tk)
    print(f"{letter}) Tk={Tk:5.2f} K, Lbb={Lbb*1.e-6:5.2f} W/m^2/sr/micron")
     
    
```

### 8-A4 

Find the brightness temperature for the following wavelengths given a radiance of $10^{-15}$ W/m^2/sr/micron.

```{code-cell} ipython3
wavelen = (0.6,3.8,4.0,4.1,4.4,4.5,4.6,6.5,7.0,7.5)
letters = string.ascii_lowercase[:len(wavelen)]

Lstar=(10**(-15))*1.e6  #W/m^2/sr/micron

for letter,wavel in zip(letters,wavelen):
    wavel_meters=wavel*1.e-6
    Tbright = planck_invert(wavel_meters,Lstar)
    print(f"{letter}) Wavelength = {wavel:5.2f} microns, Tbright = {Tbright:5.2f} K")
    
```
