---
jupytext:
  formats: ipynb,md:myst,py:percent
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

(assign5asol)=
# Assign 7:

**New material is in Section: Assignment 5a: Answers**

+++

* Setup

1. Download the MYD05 granule that corresponds to your 5 minute date/time.  It should look something like:

         MYD05_L2.A2013222.2105.061.2018048043105.hdf

1. Copy it into the google_drive `a301_data` folder

```{code-cell} ipython3
import json
import pdb
import pprint
from pathlib import Path

import numpy as np
from IPython.display import display
from IPython.display import Image
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from pyhdf.SD import SD
from pyhdf.SD import SDC
from pyproj import CRS, Transformer
from pyresample import SwathDefinition, kd_tree, geometry

import a301_lib
from sat_lib.geometry import get_proj_params
from sat_lib.modismeta_read import parseMeta
## Image('figures/MYBRGB.A2016224.2100.006.2016237025650.jpg',width=600)
import cartopy

```

```{code-cell} ipython3
%matplotlib inline
```

* Read in the 1km and 5km water vapor files

+++

* Start with the lats/lons for 1km and 5km

```{code-cell} ipython3
m5_file= (a301_lib.sat_data / 'hdf4_files').glob("**/MYD05*2105*hdf")
m3_file = (a301_lib.sat_data / 'hdf4_files').glob("MYD03*2105*.hdf")
m5_file_str = str(list(m5_file)[0])
m3_file_str = str(list(m3_file)[0])
print(m5_file_str)
print(m3_file_str)

the_file = SD(m3_file_str, SDC.READ)
lats_1km = the_file.select("Latitude").get()
lons_1km = the_file.select("Longitude").get()
the_file.end()
print(lats_1km.shape)
```

* Get the IR vapor plus 5 of its attributes

