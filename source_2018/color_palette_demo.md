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
<div class="toc"><ul class="toc-item"><li><span><a href="#Use-pyresample-to-plot-channel-30-radiances" data-toc-modified-id="Use-pyresample-to-plot-channel-30-radiances-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Use pyresample to plot channel 30 radiances</a></span></li><li><span><a href="#Read-the-lons/lats-from-the-MYD03-file" data-toc-modified-id="Read-the-lons/lats-from-the-MYD03-file-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Read the lons/lats from the MYD03 file</a></span></li><li><span><a href="#get-the-map-projection-from-a301.geometry.get_proj_params" data-toc-modified-id="get-the-map-projection-from-a301.geometry.get_proj_params-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>get the map projection from a301.geometry.get_proj_params</a></span></li><li><span><a href="#Use-pyresample-to-define-a-new-grid-in-this-projection" data-toc-modified-id="Use-pyresample-to-define-a-new-grid-in-this-projection-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Use pyresample to define a new grid in this projection</a></span></li><li><span><a href="#resample-ch30-on-this-grid" data-toc-modified-id="resample-ch30-on-this-grid-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>resample ch30 on this grid</a></span></li><li><span><a href="#replace-missing-values-with-floating-point-nan" data-toc-modified-id="replace-missing-values-with-floating-point-nan-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>replace missing values with floating point nan</a></span></li><li><span><a href="#Plot-the-image-using-cartopy" data-toc-modified-id="Plot-the-image-using-cartopy-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>Plot the image using cartopy</a></span></li></ul></div>

+++

# Use pyresample to plot channel 30 radiances

This notebook uses a MYD03 file and a modis_chans.hdf file to resample the channel 30 radiance
from your granule onto a laea projection.

The two files are copied to new files below called generic_m3 and generic_rad,
so that this notebook works for all granules.

```{code-cell}
import a301
import json
from a301.utils.data_read import download
import a301
import pprint
import shutil
from pyhdf.SD import SD, SDC
import json
import pprint
import cartopy
from pyresample import kd_tree
from a301.scripts.modismeta_read import parseMeta
```

```{code-cell}
def make_projection(proj_params):
    """
    turn a set of proj4 parameters into a cartopy laea projection
    
    Parameters
    ----------
    
    proj_params: dict
       dictionary with parameters lat_0, lon_0 datum and ellps
       
    Returns
    -------
    
    cartopy projection object
    
    """
    import cartopy.crs as ccrs
    globe_w = ccrs.Globe(datum=proj_params["datum"],ellipse=proj_params['ellps'])
    projection_w=ccrs.LambertAzimuthalEqualArea(central_latitude=float(proj_params['lat_0']),
                    central_longitude= float(proj_params['lon_0']),globe=globe_w)
    return projection_w
```

```{code-cell}
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy
from pathlib import Path
import pprint
import numpy as np
import pdb
import shutil
#
```

```{code-cell}
the_file = a301.test_dir / Path('ch30_resample.hdf')
hdf_file = SD(str(the_file), SDC.READ)
ch30_resample = hdf_file.select('ch30_resampled').get()
map_dict = json.loads(hdf_file.proj_json)
hdf_file.end()
proj_params=map_dict['proj_params']
extent = map_dict['extent']
crs = make_projection(proj_params);
```

```{code-cell}
ch30_resample
```

```{code-cell}
from matplotlib import pyplot as plt
pal = plt.get_cmap('plasma')
pal.set_bad('0.75') #75% grey
pal.set_over('r')  #color cells > 0.98 red
pal.set_under('k')  #color cells < 0.75 black
vmin= 0.1
vmax= 7.0
from matplotlib.colors import Normalize
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
plt.hist(ch30_resample.ravel())
```

```{code-cell}
fig, ax = plt.subplots(1, 1, figsize=(10,10),
                          subplot_kw={'projection': crs})
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale='coarse', levels=[1,2,3]));
ax.set_extent(extent,crs)
cs=ax.imshow(ch30_resample, transform=crs, extent=extent, 
             origin='upper',alpha=0.8,cmap=pal,norm=the_norm)
fig.colorbar(cs,extend='both');
```

