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
<div class="toc"><ul class="toc-item"><li><ul class="toc-item"><li><span><a href="#Solution:-Working-with-level-2-water-vapor-data" data-toc-modified-id="Solution:-Working-with-level-2-water-vapor-data-0.1"><span class="toc-item-num">0.1&nbsp;&nbsp;</span>Solution: Working with level 2 water vapor data</a></span></li></ul></li><li><span><a href="#Read-in-the-1km-and-5km-water-vapor-files" data-toc-modified-id="Read-in-the-1km-and-5km-water-vapor-files-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Read in the 1km and 5km water vapor files</a></span><ul class="toc-item"><li><ul class="toc-item"><li><span><a href="#Resample-the-5km-IR-retrieval-onto-a-laea-xy-grid" data-toc-modified-id="Resample-the-5km-IR-retrieval-onto-a-laea-xy-grid-1.0.1"><span class="toc-item-num">1.0.1&nbsp;&nbsp;</span>Resample the 5km IR retrieval onto a laea xy grid</a></span></li><li><span><a href="#Resample-the-1km-near-ir-water-vapor-on-the-same-grid" data-toc-modified-id="Resample-the-1km-near-ir-water-vapor-on-the-same-grid-1.0.2"><span class="toc-item-num">1.0.2&nbsp;&nbsp;</span>Resample the 1km near-ir water vapor on the same grid</a></span></li></ul></li><li><span><a href="#Now-save-these-two-images-plus-the-area_def-for-future-plotting" data-toc-modified-id="Now-save-these-two-images-plus-the-area_def-for-future-plotting-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Now save these two images plus the area_def for future plotting</a></span></li></ul></li></ul></div>

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

# Read in the 1km and 5km water vapor files

```{code-cell}
# %load temp.md
# %load temp.md
# %load temp.md
# %load temp.md
m5_file = a301.data_dir / Path('myd05_l2_10_7.hdf')
m3_file = a301.data_dir / Path('m3_file_2018_10_1.hdf')
m2_file = a301.data_dir / Path('m2_file_2018_10_1.hdf')

the_file = SD(str(m3_file), SDC.READ)
lats_1km = the_file.select('Latitude').get()
lons_1km = the_file.select('Longitude').get()
the_file.end()

the_file = SD(str(m5_file), SDC.READ)
lats_5km = the_file.select('Latitude').get()
lons_5km = the_file.select('Longitude').get()

wv_ir = the_file.select('Water_Vapor_Infrared')
attributes=['units', 'scale_factor', 'add_offset', 'valid_range', '_FillValue']
attr_dict=wv_ir.attributes()
wv_ir_attrs={k: attr_dict[k] for k in attributes}
print(f'wv_ir attributes: {pprint.pformat(wv_ir_attrs)}')
wv_ir_data = wv_ir.get()

bad_data = wv_ir_data == wv_ir_attrs['_FillValue']
wv_ir_data = wv_ir_data.astype(np.float32)
wv_ir_data[bad_data]=np.nan
wv_ir_scaled = wv_ir_data*attr_dict['scale_factor'] + attr_dict['add_offset']
wv_ir_good_data = wv_ir_scaled[np.logical_not(bad_data)]

wv_nearir = the_file.select('Water_Vapor_Near_Infrared')
attrib_list=['unit', 'scale_factor', 'add_offset', 'valid_range', '_FillValue']
attr_dict=wv_nearir.attributes()
wv_nearir_attrs={k: attr_dict[k] for k in attrib_list}
print(f'wv_nearir attributes: {pprint.pformat(wv_nearir_attrs)}')
wv_nearir_data = wv_nearir.get()
the_file.end()

bad_data = wv_nearir_data == wv_nearir_attrs['_FillValue']
wv_nearir_data = wv_nearir_data.astype(np.float32)
wv_nearir_data[bad_data]=np.nan
wv_nearir_scaled = wv_nearir_data*attr_dict['scale_factor'] + attr_dict['add_offset']
wv_nearir_good_data = wv_nearir_scaled[np.logical_not(bad_data)]

plt.hist(wv_nearir_good_data.flat);
ax=plt.gca()
ax.set_title('1 km water vapor');
```

```{code-cell}
plt.hist(wv_ir_good_data.flat);
ax=plt.gca()
ax.set_title('5 km wv data');
```

### Resample the 5km IR retrieval onto a laea xy grid

```{code-cell}
# %load temp.md
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
```

### Resample the 1km near-ir water vapor on the same grid

```{code-cell}
swath_def = SwathDefinition(lons_1km, lats_1km)
fill_value=-9999.
image_wv_nearir_lr = kd_tree.resample_nearest(swath_def, wv_nearir_scaled.ravel(),
                                  area_def_lr, radius_of_influence=5000, 
                                      nprocs=2,fill_value=fill_value)
image_wv_nearir_lr[image_wv_nearir_lr < -9000]=np.nan
```

