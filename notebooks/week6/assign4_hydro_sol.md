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

(assign4_hydro_sol)=
# Assignment 4 solution, integrated vapor path

+++

## Read soundings into pandas

There are five different average profiles for the tropics, subarctic summer, subarctic winter, midlatitude summer, midlatitude winter.  These are called the US Standard Atmospheres.  This notebook shows how to read and plot the soundings, and calculate the pressure and density scale heights.

```{code-cell} ipython3
from matplotlib import pyplot as plt
import matplotlib.ticker as ticks
import pdb
import numpy as np
import a301_lib
from pprint import pprint,pformat
import pandas as pd
import json
from pathlib import Path
```

## Reuse code from {ref}`scale_heights` notebook

Read the csv files and make a dictionary call

```{code-cell} ipython3
soundings_folder= a301_lib.data_share / Path('soundings')
sounding_files = list(soundings_folder.glob("*csv"))
```

### use the stem of the filename as a dictionary key

```{code-cell} ipython3
sound_dict={}
for item in sounding_files:
    sound_dict[item.stem]=pd.read_csv(item)
    print(f"{item.stem}\n"
          f"{sound_dict[item.stem].head()}")
```

We use these keys to get a dataframe with 6 columns, and 33 levels.  Here's an example for the midsummer sounding

```{code-cell} ipython3
midsummer=sound_dict['midsummer']
print(midsummer.head())
list(midsummer.columns)
```

### Plot  temp and vapor mixing ratio rmix ($\rho_{H2O}/\rho_{air}$)

```{code-cell} ipython3
%matplotlib inline
plt.style.use('ggplot')
meters2km=1.e-3
plt.close('all')
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(11,8))
for a_name,df in sound_dict.items():
    ax1.plot(df['temp'],df['z']*meters2km,label=a_name)
    ax1.set(ylim=(0,40),title='Temp soundings',ylabel='Height (km)',
       xlabel='Temperature (K)')

    ax2.plot(df['rmix']*1.e3,df['z']*meters2km,label=a_name)
    ax2.set(ylim=(0,8),title='Vapor soundings',ylabel='Height (km)',
       xlabel='vapor mixing ratio (g/kg)')
ax1.legend()
_=ax2.legend()
```

## Calculate the pressure scale height

```{code-cell} ipython3
g=9.8  #don't worry about g(z) for this exercise
Rd=287.  #kg/m^3

def calcScaleHeight(df):
    """
    Calculate the pressure scale height H_p

    Parameters
    ----------

    df: dataframe with the following columns

    df['temp']: vector (float)
      temperature (K)

    df['z']: vector (float) of len(df)
      with the height in m

    Returns
    -------

    Hbar: vector (float) of len(df)
      pressure scale height (m)

    """
    z=df['z'].values
    Temp=df['temp'].values
    dz=np.diff(z)
    TLayer=(Temp[1:] + Temp[0:-1])/2.
    oneOverH=g/(Rd*TLayer)
    Zthick=z[-1] - z[0]
    oneOverHbar=np.sum(oneOverH*dz)/Zthick
    Hbar = 1/oneOverHbar
    return Hbar
```

## calculate the density scale height

```{code-cell} ipython3
def calcDensHeight(df):
    """
    Calculate the density scale height H_rho

    Parameters
    ----------

    df: dataframe with the following columns

    df['temp']: vector (float)
      temperature (K)

    df['z']: vector (float) of len(df)
      with the height in m

    Returns
    -------

    Hbar: vector (float) of len(T)
      density scale height (m)
    """
    z=df['z'].values
    Temp=df['temp'].values
    dz=np.diff(z)
    TLayer=(Temp[1:] + Temp[0:-1])/2.
    dTdz=np.diff(Temp)/np.diff(z)
    oneOverH=g/(Rd*TLayer) + (1/TLayer*dTdz)
    Zthick=z[-1] - z[0]
    oneOverHbar=np.sum(oneOverH*dz)/Zthick
    Hbar = 1/oneOverHbar
    return Hbar
```

<a name="oct7assign"></a>

### Assigment 4

#### Question 4a -- scale height

a) Calculate the pressure scale height for each of the five atmospheres using calcScaleHeightFill the dictionary below (soution_4a_dict) with the five values you calculate using
calcScaleHeight

```{code-cell} ipython3
sound_names=list(sound_dict.keys())
dummy_answers=np.ones([len(sound_names)])*np.nan
solution_4a_dict=dict(zip(sound_names,dummy_answers))
print(f"here is the dictionary that will hold  my answers:\n "
       f"{pformat(solution_4a_dict)}")
```

```{code-cell} ipython3
#
# set the top height at 10 km
#
ztop = 10.e3  #meters
#
# loop through the dataframes,
# calling calcScaleHeight on each
# and saving the result in
# as an entry solution_4a_dict[name]
#
for name,df in sound_dict.items():
    #
    # limit the data frame to the heights below ztop
    #
    df = df.loc[df['z']<ztop]
    press_height = calcScaleHeight(df)
    solution_4a_dict[name]=np.round(press_height)

#
# print the answer and save a afile
#
answer_file = Path() / 'assign4a_answer.json'
print('scale heights in m')
with open(answer_file,'w') as f:
    json.dump(solution_4a_dict,f,indent=4)
    out=json.dumps(solution_4a_dict,indent=4)
    print(out)
```

#### Question 4b, water vapor

2\.  Define a function calc_wv that takes a sounding dataframe and returns the "total precipitable water", which is defined as:

$$W = \int_0^{z_{top}} \rho_v dz $$

Do a change of units to convert $kg\,m^{-2}$ to $cm\,m^{-2}$ using the density of liquid water (1000 $kg\,m^{-3}$) -- that is, turn the kg of water in the 1 square meter column into cubic meters and turn that into $cm/m^{-2}$

Store you answer for each sounding in the following dictionary:

```{code-cell} ipython3
sound_names=list(sound_dict.keys())
dummy_answers=np.ones([len(sound_names)])*np.nan
solution_7b_dict=dict(zip(sound_names,dummy_answers))
print(f"here is the dictionary that will hold  your answers:\n "
       f"{pformat(solution_7b_dict)}")
```

```{code-cell} ipython3
def calc_wv(df):

    """
    Calculate the integrated column water content in mm

    Parameters
    ----------

    df: dataframe with the following columns

    df['rmix']: vector (float)
      vapor mixing ratio in kg/kg

    df['den']: vector (float) of len(df)
      the dry air density in kg/m^3

    df['z']: vector (float) of len(df)
       the height in m

    Returns
    -------

    col_wv: scalar (float)
       the column integrated water vapor in cm/m^2
    """

    rhov = df['rmix'].values*df['den'].values
    mid_rhov = (rhov[1:] + rhov[:-1])/2.
    col_wv = np.sum(mid_rhov*np.diff(df['z'].values))
    #
    # convert kg/m^3 to meters, and meters to cm
    #
    col_wv = col_wv/1000.*100.
    return col_wv

for name,df in sound_dict.items():
    top = 10.e3 #top of atmoshere in meters
    df = df.loc[df['z']<top]
    col_wv = calc_wv(df)
    print(f'{name}: wv = {col_wv:5.2f} cm')
```

```{code-cell} ipython3

```