# Use pyresample to define a new grid in this projection

```{code-cell}
from pyresample import load_area, save_quicklook, SwathDefinition
proj_params = get_proj_params(generic_m3)
swath_def = SwathDefinition(lons, lats)
area_def=swath_def.compute_optimal_bb_area(proj_dict=proj_params)
```

```{code-cell}
area_def
```

# resample ch30 on this grid

```{code-cell}
fill_value=-9999.
area_name = 'modis swath 5min granule'
image_30 = kd_tree.resample_nearest(swath_def, ch30.ravel(),
                                  area_def, radius_of_influence=5000, 
                                      nprocs=2,fill_value=fill_value)
print(f'\ndump area definition:\n{area_def}\n')
print((f'\nx and y pixel dimensions in meters:'
       f'\n{area_def.pixel_size_x}\n{area_def.pixel_size_y}\n'))
```

# replace missing values with floating point nan

```{code-cell}
nan_value = np.array([np.nan],dtype=np.float32)[0]
image_30[image_30< -9000]=nan_value
```

# Plot the image using cartopy

```{code-cell}
pal = plt.get_cmap('plasma')
pal.set_bad('0.75') #75% grey
pal.set_over('r')  #color cells > 0.98 red
pal.set_under('k')  #color cells < 0.75 black
vmin= 0.1
vmax= 7.0
from matplotlib.colors import Normalize
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
```

```{code-cell}
crs = area_def.to_cartopy_crs()
fig, ax = plt.subplots(1, 1, figsize=(10,10),
                          subplot_kw={'projection': crs})
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale='coarse', levels=[1,2,3]));
ax.set_extent(crs.bounds,crs)
cs=ax.imshow(image_30, transform=crs, extent=crs.bounds, 
             origin='upper',alpha=0.8,cmap=pal,norm=the_norm)
fig.colorbar(cs,extend='both');
```

```{code-cell}
out_dict={}
out_dict['proj_params']=crs.proj4_params
out_dict['extent']=crs.bounds
globe=crs.globe.to_proj4_params()
out_dict['globe']=dict(globe)
m3_metadata['lon_list']=list(m3_metadata['lon_list'])
m3_metadata['lat_list']=list(m3_metadata['lat_list'])
out_dict['metadata']=m3_metadata
out_dict['field_name']="ch30"
out_dict['units']="W/m^2/sr/micron"
out_dict['variable_name']="channel 30 radiance"
out_dict['x_size']=area_def.x_size
out_dict['y_size']=area_def.y_size
out_string=json.dumps(out_dict,indent=4)
test=json.loads(out_string)
# Create an HDF file
test_dir = a301.data_dir.parent / Path('test_data')
test_dir.mkdir(parents=True, exist_ok=True)
test_data = test_dir / Path('ch30_resample.hdf')
sdout = SD(str(test_data), SDC.WRITE | SDC.CREATE)
sdout.proj_json=out_string
sdout.history="written with cartopy_resample_ch30.ipynb"
# Create a dataset
sds = sdout.create("ch30_resampled", SDC.FLOAT64, image_30.shape)

# Fill the dataset with a fill value
sds.setfillvalue(-999.)
    
# Assign an attribute to the dataset
sds.units = "W/m^2/micron/sr"

# Write data
sds[:,:] = image_30[:,:]
# Close the dataset
sds.endaccess()
sdout.end()
```

```{code-cell}
def make_projection(proj_params):
    """
    turn a set of proj4 parameters into a cartopy laea projection
    
    Parameters
    ----------
    
    proj_params: dict
       dictionary with parameters lat_0, lon_0 datum and ellps
       
    Returns
    -------
    
    cartopy projection object
    
    """
    import cartopy.crs as ccrs
    globe_w = ccrs.Globe(datum=proj_params["datum"],ellipse=proj_params['ellps'])
    projection_w=ccrs.LambertAzimuthalEqualArea(central_latitude=proj_params['lat_0'],
                    central_longitude= proj_params['lon_0'],globe=globe_w)
    return projection_w
```

```{code-cell}
out_dict
```

```{code-cell}
out_dict['extent']
```

```{code-cell}
out_dict
```

```{code-cell}

```
