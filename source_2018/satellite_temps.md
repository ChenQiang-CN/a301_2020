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
<div class="toc"><ul class="toc-item"><li><span><a href="#Repeat-the-raw-image-plot-from-satellite_III" data-toc-modified-id="Repeat-the-raw-image-plot-from-satellite_III-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Repeat the raw image plot from satellite_III</a></span><ul class="toc-item"><li><ul class="toc-item"><li><span><a href="#Read-the-radiance-data-from-MODIS_SWATH_Type_L1B/Data-Fields/EV_1KM_Emissive" data-toc-modified-id="Read-the-radiance-data-from-MODIS_SWATH_Type_L1B/Data-Fields/EV_1KM_Emissive-1.0.1"><span class="toc-item-num">1.0.1&nbsp;&nbsp;</span><strong>Read the radiance data from MODIS_SWATH_Type_L1B/Data Fields/EV_1KM_Emissive</strong></a></span></li><li><span><a href="#The-corners-dictionary-will-be-used-by-basemap-below.--For-now-we-can-use-the-corner-positions-and-the-pixel-spacing-to-get-histogram-limits:" data-toc-modified-id="The-corners-dictionary-will-be-used-by-basemap-below.--For-now-we-can-use-the-corner-positions-and-the-pixel-spacing-to-get-histogram-limits:-1.0.2"><span class="toc-item-num">1.0.2&nbsp;&nbsp;</span>The corners dictionary will be used by basemap below.  For now we can use the corner positions and the pixel spacing to get histogram limits:</a></span></li></ul></li></ul></li></ul></div>

+++

# Repeat the raw image plot from satellite_III

```{code-cell}
from a301utils.a301_readfile import download
import numpy as np
import h5py
import sys
import a301lib
from a301lib.geolocate import fast_hist, slow_hist, fast_avg, slow_avg,make_plot 
from a301lib.radiation import planckInvert

filename = 'MYD021KM.A2016136.2015.006.2016138123353.h5'
download(filename)
```

Here is the corresponding red,green,blue color composite for the granule.

```{code-cell}
from IPython.display import Image
Image(url='http://clouds.eos.ubc.ca/~phil/courses/atsc301/downloads/aqua_136_2015.jpg',width=600)
```

```{code-cell}
h5_file=h5py.File(filename)
```

### **Read the radiance data from MODIS_SWATH_Type_L1B/Data Fields/EV_1KM_Emissive**

According to the [Modis channel listing](https://modis.gsfc.nasa.gov/about/specifications.php)
channel 31 is centered at 11 microns.  The Band_1KM_Emissive band listing says that this is index 10 of the the Emissive data array.  Note that Channel 26 is missing:

```{code-cell}
index31=10

my_name = 'EV_1KM_Emissive'
chan31=h5_file['MODIS_SWATH_Type_L1B']['Data Fields'][my_name][index31,:,:]
scale=h5_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][...]
offset=h5_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][...]
chan31_calibrated =(chan31 - offset[index31])*scale[index31]
```

Now call the planckInvert function imported at the top of the notebook to convert radiance to brightness temperature

```{code-cell}
wavel=11.e-6  #chan 31 central wavelength, meters
chan31_mks = chan31_calibrated*1.e6  #W/m^2/m/sr
Tbright = planckInvert(wavel,chan31_mks)
Tbright = Tbright - 273.15 #convert to Centigrade
```

```{code-cell}
%matplotlib inline
from matplotlib import pyplot as plt
```

```{code-cell}
fig,ax = plt.subplots(1,1,figsize = (10,14))
CS=ax.imshow(Tbright)
cax=fig.colorbar(CS)
ax.set_title('Brightness temperatures, Ft. McMurray')
out=cax.ax.set_ylabel('Chan 31 brightness temperature (deg C)$)')
out.set_rotation(270)
out.set_verticalalignment('bottom')
```

```{code-cell}
filename='MYD03.A2016136.2015.006.2016138121537.h5'
download(filename)
geo_file = h5py.File(filename)
lon_data=geo_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Longitude'][...]
lat_data=geo_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Latitude'][...]
```

```{code-cell}
from importlib import reload
import a301lib.geolocate
reload(a301lib.geolocate)
from a301lib.geolocate import find_corners
corners=find_corners(lat_data,lon_data)
corners
```

### The corners dictionary will be used by basemap below.  For now we can use the corner positions and the pixel spacing to get histogram limits:

Note that [fast_hist](http://clouds.eos.ubc.ca/~phil/courses/atsc301/_modules/a301lib/geolocate.html#fast_hist) now takes either a numbins or a binsize keyword argument to make the histogram bins.

```{code-cell}
lon_min= -144
lon_max = -92

lat_min = 47
lat_max = 70
binsize = 0.1

lon_hist = fast_hist(lon_data.ravel(),lon_min,lon_max,binsize=binsize)
lat_hist =  fast_hist(lat_data.ravel(),lat_min,lat_max,binsize=binsize)
gridded_image = fast_avg(lat_hist,lon_hist,Tbright.ravel())
```

```{code-cell}
out=np.meshgrid([-1,-2,-3], [1.,2.,3.,4.,5.])
type(out)
len(out)
out[0]
out[1]
```

```{code-cell}
lat_centers=(lat_hist['edges_vec'][1:] + lat_hist['edges_vec'][:-1])/2.
lon_centers=(lon_hist['edges_vec'][1:] + lon_hist['edges_vec'][:-1])/2.
lon_array,lat_array=np.meshgrid(lon_centers,lat_centers)
print(lon_array.shape)
masked_temps = np.ma.masked_invalid(gridded_image)
```

```{code-cell}
from matplotlib import cm
from matplotlib.colors import Normalize

cmap=cm.autumn  #see http://wiki.scipy.org/Cookbook/Matplotlib/Show_colormaps
cmap.set_over('w')
cmap.set_under('b',alpha=0.1)
cmap.set_bad('0.75') #75% grey
#
# set the range over which the pallette extends so I use
# use all my colors on data 10 and 40 degrees centigrade
#
vmin= 10
vmax= 40
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
fig,ax = plt.subplots(1,1,figsize=(14,18))
corners['ax'] = ax
corners['resolution']='l'
corners['projection']='lcc'
corners['urcrnrlon'] = -70.
corners['urcrnrlat'] = 65.
corners['llcrnrlat'] = 46.
corners['llcrnrlon'] = -140.
proj = make_plot(corners)
lat_centers=(lat_hist['edges_vec'][1:] + lat_hist['edges_vec'][:-1])/2.
lon_centers=(lon_hist['edges_vec'][1:] + lon_hist['edges_vec'][:-1])/2.
lon_array,lat_array=np.meshgrid(lon_centers,lat_centers)
#
# translate every lat,lon pair in the scene to x,y plotting coordinates 
# for th Lambert projection
#
x,y=proj(lon_array,lat_array)
CS=proj.pcolormesh(x, y,masked_temps, cmap=cmap, norm=the_norm)
CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
CBar.set_label('Channel 31 brightness temps (deg C))',
               rotation=270,verticalalignment='bottom',size=18)
_=ax.set_title('Modis Channel 11, May 15, 2016 -- Fort McMurray',size=22)
```

```{code-cell}

```
