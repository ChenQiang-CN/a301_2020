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
<div class="toc"><ul class="toc-item"><li><span><a href="#Introduction" data-toc-modified-id="Introduction-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Introduction</a></span></li><li><span><a href="#Setup" data-toc-modified-id="Setup-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Setup</a></span></li><li><span><a href="#Read-in-the-1km-and-5km-water-vapor-images" data-toc-modified-id="Read-in-the-1km-and-5km-water-vapor-images-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Read in the 1km and 5km water vapor images</a></span></li></ul></div>

+++

# Introduction

This notebook reads the files produced by level2_cartopy_resample and plots
them on a map.

It introduces a new functions to read the image and the area_def, and to get
the readiance from a MYD02 file.

# Setup

1. Run level2_cartopy_resample

1. Copy the MYD021KM corresponding to your MYD03 file to a301.data_dir, and rename it to:
```
      myd02_2018_10_10.hdf
```      
1. Run the following test script
```
      python -m a301.install_tests.assign9_test
```
to check file locations.    

```{code-cell}
from matplotlib import cm

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from IPython.display import Image,display
from pyresample import geometry
import pdb

#Image('figures/MYBRGB.A2016224.2100.006.2016237025650.jpg',width=600)
```

```{code-cell}
%matplotlib inline
from matplotlib import cm

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from IPython.display import Image,display
import a301
from a301.geometry import (make_projection, get_proj_params)
from a301.scripts.modismeta_read import parseMeta
from pathlib import Path
from pyhdf.SD import SD, SDC
import pprint
import json
```

# Read in the 1km and 5km water vapor images

Use the two helper functions below to get the area_def and image

```{code-cell}
def area_def_from_dict(area_def_dict):
    """
    given an dictionary produced by dump_area_def
    return a pyresample area_def
    
    Parameters
    ----------
    
    area_def_dict: dict
        dictionary containing area_def parameters
        
    Returns
    -------
    
    pyresample area_def object

    """
    keys=['area_id','proj_id','name','proj_dict','x_size','y_size','area_extent']    
    arglist=[area_def_dict[key] for key in keys]
    area_def=geometry.AreaDefinition(*arglist)
    return area_def

def get_image(foldername,image_array_name):
    """
    write an image plus mmetadata to a folder under a301.map_dir
    
    Parameters
    ----------

    foldername:  Path object or string
        the path to the folder that holds the image files
        
    image_array_name:  str
        the root name for the npz and json files
        i.e. image.npz and image.json
        
    Returns: 
    
    image_array: ndarray with the image
    
    area_def:  pyresample area_def for image

    """
    image_file=Path(foldername) / Path(image_array_name + '.npz')
    image_array = np.load(image_file)[image_array_name]
    json_file = foldername / Path(image_array_name + '.json')
    with open(json_file,'r') as f:
        meta_dict=json.load(f)
    area_def = area_def_from_dict(meta_dict['area_def'])
    return image_array, area_def
```

```{code-cell}
import cartopy
def plot_image(resampled_image,area_def,vmin=0.,vmax=4.,palette='plasma'):
    """
    Make a cartopy plot of an image 
    
    Parameters
    ----------
    
    resampled_image: ndarray
       2-dimensional image that has be resampled onto an xy grid
       
    area_def:  pyresample area_def objet
       the area_def that was used by pyresample
       
    vmin,vmax:  floats
        upper and lower limits for the color map
        
    palette: str or matplotlib colormap
        colormap to use for plot
        
    Returns
    -------
    
    fig,ax: matmplotlib figure and axis objects
    """
    if isinstance(palette,str):
        pal = plt.get_cmap(palette)
    else:
        pal = palette
    pal.set_bad('0.75') #75% grey for out-of-map cells
    pal.set_over('r')  #color cells > vmax red
    pal.set_under('k')  #color cells < vmin black
    
    from matplotlib.colors import Normalize
    the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
    crs = area_def.to_cartopy_crs()
    fig, ax = plt.subplots(1, 1, figsize=(10,10),
                              subplot_kw={'projection': crs})
    ax.gridlines(linewidth=2)
    ax.add_feature(cartopy.feature.GSHHSFeature(scale='coarse', levels=[1,2,3]));
    ax.set_extent(crs.bounds,crs)
    cs=ax.imshow(resampled_image, transform=crs, extent=crs.bounds, 
                 origin='upper',alpha=0.8,cmap=pal,norm=the_norm)
    fig.colorbar(cs,extend='both')
    return fig, ax
```

