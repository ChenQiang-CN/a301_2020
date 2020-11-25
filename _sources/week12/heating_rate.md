---
jupytext:
  cell_metadata_filter: -all
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.7.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
```
(heating_profiles)=
# Heating rate profiles

In {ref}`heating_rate` we showed that the heating rate $Q_r$ (K/s) for a particular height in
the atmosphere was defined by:

$$
\begin{aligned}
\rho c_p \Delta z \frac{dT}{dt} &= \Delta E_n\\
Q_r = \frac{dT}{dt} &= \frac{1}{\rho c_p} \frac{\Delta E_n}{\Delta z} = \frac{1}{\rho c_p} \frac{dE_n}{dz}
\end{aligned}
$$

where $E_n$ was the net flux integrated overall wavelengths (positive downwards).

In this notebook we use the hydrostatic equation  from {ref}`hydro` and the flux equation
from {ref}`flux_schwartzchild` to find dT/dz as a function of height for an atmosphere with
containing an absorbing gas with a mixing ratio of $r_gas=0.01$ kg/kg and a mass absorption coefficient
averaged across all longwave wavelengths of $k=0.01$   $m^2/kg$.

+++

## Integrate the atmospheric pressure, temperature and density

Since we know that 

$$
dp = \rho g dz
$$

for a hydrostatic atmosphere, if we assume that dT/dz is constant with height, we can
build up an atmosphere one level at a time, but starting with know $p$, $\rho$ and $T$ at the
surface and using the values of $dT/dz$, $dp/dz$  to find $T$ and $p$ at the next level.  Once
we have those, we can use the ideal gas law to find the density $\rho$ and move up.

This is done in the cell below.

```{code-cell} ipython3
def hydrostat(T_surf,p_surf,dT_dz,delta_z,num_levels):
    """
       build a hydrostatic atmosphere by integrating the hydrostatic equation from the surface,
       using num_levels of constant thickness delta_z
       input:  T_surf -- surface temperature in K
              p_surf -- surface pressure in Pa
              dT_dz -- constant rate of temperature change with height in K/m
              delta_z  -- layer thickness in m
              num_levels -- number of levels in the atmosphere
       output:
              numpy arrays: Temp (K) , press (Pa), rho (kg/m^3), height (m)
    """
    Rd=287. #J/kg/K  -- gas constant for dry air
    g=9.8  #m/s^2
    Temp=np.empty([num_levels])
    press=np.empty_like(Temp)
    rho=np.empty_like(Temp)
    height=np.empty_like(Temp)
    #
    # level 0 sits directly above the surface, so start
    # with pressure, temp of air equal to ground temp, press
    # and get density from equaiton of state
    #
    press[0]=p_surf
    Temp[0]=T_surf
    rho[0]=p_surf/(Rd*T_surf)
    height[0]=0
    num_layers=num_levels - 1
    #now march up the atmosphere a layer at a time
    for i in range(num_layers):
        delP= -rho[i]*g*delta_z
        height[i+1] = height[i] + delta_z
        Temp[i+1] = Temp[i] + dT_dz*delta_z
        press[i+1]= press[i] + delP
        rho[i+1]=press[i+1]/(Rd*Temp[i+1])
    return (Temp,press,rho,height)
```

## Next we can find the optical depth 

If we have the air density $\rho$, the mixing ratio $r_{mix}$ asnd  the absorption coefficient $k$ from Stull Chapter 2
section 2.3.6 we can find the optical depth in the layer:

$$
\tau = \rho r_{mix} k \Delta z
$$

where $\Delta z$ is the layer thickness.  That's done in the next cell.

```{code-cell} ipython3
def find_tau(r_gas,k,rho,height):
    """
       input: r_gas -- gas mixing ratio in kg/kg
              k -- mass absorption coefficient in kg/m^2
              rho -- vector of air densities in kg/m^3 at each level
              height -- corresponding level heights in m
       output:  tau -- vetical optical depth from the surface, same shape as rho
    """
    tau=np.empty_like(rho)
    tau[0]=0
    num_levels=len(rho)
    num_layers=num_levels - 1
    for index in range(num_layers):
        delta_z=height[index+1] - height[index]
        delta_tau=r_gas*rho[index]*k*delta_z
        tau[index+1]=tau[index] + delta_tau
    return tau
