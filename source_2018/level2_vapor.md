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
<div class="toc"><ul class="toc-item"><li><span><a href="#Working-with-level-2-water-vapor-data" data-toc-modified-id="Working-with-level-2-water-vapor-data-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Working with level 2 water vapor data</a></span><ul class="toc-item"><li><span><a href="#Assignment-10" data-toc-modified-id="Assignment-10-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Assignment 10</a></span></li></ul></li></ul></div>

```{code-cell}
from IPython.display import Image
Image('figures/MYBRGB.A2016224.2100.006.2016237025650.jpg',width=600)
```

## Working with level 2 water vapor data

We have been using MYD021KM and MYD02QKM data, which are the calibrated and geolocated radiances at 1 km and 250 meter resolution for a 5 minute swath of MODIS data on the Aqua satellite.  The next step up in processing is level 2 data, where the radiances are turned into physical paramters like preciptable water or surface temperature.

The level 2 water vapor retrievals from MODIS are indicated by filenames that start with MYD05_L2.  I have downloaded the MYD05_L2 file for our Vancouver granuale (false color above) that we looked at in the satellite_ndvi notebook.  Water vapor is retrieved on 5 km x 5 km pixels using two separate water vapor absorption bands in the infrared (11 microns) and near-infrared (0.8 microns).  You should use HDFview to convince yourself that the code below reads and scales the two different retrieval fields from this file to column water vapor measurements in cm of precipitable water.

```{code-cell}
from a301utils.a301_readfile import download
from a301lib.geolocate import fast_hist, fast_avg
from matplotlib import cm
import h5py
import numpy as np
from matplotlib import pyplot as plt
wv_filename = 'MYD05_L2.A2016224.2100.006.2016237021914.h5'
download(wv_filename)
```

```{code-cell}
wv_file = h5py.File(wv_filename)
lon_data=wv_file['mod05']['Geolocation Fields']['Longitude'][...]
lat_data=wv_file['mod05']['Geolocation Fields']['Latitude'][...]
wv_ir=wv_file['mod05']['Data Fields']['Water_Vapor_Infrared'][...]
wv_nearir = wv_file['mod05']['Data Fields']['Water_Vapor_Near_Infrared'][...]
scale = wv_file['mod05']['Data Fields']['Water_Vapor_Infrared'].attrs['scale_factor']
wv_ir = wv_ir*scale
scale=wv_file['mod05']['Data Fields']['Water_Vapor_Near_Infrared'].attrs['scale_factor']
wv_nearir = wv_nearir*scale
```

```{code-cell}

```

### Assignment 10

1) Borrowing code from the satellite_ndvi notebook, grid these two fields at a suitable lat/lon resolution and plot them using the corner lat/lon values from satellite_ndvi with  basemap.  Your result should be two plots, one for IR and one for nearIR, with colorbars, titles and labels.  The colorbars should be normalized so that both retrievals show colors over the same range of data.  Use masked arrays to show the missing values as gray, as in satellite_ndvi.

Result -- two pcolormesh plots (IR and nearIR water vapor) using basemap's lcc projection, same corners as satellite_ndvi

2) Subtract IR - nearIR and make a gridded navigated plot of the difference between the two measurements with colorbar labels and titles

Result -- one pcolormesh plot using basemap's lcc projection

3) plot a histogram of the difference  diff = IR - nearIR  -- to get valid values to histogram from the masked array
   use  the compressed method on the diff masked array:   good_vals = diff.compressed()
   
Result -- one histogram plot with title and labels

```{code-cell}

```

```{code-cell}

```