```{code-cell}
foldername=a301.map_dir / Path('wv_maps')
image_wv_ir, area_def_lr = get_image(foldername, 'wv_ir')
```

```{code-cell}
fig,ax=plot_image(image_wv_ir, area_def_lr)
ax.set_title('5 km IR water vapor (cm)');
```

```{code-cell}
image_wv_nearir_lr, area_def_hr = get_image(foldername, 'wv_nearir_lr')
fig,ax=plot_image(image_wv_nearir_lr, area_def_hr)
ax.set_title('1 km IR water vapor (cm) at 5k low resolution (lr)');
print(image_wv_nearir_lr.shape)
```

```{code-cell}
image_wv_nearir_hr, area_def_hr = get_image(foldername, 'wv_nearir_hr')
fig,ax=plot_image(image_wv_nearir_hr, area_def_hr)
ax.set_title('1 km IR water vapor high resolution (cm)');
print(image_wv_nearir_hr.shape)
```

```{code-cell}
difference = (image_wv_nearir_lr - image_wv_ir)
pal = plt.get_cmap('RdYlBu').reversed()
fig,ax=plot_image(difference, area_def_lr,vmin=-1,vmax=+1,palette=pal)
ax.set_title('1km - 5km wv (cm)');
```

```{code-cell}
def get_index(band_nums,chan_num):
    """
    given the longwave_bands vector from the level1b file, 
    find the index of the channel chan_num in the dataset
    
    Parameters
    ----------
    
    band_nums: numpy float vector
       list of channel numbers
       
    chan_num: float or int
       channel number to get index for
       
    Returns
    -------
    
    the_index: int
        index of channel in modis image

    """
    ch_index=np.searchsorted(band_nums,chan_num)
    return int(ch_index)

from pyhdf.SD import SD, SDC
from a301.radiation import planck_invert
modis_file = a301.data_dir / Path("myd02_2018_10_10.hdf")

def get_modis_lw_radiance(m2_file,chan_num):
    """
    given a modis MYD02 file path and and a band number 
    from https://modis.gsfc.nasa.gov/about/specifications.php
    get the scaled radiance
    
    Parameters:
    
    m2_file: Path or str 
       path to MYD02 file
    
    chan_num: int
       channel/band number to extract
    """
    the_file = SD(str(m2_file), SDC.READ)    
    longwave_data = the_file.select('EV_1KM_Emissive') # 
    longwave_bands = the_file.select('Band_1KM_Emissive')
    band_nums=longwave_bands.get()
    band_index=get_index(band_nums,chan_num)
    band_data = longwave_data[band_index,:,:]
    scales=longwave_data.attributes()['radiance_scales']
    offsets=longwave_data.attributes()['radiance_offsets']
    band_scale=scales[band_index]
    band_offset=offsets[band_index]
    band_calibrated =(band_data - band_offset)*band_scale
    return band_calibrated

ch31=get_radiance(modis_file,31)
wavel_31=1.e-6*(10.780 + 11.280)/2.
#
# convert from W/m^2/microns/sr to W/m^2/m/sr
#
Tbright31=planck_invert(wavel_31,ch31*1.e6)
plt.hist(Tbright31.ravel());
```

```{code-cell}
image_wv_nearir_hr, area_def_hr = get_image(foldername, 'wv_nearir_hr')
fig,ax=plot_image(image_wv_nearir_hr, area_def_hr)
ax.set_title('1 km IR water vapor high resolution (cm)');
print(image_wv_nearir_hr.shape)
```