```{code-cell}
### Resample the 1 km near-ir water vapor onto a 1 km grid

proj_params = get_proj_params(m3_file)
swath_def = SwathDefinition(lons_1km, lats_1km)
area_def_hr=swath_def.compute_optimal_bb_area(proj_dict=proj_params)
area_def_hr.name="near ir wv retrieval modis 1 km resolution (hr=high resolution)"
area_def_hr.area_id="wv_nearir_hr"
area_def_hr.job_id = area_def_hr.area_id
fill_value=-9999.
image_wv_nearir_hr = kd_tree.resample_nearest(swath_def, wv_nearir_scaled.ravel(),
                                  area_def_hr, radius_of_influence=5000, 
                                      nprocs=2,fill_value=fill_value)
image_wv_nearir_hr[image_wv_nearir_hr < -9000]=np.nan
```

## Now save these two images plus the area_def for future plotting

```{code-cell}
import json
from pyresample import  SwathDefinition, kd_tree, geometry

def dump_area_def(area_def):
    """
    given an area_def, save it as a dictionary
    
    Parameters
    ----------
    
    area_def: pyresample area_def object
         
    Returns
    -------
    
    out_dict: dict containing
       area_def dictionary
         
    """
    keys=['area_id','proj_id','name','proj_dict','x_size','y_size','area_extent']
    area_dict={key:getattr(area_def,key) for key in keys}
    area_dict['proj_id']=area_dict['area_id']
    return area_dict
        
def area_def_from_dict(area_def_dict):
    """
    given an dictionary by dump_area_def
    return a pyresample area_def
    
    Parameters
    ----------
    
    area_def_dict: dict
        dictionary containing area_def parameters
        
    Returns
    -------
    
    pyresample area_def object

    """
    with open(filename,'r') as f:
        area_dict=json.load(f)
        area_dict=input_dict['area_dict']
    area_dict['proj_id']=area_dict['area_id']
    keys=['area_id','proj_id','name','proj_dict','x_size','y_size','area_extent']    
    arglist=[area_dict[key] for key in keys]
    area_def=geometry.AreaDefinition(*arglist)
    return area_def
```

```{code-cell}
import pdb
def dump_image(image_array,metadata_dict,foldername,
              image_array_name='image'):
    image_file=Path(foldername) / Path(image_array_name)
    np.savez(image_file,
               image_array_name=image_array)
    json_name = foldername / Path(image_array_name + '.json')
    with open(json_name,'w') as f:
        json.dump(metadata_dict,f,indent=4)

image_name='wv_nearir_lr'
metadata_dict=dict(modismeta = parseMeta(m5_file))
metadata_dict['area_def']=dump_area_def(area_def_lr)
metadata_dict['image_name']=image_name
metadata_dict['description']='modis near ir water vapor (cm) sampled at 5 km resolution'
map_dir = a301.data_dir.parent / Path('map_data/wv_maps')
map_dir.mkdir(parents=True, exist_ok=True)
dump_image(image_wv_nearir_lr,metadata_dict,map_dir,image_name)

image_name='wv_nearir_hr'
metadata_dict=dict(modismeta = parseMeta(m5_file))
metadata_dict['area_def']=dump_area_def(area_def_hr)
metadata_dict['image_name']=image_name
metadata_dict['description']='modis near ir water vapor (cm) sampled at 1 km resolution'
map_dir = a301.data_dir.parent / Path('map_data/wv_maps')
map_dir.mkdir(parents=True, exist_ok=True)
dump_image(image_wv_nearir_lr,metadata_dict,map_dir,image_name)

image_name='wv_ir'
metadata_dict=dict(modismeta = parseMeta(m5_file))
metadata_dict['area_def']=dump_area_def(area_def_lr)
metadata_dict['image_name']=image_name
metadata_dict['description']='modis ir water vapor (cm) sampled at 5 km resolution'
map_dir = a301.data_dir.parent / Path('map_data/wv_maps')
map_dir.mkdir(parents=True, exist_ok=True)
dump_image(image_wv_nearir_lr,metadata_dict,map_dir,image_name)




```

```{code-cell}
map_dir = a301.data_dir.parent / Path('map_data/wv_maps')
map_dir.mkdir(parents=True, exist_ok=True)
```

```{code-cell}

```

```{code-cell}
import cartopy
def plot_image(resampled_image,area_def,vmin=0.,vmax=4.,palette='plasma'):
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
fig,ax=plot_image(image_wv_ir, area_def_lr)
ax.set_title('5 km IR water vapor (cm)');
```

```{code-cell}
fig,ax=plot_image(image_wv_nearir_lr, area_def_lr)
ax.set_title('1 km IR water vapor (cm)');
print(image_wv_nearir_lr.shape)
```

```{code-cell}
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