Store the data in a numpy array, and the attributes in a dictionary,
using a [dictionary comprehension](https://jakevdp.github.io/WhirlwindTourOfPython/11-list-comprehensions.html)
at line 4

```{code-cell} ipython3
the_file = SD(m5_file_str, SDC.READ)
wv_nearir = the_file.select("Water_Vapor_Near_Infrared")
attrib_list = ["unit", "scale_factor", "add_offset", "valid_range", "_FillValue"]
attr_dict = wv_nearir.attributes()
wv_nearir_attrs = {k: attr_dict[k] for k in attrib_list}
print(f"wv_nearir attributes: {pprint.pformat(wv_nearir_attrs)}")
wv_nearir_data = wv_nearir.get()
the_file.end()
```

```{code-cell} ipython3
bad_data = wv_nearir_data == wv_nearir_attrs["_FillValue"]
wv_nearir_data = wv_nearir_data.astype(np.float32)
wv_nearir_data[bad_data] = np.nan
wv_nearir_scaled = wv_nearir_data * attr_dict["scale_factor"] + attr_dict["add_offset"]
```

* Note that the  scaled wv values are similar between near_ir and ir retrievals

```{code-cell} ipython3
plt.hist(wv_nearir_scaled[~np.isnan(wv_nearir_scaled)])
ax = plt.gca()
ax.set_title("1 km water vapor (cm)")
```

### Map the data

+++

* Resample the 5km IR retrieval onto a laea xy grid

Let swath_def.compute_optimal_bb_area choose the extent and dimensions for
the low resolution (lr) image.  The cell below let's pyresample create the
area_def object, which we will reuse for the 1 km watervapor retrieval to
get both onto the same grid.

The cell below produces:

* `image_wv_ir`  -- resampled 5 km infrared water vapor
* `area_def_lr`  -- area_def used for the resample

+++

* Resample the 1km near-ir water vapor on the same grid

Reuse area_def_lr for the high resolution nearir image so we can compare directly with low resolution ir

The cell below produces:

* `image_wv_nearir_lr`  -- resampled using `area_def_lr`

+++

* now use the 1 km MYD03 lons and lats to get a full resolution xy grid

resample the neair wv onto that grid to show full resolution image.  Call this
area_def area_def_hr

The cell below produces:

* `image_wv_nearir_hr`  -- 1 km near-ir watervapor
* `area_def_hr`  -- the `area_def` file used to do the 1 k resample

### Resample the 1 km near-ir water vapor onto a 1 km grid

```{code-cell} ipython3
proj_params = get_proj_params(m3_file_str)
print(f"{proj_params=}")
swath_def = SwathDefinition(lons_1km, lats_1km)
area_def_hr = swath_def.compute_optimal_bb_area(proj_dict=proj_params)
fill_value = -9999.0
image_wv_nearir_hr = kd_tree.resample_nearest(
    swath_def,
    wv_nearir_scaled.ravel(),
    area_def_hr,
    radius_of_influence=5000,
     nprocs=2,
    fill_value=fill_value
)
image_wv_nearir_hr[image_wv_nearir_hr < -9000] = np.nan
print(area_def_hr.to_cartopy_crs())
proj4_str = area_def_hr.proj_str
```

```{code-cell} ipython3
#https://a301_web.eoas.ubc.ca/week10/image_zoom.html
#https://pyresample.readthedocs.io/en/latest/geo_def.html
#https://pyproj4.github.io/pyproj/stable/api/transformer.html
#area_extent: (lower_left_x, lower_left_y, upper_right_x, upper_right_y)
ll_x,ll_y,ur_x,ur_y =area_def_hr.area_extent
print(f"{(ll_x,ll_y,ur_x,ur_y)=}")
```

```{code-cell} ipython3
p_latlon = CRS.from_proj4("+proj=latlon")
p_crs = CRS.from_proj4(proj4_str)
transform = Transformer.from_crs(p_crs, p_latlon)
ll_lon,ll_lat = transform.transform(ll_x,ll_y)
ur_lon, ur_lat =transform.transform(ur_x,ur_y)
print(f"{(ll_lon,ll_lat,ur_lon,ur_lat)=}")
```

```{code-cell} ipython3
ll_x, ll_y = transform.transform(ll_lon,ll_lat,direction='INVERSE')
print(f"{(ll_x,ll_y)=}")
#help(transform.transform)
```

### Save the mapped images
* Now save these three images plus their area_def's for future plotting

The function area_def_to_dict saves the pyresample area_def as a dict

At line 20 note that
```python
    a=getattr(area_def,key)
```
where key='my_attribute'  is the same as
```python
    a=area_def.my_attribute
```
but you don't have to hard-code in 'my_attribute'

```{code-cell} ipython3
import json


def area_def_to_dict(area_def):
    """
    given an area_def, save it as a dictionary`
    
    Parameters
    ----------
    
    area_def: pyresample area_def object
         
    Returns
    -------
    
    out_dict: dict containing
       area_def dictionary
         
    """
    keys = [
        "area_id",
        "proj_id",
        "name",
        "proj_dict",
        "x_size",
        "y_size",
        "area_extent",
    ]
    area_dict = {key: getattr(area_def, key) for key in keys}
    area_dict["proj_id"] = area_dict["area_id"]
    return area_dict
```

* Create a directory to hold the images and area_def dictionaries

```{code-cell} ipython3
map_dir = Path() / "map_data/wv_maps"
map_dir.mkdir(parents=True, exist_ok=True)
```

* Here's a function that writes the image plus metadata to npz and json files

We'll need to use area_def_to_dict when we create the metadata_dict

```{code-cell} ipython3
def dump_image(image_array, metadata_dict, foldername, image_array_name="image"):
    """
    write an image plus mmetadata to a folder
    
    Parameters
    ----------
    
    image_array: ndarray
        the 2-d image to be saved
    
    foldername:  Path object or string
        the path to the folder that holds the image files
        
    image_array_name:  str
        the root name for the npz and json files
        i.e. image.npz and image.json
        
    Returns: None
       side effect -- an npz and a json file are written
    """
    image_file = Path(foldername) / Path(image_array_name)
    out_dict = {image_array_name: image_array}
    np.savez(image_file, **out_dict)
    json_name = foldername / Path(image_array_name + ".json")
    with open(json_name, "w") as f:
        json.dump(metadata_dict, f, indent=4)
    print(f"\ndumping {image_file}\n and {json_name}\n")
```

### Write out images, putting useful metadeta in metadata_dict

We have three images:  

* `wv_ir` -- 5km ir retrieval
* `wv_nearir_hr`  -- 1 km nearir retrieval
* `wv_nearir_lr`  -- 1 km nearir retrieval resampled to 5 km grid

```{code-cell} ipython3
metadata_dict = dict(modismeta=parseMeta(m5_file_str))
map_dir.mkdir(parents=True, exist_ok=True)
map_dir = Path() / "map_data/wv_maps"

image_name = "wv_ir"
metadata_dict["area_def"] = area_def_to_dict(area_def_lr)
metadata_dict["image_name"] = image_name
metadata_dict["description"] = "modis ir water vapor (cm) sampled at 5 km resolution"
metadata_dict["history"] = "written by level2_cartopy_resample.ipynb"
dump_image(image_wv_ir, metadata_dict, map_dir, image_name)

image_name = "wv_nearir_hr"
metadata_dict["area_def"] = area_def_to_dict(area_def_hr)
metadata_dict["image_name"] = image_name
metadata_dict[
    "description"
] = "modis near ir water vapor (cm) sampled at 1 km resolution"
metadata_dict["history"] = "written by level2_cartopy_resample.ipynb"
dump_image(image_wv_nearir_hr, metadata_dict, map_dir, image_name)


image_name = "wv_nearir_lr"
metadata_dict["area_def"] = area_def_to_dict(area_def_lr)
metadata_dict["image_name"] = image_name
metadata_dict[
    "description"
] = "modis near ir water vapor (cm) sampled at 5 km resolution"
metadata_dict["history"] = "written by level2_cartopy_resample.ipynb"


dump_image(image_wv_nearir_lr, metadata_dict, map_dir, image_name)
```

```{code-cell} ipython3
area_def_lr
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1)
ax.imshow(image_wv_ir)
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1)
ax.imshow(image_wv_ir)
```

```{code-cell} ipython3
area_def_hr
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1)
ax.imshow(image_wv_nearir_lr)
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1)
ax.imshow(image_wv_nearir_hr)
```

## Assignment 5a -- answers

Add cells that do the following:

1) Read your MYD05 and MYD03 files and show your 1km, and 5km IR and 5 km nearir regridded MYD05 water vapor images

2) Regrid your Channel 32/31 brightness temperature map on the MYD05 `area_def_hr` grid.

3) Draw a scatterplot showing the correlation between your 1km and 5km water vapor retrievals

4) Draw a scatterplot showing the correlation between your 1km MYD05 and brightness temperature difference cells

+++

* **Question 1 see images above**

* **Question 2:  reproduce the plot from [Assignment 3](https://a301_web.eoas.ubc.ca/week5/assignment3.html#assign3) below**

+++

a) grab the lats and lons

```{code-cell} ipython3
geom_filelist = list(a301_lib.sat_data.glob("h5_dir/geom*2105*h5"))
geom_file_name = geom_filelist[0]
print(geom_file_name)
with h5py.File(geom_file_name,'r') as f:
    print(list(f.keys()))
    geom_group = f['geometry']
    print(list(geom_group.keys()))
    lats = geom_group['latitude'][...]
    print(lats.shape)
    lons = geom_group['longitude'][...]
    print(lons.shape)
    print(f.attrs.keys())
```

b) grab the radiances

```{code-cell} ipython3
rad_file_name = list(a301_lib.sat_data.glob("h5_dir/oct9*2105*h5"))[0]
with h5py.File(rad_file_name,'r') as f:
    print(list(f.keys()))
    channel_group = f['channels']
    print(list(channel_group.keys()))
    ch31 = channel_group['chan31'][...]
    ch32 = channel_group['chan32'][...]
    print(ch31.shape)
```

c) figure out the middle of the each channel and get the brightness temperature

Tdiff = clean channel - "dirty" channel, where water vapor makes a the channel dirty

https://cimss.ssec.wisc.edu/satellite-blog/archives/23702

```{code-cell} ipython3
chan31_mid = (chan_dict['31']['wavelength_um'][0] + chan_dict['31']['wavelength_um'][1])/2.
chan32_mid = (chan_dict['32']['wavelength_um'][0] + chan_dict['32']['wavelength_um'][1])/2.
print(f"mid-channel wavelengths: {chan31_mid}, {chan32_mid}")
T31 = planck_invert(chan31_mid*1.e-6, ch31*1.e6)
T32 = planck_invert(chan32_mid*1.e-6, ch32*1.e6)

Tdiff = T31 -T32
```

d) Grid Tdiff onto area_def_hr, should get same picture as assignment 3

```{code-cell} ipython3
fill_value = -9999.0
area_name = "modis swath 5min granule"
image_Tdiff = kd_tree.resample_nearest(
    swath_def,
    Tdiff.ravel(),
    area_def_hr,
    radius_of_influence=5000,
    nprocs=2,
    fill_value=fill_value,
)
print(f"\ndump area definition:\n{area_def_hr}\n")
print(
    (
        f"\nx and y pixel dimensions in meters:"
        f"\n{area_def_hr.pixel_size_x}\n{area_def_hr.pixel_size_y}\n"
    )
)
```

e) replaced all the missing values with a 32 bit nan

(we do this by making a 1x1 array using np.array)

```{code-cell} ipython3
nan_value = np.array([np.nan], dtype=np.float32)[0]
image_Tdiff[image_Tdiff < -9000] = nan_value
```

f) Plot on a map

```{code-cell} ipython3
import copy
pal = copy.copy(plt.get_cmap("plasma"))
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("r")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
vmin = 0.
vmax = 4.
from matplotlib.colors import Normalize

the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)

cartopy_crs = area_def_hr.to_cartopy_crs()
fig, ax = plt.subplots(1, 1, figsize=(10,10), subplot_kw={"projection": cartopy_crs})
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="coarse", levels=[1, 2, 3]))
ax.set_extent(cartopy_crs.bounds, cartopy_crs)
cs = ax.imshow(
    image_Tdiff,
    transform=cartopy_crs,
    extent=cartopy_crs.bounds,
    origin="upper",
    alpha=0.8,
    cmap=pal,
    norm=the_norm,
)
fig.colorbar(cs, extend="both");
ax.set_title("Ch 31 - Ch 32 BTD (K) at 1 km resolution")
```

* **Question 3) Scatterplot of near-ir vs. ir water vapor at 5 km resolution**

Here's the map of the high resolution near-ir water vapor at low resolution

```{code-cell} ipython3
import copy
vmin = 0.
vmax = 4.
from matplotlib.colors import Normalize

the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
cartopy_crs = area_def_lr.to_cartopy_crs()
print(f"{cartopy_crs=}")
fig, ax = plt.subplots(1, 1, figsize=(10,10), subplot_kw={"projection": cartopy_crs})
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="coarse", levels=[1, 2, 3]))
ax.set_extent(cartopy_crs.bounds, cartopy_crs)
cs = ax.imshow(
    image_wv_nearir_lr,
    transform=cartopy_crs,
    extent=cartopy_crs.bounds,
    origin="upper",
    alpha=0.8,
    cmap=pal,
    norm=the_norm,
)
fig.colorbar(cs, extend="both")
ax.set_title('near ir precipitable water, 5km resolution (cm/m^2)');
```

And here's the IR water vapor on the same grid -- note that as we saw in the images above, it fails consistently over
the ocean -- because it can't handle situations were the water vapor near the surface
is dominating the water vapor emissions:  https://atmosphere-imager.gsfc.nasa.gov/products/water-vapor
The channel difference technique depends on the water vapor being colder than the surface, and that's
not true over the ocean.

```{code-cell} ipython3
fig, ax = plt.subplots(1, 1, figsize=(10,10), subplot_kw={"projection": cartopy_crs})
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="coarse", levels=[1, 2, 3]))
ax.set_extent(cartopy_crs.bounds, cartopy_crs)
cs = ax.imshow(
    image_wv_ir,
    transform=cartopy_crs,
    extent=cartopy_crs.bounds,
    origin="upper",
    alpha=0.8,
    cmap=pal,
    norm=the_norm,
)
fig.colorbar(cs, extend="both")
ax.set_title('ir precipitable water, 5km resolution (cm/m^2)');
```

* Plot the scatter plot

At least some of the values show approximate 1 to 1 correlation

```{code-cell} ipython3
fig,ax = plt.subplots(1,1,figsize=(10,10))
ax.plot(image_wv_nearir_lr,image_wv_ir,'b.');
ax.set_xlim(0,4)
ax.set_ylim(0,4)
ax.set_xlabel('near ir water vapor (cm/m^2)')
ax.set_ylabel('ir water vapor (cm/m^2)')
ax.set_title('neair vs ir water vapor at 5 km resolution')
```

* Here is the joint histogram version of the scatterplot

```{code-cell} ipython3
import seaborn as sns
sns.jointplot(
    x=image_wv_nearir_lr.flat,
    y=image_wv_ir.flat,
    xlim=(0, 4),
    ylim=(0.0, 4),
    kind="hex",
    color="#4CB391",
);
```

* **Question 4) Scatterplot for near-ir water vapor vs. channel 31-32 BTD**

Not so great -- since we haven't excluded the ocean pixels, we get lots
of pixels with no correlation.  In order to see any kind of pattern, I thin
the data by taking a random sample of 50,000 pixels

```{code-cell} ipython3
import numpy as np
near_ir_flat = image_wv_nearir_hr.flat
Tdiff_flat = image_Tdiff.flat
subset = np.random.randint(0, high=len(near_ir_flat), size=50000, dtype='l')
```

```{code-cell} ipython3
fig,ax = plt.subplots(1,1,figsize=(10,10))
ax.plot(near_ir_flat[subset],Tdiff_flat[subset],'b.');
ax.set_xlim(0,4)
ax.set_ylim(0,4)
ax.set_xlabel('level 2 water vapor 1 km')
ax.set_ylabel('ch31 - ch32 BTD 1 km')
ax.set_title('near ir vs. BTD at 1 km resolution')
```

*  Here is the joint distribution plot

```{code-cell} ipython3
import seaborn as sns
sns.jointplot(
    x=near_ir_flat[subset],
    y=Tdiff_flat[subset],
    xlim=(0, 3),
    ylim=(0.0, 3),
    kind="hex",
    color="#4CB391",
);
```

## Appendix -- try resampling the BTD to 5 km

```{code-cell} ipython3
fill_value = -9999.0
area_name = "modis swath 5min granule"
image_Tdiff_lr = kd_tree.resample_nearest(
    swath_def,
    Tdiff.ravel(),
    area_def_lr,
    radius_of_influence=5000,
    nprocs=2,
    fill_value=fill_value,
)
print(f"\ndump area definition:\n{area_def_lr}\n")
print(
    (
        f"\nx and y pixel dimensions in meters:"
        f"\n{area_def_lr.pixel_size_x}\n{area_def_lr.pixel_size_y}\n"
    )
)
```

We'll also remove all pixels that are set to NaN in the IR water vapor image.  Once the
ocean pixels are taken out, the comparison looks a little better

```{code-cell} ipython3
good_pixels = ~np.isnan(image_wv_ir)
fig,ax = plt.subplots(1,1,figsize=(10,10))
ax.plot(image_wv_nearir_lr[good_pixels],image_Tdiff_lr[good_pixels],'b.');
ax.set_xlim(0,4)
ax.set_ylim(0,4)
ax.set_xlabel('level 2 water vapor 5 km')
ax.set_ylabel('ch31 - ch32 BTD 5 km')
ax.set_title('nearir vs BTD at 5 km resolution, land only')
```

```{code-cell} ipython3
import seaborn as sns
sns.jointplot(
    x=image_wv_nearir_lr[good_pixels],
    y=image_Tdiff_lr[good_pixels],
    xlim=(0, 3),
    ylim=(0.0, 3),
    kind="hex",
    color="#4CB391",
);
```
