---
jupytext:
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
<div class="toc"><ul class="toc-item"><li><span><a href="#Solution:-Working-with-level-2-water-vapor-data" data-toc-modified-id="Solution:-Working-with-level-2-water-vapor-data-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Solution: Working with level 2 water vapor data</a></span></li></ul></div>

+++

## Solution: Working with level 2 water vapor data

We have been using MYD021KM and MYD02QKM data, which are the calibrated and geolocated radiances at 1 km and 250 meter resolution for a 5 minute swath of MODIS data on the Aqua satellite.  The next step up in processing is level 2 data, where the radiances are turned into physical paramters like preciptable water or surface temperature.

The level 2 water vapor retrievals from MODIS are indicated by filenames that start with MYD05_L2.  I have downloaded the MYD05_L2 file for our Vancouver granuale.  Water vapor is retrieved on 5 km x 5 km pixels using two separate water vapor absorption bands in the infrared (11 microns) and near-infrared (0.8 microns).  You should use HDFview to convince yourself that the code below reads and scales the two different retrieval fields from this file.

```{code-cell}
from matplotlib import cm

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from IPython.display import Image,display

wv_filename = 'MYD05_L2.A2016224.2100.006.2016237021914.h5'
download(wv_filename)
Image('figures/MYBRGB.A2016224.2100.006.2016237025650.jpg',width=600)
```

```{code-cell}
wv_filename = 'MYD05_L2.A2016224.2100.006.2016237021914.h5'
wv_file = h5py.File(wv_filename)
print(wv_file)
lon_data=wv_file['mod05']['Geolocation Fields']['Longitude'][...]
lat_data=wv_file['mod05']['Geolocation Fields']['Latitude'][...]
wv_ir=wv_file['mod05']['Data Fields']['Water_Vapor_Infrared'][...]
wv_nearir = wv_file['mod05']['Data Fields']['Water_Vapor_Near_Infrared'][...]
scale = wv_file['mod05']['Data Fields']['Water_Vapor_Infrared'].attrs['scale_factor']
wv_ir = wv_ir*scale
scale=wv_file['mod05']['Data Fields']['Water_Vapor_Near_Infrared'].attrs['scale_factor']
wv_nearir = wv_nearir*scale
corners=find_corners(lat_data,lon_data)

lon_min= -140
lon_max = -105

lat_min = 35
lat_max = 55
binsize = 0.25



lon_hist = fast_hist(lon_data.ravel(),lon_min,lon_max,binsize=binsize)
lat_hist =  fast_hist(lat_data.ravel(),lat_min,lat_max,binsize=binsize)
gridded_ir = fast_avg(lat_hist,lon_hist,wv_ir.ravel())
gridded_nearir = fast_avg(lat_hist,lon_hist,wv_nearir.ravel())

%matplotlib inline
                       
#_=plt.hist(wv_ir.ravel())
fig,(ax1,ax2)=plt.subplots(2,1,figsize=(14,10))

def set_plot(ax,masked_field,lat_hist,lon_hist,the_norm=None,cmap=None):
    corners['ax'] = ax
    corners['resolution']='l'
    corners['projection']='lcc'
    corners['urcrnrlon'] = -90
    corners['urcrnrlat'] = 55.
    corners['llcrnrlat'] = 35.
    corners['llcrnrlon'] = -140.
    proj = make_plot(corners)
    lat_centers = lat_hist['centers_vec']
    lon_centers = lon_hist['centers_vec']
    lon_array,lat_array=np.meshgrid(lon_centers,lat_centers)
    #
    #
    # translate every lat,lon pair in the scene to x,y plotting coordinates 
    # for th Lambert projection
    #
    x,y=proj(lon_array,lat_array)
    CS=proj.pcolormesh(x, y,masked_field, cmap=cmap, norm=the_norm)
    CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
    CBar.set_label('Column water vapor (cm)',
               rotation=270,verticalalignment='bottom',size=10)
    return None

cmap=cm.YlGnBu
cmap.set_over('cyan')
cmap.set_under('w',alpha=0.1)
cmap.set_bad('0.75') #75% grey
#
# use all my colors on data between 7 and 10 
#
vmin= 0
vmax= 2
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)  
masked_ir = np.ma.masked_invalid(gridded_ir)
set_plot(ax1,masked_ir,lat_hist,lon_hist,
         the_norm=the_norm,cmap=cmap)
ax1.set_title('Modis IR Column Water Vapor, Vancouver August 11, 2016',size=12)
         

masked_nearir = np.ma.masked_invalid(gridded_nearir)
set_plot(ax2,masked_nearir,lat_hist,lon_hist,
          the_norm=the_norm,cmap=cmap)
_=ax2.set_title('Modis near IR Column Water Vapor, Vancouver August 11, 2016',size=12)

```

```{code-cell}
masked_diff = masked_ir - masked_nearir
fig, ax = plt.subplots(1,1, figsize=(10,8))
set_plot(ax,masked_diff,lat_hist,lon_hist,
          the_norm=the_norm,cmap=cmap)
fig.axes[1].set_ylabel('IR - nearIR (cm)')
_=ax.set(title='Column WV Retrieval difference: IR - nearIR (cm)')
```

```{code-cell}
fig,ax = plt.subplots(1,1,figsize=(8,6))
ax.hist(masked_diff.compressed())
_=ax.set(title='difference IR - nearIR retreivals (cm)',
        ylabel='pixel counts',xlabel='column water vapor difference (cm)')
```

```{code-cell}

```