```

## Flux with height

Note the factor of 1.666 below that multiplies the optical depth in
the transmission -- this is the flux diffusivity approximation.  The function below
solves for the upward and downward fluxes one layer at at time by calculating
the transmitted flux arriving from the bottom or the top of the layer, and the
emitted flux that the layer is sending to the next layer above or below using the equation given in
{math:numref}`layer_flux`. This is the
"two stream approximation" mentioned in {ref}`two_stream`

```{code-cell} ipython3
def fluxes(tau,Temp,height,T_surf):
    sigma=5.67e-8 #W/m^2/K^4
    up_flux=np.empty_like(height)
    down_flux=np.empty_like(height)
    sfc_flux=sigma*T_surf**4.
    up_flux[0]=sfc_flux
    tot_levs=len(tau)
    for index in np.arange(1,tot_levs):
        upper_lev=index
        lower_lev=index - 1
        del_tau=tau[upper_lev] - tau[lower_lev]
        trans=np.exp(-del_tau)
        emiss=1 - trans
        layer_flux=sigma*Temp[lower_lev]**4.*emiss
        #
        # find the flux at the next level
        #
        up_flux[upper_lev]=trans*up_flux[lower_lev] + layer_flux
    #
    # start at the top of the atmosphere
    # with zero downwelling flux
    #
    down_flux[tot_levs-1]=0
    #
    # go down a level at a time, adding up the fluxes
    #
    for index in np.arange(1,tot_levs):
        upper_lev=tot_levs - index
        lower_lev=tot_levs - index -1
        del_tau=tau[upper_lev] - tau[lower_lev]
        trans=np.exp(-1.666*del_tau)
        emiss=1 - trans
        layer_flux=sigma*Temp[upper_lev]**4.*emiss
        down_flux[lower_lev]=down_flux[upper_lev]*trans + layer_flux
    return (up_flux,down_flux)
```

```{code-cell} ipython3
def heating_rate(net_up,height,rho):
    cpd=1004.
    #
    # find the flux divergence across the layer
    # by differencing the levels
    #
    rho_mid=(rho[1:] + rho[:-1])/2.
    dEn_dz= -1.*np.diff(net_up)/np.diff(height)
    dT_dz=dEn_dz/(rho_mid*cpd)
    return dT_dz
```

```{code-cell} ipython3
def main():
    r_gas=0.01  #kg/kg
    k=0.01  #m^2/kg
    T_surf=300 #K
    p_surf=100.e3 #Pa
    dT_dz = -7.e-3 #K/km
    delta_z=1
    num_levels=15000
    Temp,press,rho,height=hydrostat(T_surf,p_surf,dT_dz,delta_z,num_levels)
    tau=find_tau(r_gas,k,rho,height)
    up,down=fluxes(tau,Temp,height,T_surf)
    dT_dz=heating_rate(up - down,height,rho)

    fig1,axis1=plt.subplots(1,1,figsize=(10,10))
    axis1.plot(up,height*0.001,'b-',lw=5,label='upward flux')
    axis1.plot(down,height*0.001,'g-',lw=5,label='downward flux')
    axis1.set_title('upward and downward fluxes')
    axis1.set_xlabel('flux $(W\,m^{-2}$')
    axis1.set_ylabel('height (km)')
    axis1.legend(numpoints=1,loc='best')

    fig2,axis2=plt.subplots(1,1,figsize=(10,10))
    axis2.plot(up-down,height*0.001,'b-',lw=5)
    axis2.set_title('net upward flux')
    axis2.set_xlabel('net upward flux $(W\,m^{-2})$')
    axis2.set_ylabel('height (km)')

    fig3,axis3=plt.subplots(1,1,figsize=(10,10))
    dT_dz=dT_dz*3600.
    mid_height=(height[1:] + height[:-1])/2.
    axis3.plot(dT_dz,mid_height*0.001,'b-',lw=5)
    axis3.set_title('heating rate')
    axis3.set_xlabel('heating rate in K/hr')
    axis3.set_ylabel('height (km)')
```

```{code-cell} ipython3
main()
```
