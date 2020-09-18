---
jupytext:
  cell_metadata_filter: all
  formats: ipynb,py:percent
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
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

+++ {"nbgrader": {"grade": false, "grade_id": "cell-f686910c4b34f225", "locked": true, "schema_version": 1, "solution": false}}

# Introduction

This notebook asks you to adapt the [multichan assignment](https://clouds.eos.ubc.ca/~phil/courses/atsc301/coursebuild/html/multichan_assignment.html) notebook to look at seasonal changes in the your landsat scenes. (Rerun that notebook to see changes I made to fix the ndvi for landsat 7, and to add the Normalization object to ax.imshow).

Most of the cells will work with my own Vancouver data.  If you set the variable:

    run_example=True

in a cell then it will execute with my data.  For the assignment, I've left 5 cells unfinshed -- they are labeled Question A-E.  The assignment requires you to create a nested dictionary called file_dict that holds the names of your tif files for the red, nearir and thermal channels, then use them to calculate the change in ndvi and the change in temperature between seasons for your fall and spring landsat images.

Here is a quick question summary:

* Question A: set up a dictionary called file_dict with the following structure:

        file_dict={'fall': {'filenames': {'mtl': mtl.txt_name,
                                'nearir': neair.tiff_name
                                'red': red.tiff_name
                                'thermal': thermal.tiff_name
                   'spring': {'filenames': {'mtl': mtl.txt_name,
                                  'nearir': nearir.tiff_name,
                                  'red': red.tiff_name,
                                  'thermal': thermal.tiff_name}}

where "xxx_name" is a str giving the location of your file for a particular band and season.

* Question B:

  * Define a subscene and add it to file_dict for each season  (note the rows and columns will be different for the different swaths, but the ul_x,ul_y should be the same):

        file_dict[season]['small_window']=Window(ul_col, ul_row, width, height)
        print(file_dict[season]['small_window'])
        file_dict[season]['new_affine']=Affine(30.,0.,ul_x,0.,-30.,ul_y)
        file_dict[season]['extent'] = [ul_x,lr_x,lr_y,ul_y]

* Question C:

  * Plot a mapped image on the tiff's UTM crs of the spring-fall ndvi difference for you window

* Question D:

  * Use a301.radiation.planck_invert to find the brightness temperature for your spring scene and map it

* Question E:

  * Find the coldest  pixels in your fall image and map their ndvi, setting all warmer pixels to np.nan

```{code-cell} ipython3
---
nbgrader:
  grade: false
  grade_id: cell-a3f4e924ca02ab89
  locked: true
  schema_version: 1
  solution: false
---
import pprint
from pathlib import Path

import cartopy
import numpy as np
import rasterio
from affine import Affine
from IPython.display import Image
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from pyproj import Proj
from pyproj import transform as proj_transform
from rasterio.windows import Window

import a301
from a301.landsat.landsat_metadata import landsat_metadata
from a301.landsat.toa_radiance import calc_radiance_457
from a301.landsat.toa_radiance import calc_radiance_8
from a301.landsat.toa_reflectance import calc_refl_457
from a301.landsat.toa_reflectance import calc_reflc_8
from a301.radiation import planck_invert
from a301.utils.data_read import download
import numpy as np
```

+++ {"nbgrader": {"grade": false, "grade_id": "cell-b700b41e2d83fe79", "locked": true, "schema_version": 1, "solution": false}}

# Get bands the near-ir, red, and thermal tiffs for your landsat scene

Write the filenmes into a nested dictionary called file_dict.  In the cell below I do this for
my Vancouver scenes to what the structure should look like.

Note that landsat7 and landsat8 have their bands in different orders:

https://www.esri.com/arcgis-blog/products/product/imagery/band-combinations-for-landsat-8/

Note from this link that landsat 7 and landsat 8 made different tradeoffs for their thermal channel.  Landsat

I use landsat_band_dict to keep track of the different channel numbers.


* for landsat 8: landsat_band_dict={'red':4,'nearir':5,'thermal':10}

* for landsat 7: landsat_band_dict={'red':3,'nearir':4,'thermal':'6_VCID_1'}

+++

# To run my example.

set

    run_example=True

if you want to see how these cells work for the vancouver scenes

and set

    landsat8=False

to see the landsat 7 image instead of landsat 8.

```{code-cell} ipython3
run_example = True
landsat8 = True
```

## Preliminary set up: create my example folders which will hold my tif files

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-8d3705a4a6fbb7bc
  locked: false
  points: 5
  schema_version: 1
  solution: true
---
if run_example:
    file_dict = {}
    file_dict["spring"] = dict()
    file_dict["fall"] = dict()
    if landsat8:
        landsat_band_dict = {"red": 4, "nearir": 5, "thermal": 10}
        file_dict["spring"]["root"] = "LC08_L1TP_047026_20150614_20180131_01_T1_"
        file_dict["spring"]["prefix_remote"] = Path(
            "landsat_scenes/l8_vancouver/spring"
        )
        file_dict["spring"]["prefix_local"] = Path("landsat8/vancouver/spring")
        file_dict["fall"]["root"] = "LC08_L1TP_047026_20140203_20170307_01_T1_"
        file_dict["fall"]["prefix_remote"] = Path("landsat_scenes/l8_vancouver/fall")
        file_dict["fall"]["prefix_local"] = Path("landsat8/vancouver/fall")
    else:
        landsat_band_dict = {"red": 3, "nearir": 4, "thermal": "6_VCID_1"}
        file_dict["spring"]["root"] = "LE07_L1TP_047026_20180513_20180610_01_T1_"
        file_dict["spring"]["prefix_remote"] = Path(
            "landsat_scenes/l7_vancouver/spring"
        )
        file_dict["spring"]["prefix_local"] = Path("landsat7/vancouver/spring")
        file_dict["fall"]["root"] = "LE07_L1TP_047026_20141110_20160904_01_T1_"
        file_dict["fall"]["prefix_remote"] = Path("landsat_scenes/l7_vancouver/fall")
        file_dict["fall"]["prefix_local"] = Path("landsat7/vancouver/fall")
    pprint.pprint(file_dict)
```

## Download all my example files

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-8d3705a4a6fbb7bc
  locked: false
  points: 5
  schema_version: 1
  solution: true
---
if run_example:
    for season in ["fall", "spring"]:
        season_dict = file_dict[season]
        root = season_dict["root"]
        name_dict = dict()
        prefix_local = season_dict["prefix_local"]
        prefix_remote = season_dict["prefix_remote"]
        the_file = Path(f"{root}MTL.txt")
        mtl_file = prefix_remote / the_file
        dest_folder = a301.data_dir / prefix_local
        dest_folder.mkdir(parents=True, exist_ok=True)
        download(str(mtl_file), dest_folder=dest_folder)
        name_dict["mtl"] = str(a301.data_dir / prefix_local / the_file)
        for key, band_num in landsat_band_dict.items():
            name_dict[key] = f"{root}B{band_num}.TIF"
        season_dict["filenames"] = name_dict
        for key, the_file in name_dict.items():
            landsat_tif = season_dict["prefix_remote"] / Path(the_file)
            download(str(landsat_tif), dest_folder=dest_folder)
            name_dict[key] = str(a301.data_dir / prefix_local / the_file)
```

## See what my  version of file_dict looks like

```{code-cell} ipython3
#
# deletefile_dict entries we don't need anymore, leaving just the filenames for each season
#
if run_example:
    for season in ["spring", "fall"]:
        for key in ["prefix_local", "prefix_remote", "root"]:
            del file_dict[season][key]
    pprint.pprint(file_dict)
```

# Question A: define your own version of  file_dict

In the next cell create a version of file_dict with the same structure as mine, but with your filenames substituted
for mine

```{code-cell} ipython3

```

+++ {"nbgrader": {"grade": false, "grade_id": "cell-dd09edb695c92076", "locked": true, "schema_version": 1, "solution": false}}

# This cell reads in your affine transform, metadata and profile

Using red band file for transform/profile information (arbitrary)

```{code-cell} ipython3
---
nbgrader:
  grade: false
  grade_id: cell-daebc17375c70921
  locked: true
  schema_version: 1
  solution: false
---
metadata = landsat_metadata(file_dict["spring"]["filenames"]["mtl"])
zone = metadata.UTM_ZONE
crs = cartopy.crs.UTM(zone, southern_hemisphere=False)
p_utm = Proj(crs.proj4_init)
p_lonlat = Proj(proj="latlong", datum="WGS84")
file_dict["satellite"] = metadata.SPACECRAFT_ID
```

+++ {"nbgrader": {"grade": false, "grade_id": "cell-cef7282b3b40dd6f", "locked": true, "schema_version": 1, "solution": false}}

# This cell gets the right reflection and radiance functions for your satellite

See [the library listing](https://clouds.eos.ubc.ca/~phil/courses/atsc301/codedoc/full_listing.html) for the function signatures.

```{code-cell} ipython3
---
nbgrader:
  grade: false
  grade_id: cell-df3ceb3d365ce669
  locked: true
  schema_version: 1
  solution: false
---
refl_dict = {"LANDSAT_7": calc_refl_457, "LANDSAT_8": calc_reflc_8}
radiance_dict = {"LANDSAT_7": calc_radiance_457, "LANDSAT_8": calc_radiance_8}
satellite = metadata.SPACECRAFT_ID
refl_fun = refl_dict[satellite]
radiance_fun = radiance_dict[satellite]
```

+++ {"nbgrader": {"grade": false, "grade_id": "cell-175a34f2bd5cec2f", "locked": true, "schema_version": 1, "solution": false}}

# Question B: Define a subscene window and a transform

In the cell below following this one, get the upper left col,row (ul_col,ul_row) and upper left and lower
right x,y (ul_x,ul_y,lr_x,lr_y)
coordinates the upper left corner of
your subscene as in the image_zoom notebook.  Use ul_col, ul_row, ul_x, ul_y plus your subscene
width and height to make a rasterio window and new transform.

    window=Window(ul_col, ul_row, small_width, small_height)
    new_affine=Affine(30.,0.,ul_x,0.,-30.,ul_y)
    extent = [ul_x,lr_x,lr_y,ul_y]

**Note that the rows and columns for your ul_x and ul_y are going to be different between spring and fall**

After the cell executes, it should have filled in the following values for file_dict for each
of the two seasons (['spring', 'fall']:

    file_dict[season]['small_window']=Window(ul_col, ul_row, width, height)
    print(file_dict[season]['small_window'])
    file_dict[season]['new_affine']=Affine(30.,0.,ul_x,0.,-30.,ul_y)
    file_dict[season]['extent'] = [ul_x,lr_x,lr_y,ul_y]

**Note that the extent=[ul_x,lr_x,lr_y,ul_y] should not change from season to season, I keep both spring and fall as a  check**

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-5d894d6363b58394
  locked: false
  points: 10
  schema_version: 1
  solution: true
---
### BEGIN SOLUTION
ubc_lon = -123.2460
ubc_lat = 49.2606
ubc_x, ubc_y = proj_transform(p_lonlat, p_utm, ubc_lon, ubc_lat)
for season in ["spring", "fall"]:
    name_dict = file_dict[season]["filenames"]
    metadata = landsat_metadata(name_dict["mtl"])
    with rasterio.open(name_dict["red"]) as raster:
        affine_transform = raster.transform
    ubc_col, ubc_row = ~affine_transform * (ubc_x, ubc_y)
    ubc_col, ubc_row = int(ubc_col), int(ubc_row)
    l_col_offset = -100
    t_row_offset = -100
    width = 200
    height = 200
    ul_col = ubc_col + l_col_offset
    ul_row = ubc_row + t_row_offset
    ul_x, ul_y = affine_transform * (ul_col, ul_row)
    lr_x, lr_y = affine_transform * (ul_col + width, ul_row + height)
    file_dict[season]["small_window"] = Window(ul_col, ul_row, width, height)
    print(file_dict[season]["small_window"])
    file_dict[season]["new_affine"] = Affine(30.0, 0.0, ul_x, 0.0, -30.0, ul_y)
    file_dict[season]["extent"] = [ul_x, lr_x, lr_y, ul_y]
### END SOLUTION
```

+++ {"nbgrader": {"grade": false, "grade_id": "cell-cd9770b2c44fe58c", "locked": true, "schema_version": 1, "solution": false}}

# The cell below calculates the reflectivities for red and nearir

```{code-cell} ipython3
---
nbgrader:
  grade: false
  grade_id: cell-3b8481e8992f8a6a
  locked: true
  schema_version: 1
  solution: false
---
for season in ["spring", "fall"]:
    name_dict = file_dict[season]["filenames"]
    metadata_string = str(name_dict["mtl"])
    refl_dict = dict()
    small_window = file_dict[season]["small_window"]
    for key in ["red", "nearir"]:
        filepath = name_dict[key]
        bandnum = landsat_band_dict[key]
        with rasterio.open(filepath) as src:
            counts = src.read(1, window=small_window)
            counts = counts.astype(np.float32)
            counts[counts == 0.0] = np.nan
            refl_vals = refl_fun(counts, bandnum, metadata_string)
            refl_dict[key] = refl_vals
    file_dict[season]["reflect"] = refl_dict
for season in ["spring", "fall"]:
    print(np.nanmean(file_dict[season]["reflect"]["nearir"]))
```

+++ {"nbgrader": {"grade": false, "grade_id": "cell-f4c6415f2226afe9", "locked": true, "schema_version": 1, "solution": false}}

# Question C: map your ndvi spring-fall difference

After this cell executes you should have two new entries in the file_dict:

    file_dict['spring']['ndvi']
    file_dict['fall']['ndvi']

And a plot of the ndvi difference for spring - fall

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-6589d24a5ba25504
  locked: false
  points: 2
  schema_version: 1
  solution: true
---
# I used vmin=-1, vmax=1 for my normalization

### BEGIN SOLUTION
for season in ["spring", "fall"]:
    red = file_dict[season]["reflect"]["red"]
    nearir = file_dict[season]["reflect"]["nearir"]
    ndvi = (nearir - red) / (nearir + red)
    file_dict[season]["ndvi"] = ndvi

extent = file_dict[season]["extent"]
ndvi_diff = file_dict["spring"]["ndvi"] - file_dict["fall"]["ndvi"]
vmin = -1.0
vmax = 1.0
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
palette = "viridis"
pal = plt.get_cmap(palette)
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("w")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black

fig, ax = plt.subplots(1, 1, figsize=[10, 15], subplot_kw={"projection": crs})
col = ax.imshow(ndvi_diff, origin="upper", extent=extent, transform=crs, norm=the_norm)
ax.plot(ul_x, ul_y, "ro", markersize=50)
ax.plot(lr_x, lr_y, "wo", markersize=50)
ax.set(title="spring - fall ndvi difference")
cbar_ax = fig.add_axes([0.95, 0.2, 0.05, 0.6])
cbar = ax.figure.colorbar(col, extend="both", cax=cbar_ax, orientation="vertical")
cbar.set_label("ndvi index")
### END SOLUTION
```

# NDVI checks -- get some statistics

These cells give you a sanity check on your subscene selection.  Is your spring ndvi bigger than your fall?

```{code-cell} ipython3
for season in ["spring", "fall"]:
    ndvi = file_dict[season]["ndvi"]
    print(f"mean ndvi for {season}= {np.nanmean(ndvi)}")
    print("-" * 50)
```

```{code-cell} ipython3
fig, axes = plt.subplots(1, 2, figsize=(10, 6))
for the_ax, season in zip(axes, ["spring", "fall"]):
    ndvi = file_dict[season]["ndvi"]
    the_ax.hist(ndvi[~np.isnan(ndvi)].flat)
    the_ax.set_title(f"ndvi from {satellite}")
    the_ax.set(xlabel=f"ndvi (unitless) {season}", ylabel="counts")
```

```{code-cell} ipython3
---
nbgrader:
  grade: false
  grade_id: cell-bad1a69cdb6fa35c
  locked: true
  schema_version: 1
  solution: false
---
plt.hist(ndvi[~np.isnan(ndvi)].flat)
plt.title("spring ndvi")
plt.savefig("spring_ndvi.png")
```

# This cell reads in the thermal band and calculates the radiance

```{code-cell} ipython3
---
nbgrader:
  grade: false
  grade_id: cell-3b8481e8992f8a6a
  locked: true
  schema_version: 1
  solution: false
---
for season in ["spring", "fall"]:
    key = "thermal"
    filepath = file_dict[season]["filenames"][key]
    bandnum = landsat_band_dict[key]
    with rasterio.open(filepath) as src:
        counts = src.read(1, window=small_window)
        counts = counts.astype(np.float32)
        counts[counts == 0.0] = np.nan
        thermal_rad = radiance_fun(counts, bandnum, metadata_string)
    file_dict[season]["thermal"] = thermal_rad
```

# This cell histograms your spring/fall thermal radiances

```{code-cell} ipython3
---
nbgrader:
  grade: false
  grade_id: cell-3b8481e8992f8a6a
  locked: true
  schema_version: 1
  solution: false
---
fig, ax = plt.subplots(1, 2, figsize=(12, 8))
for index, season in enumerate(["spring", "fall"]):
    thermal_rad = file_dict[season]["thermal"]
    ax[index].hist(thermal_rad[~np.isnan(thermal_rad)].flat)
    ax[index].set_title(f"{satellite} in {season}")
    ax[index].set(xlabel="radiance in W/m^2/micron/sr", ylabel="counts")
```

# Question D: calculate the brightness temperature

Referring back to:

https://www.esri.com/arcgis-blog/products/product/imagery/band-combinations-for-landsat-8/

Note from this link that landsat 7 and landsat 8 made different tradeoffs for their thermal channel.  Landsat 7 has two channel 6's with different channel ranges 6 [see this link](https://landsat.usgs.gov/why-are-there-two-thermal-band-6-files-landsat-7-data-i-downloaded) -- we are using 6.VCID_1 which has a wider temperature range but coarser intevals.  For Landsat 8, they instead split the thermal channel into two wavelength intervals, channel 10 and channel 11.  We are using channel 10 for landsat 8.  Also note that the Landsat 8 thermal channel has 100 meter pixels, while the Landsat 6 channel 6 has 60 meter pixels.  In both cases they are resampled to the same 30 meter grid as the reflectance channels, so pixels can be overlayed.


After this cell executes you should have two new entries in the file_dict:

    file_dict['spring']['btemp']
    file_dict['fall']['btemp']

And a plot of the spring brightness temperature for your thermal channel



```{code-cell} ipython3
### BEGIN SOLUTION
landsat7_thermal = np.array([10.4, 12.5])
landsat7_center = (landsat7_thermal[0] + landsat7_thermal[1]) / 2.0
landsat8_thermal = np.array([11.19, 10.6])
landsat8_center = (landsat8_thermal[0] + landsat8_thermal[1]) / 2.0
thermal_center = dict(LANDSAT_7=landsat7_center, LANDSAT_8=landsat8_center)
band_center = thermal_center[file_dict["satellite"]]
for season in ["fall", "spring"]:
    file_dict[season]["btemp"] = planck_invert(
        band_center * 1.0e-6, file_dict[season]["thermal"] * 1.0e6
    )

season = "spring"
vmin = 290.0
vmax = 310
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
palette = "viridis"
pal = plt.get_cmap(palette)
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("w")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
fig, ax = plt.subplots(1, 1, figsize=[10, 15], subplot_kw={"projection": crs})
col = ax.imshow(
    file_dict[season]["btemp"],
    origin="upper",
    extent=extent,
    transform=crs,
    norm=the_norm,
)
ax.set(title=f"{season} brightness temperature for {satellite}")
cbar_ax = fig.add_axes([0.95, 0.2, 0.05, 0.6])
cbar = ax.figure.colorbar(col, extend="both", cax=cbar_ax, orientation="vertical")
cbar.set_label("brightness temperature (K)")
### END SOLUTION
```

# Question E: highlight the ndvi in the coldest fall pixels

In the cell below:

1. Use numpy.quantile to find the T_25 quantile of your fall brightness temperature (i.e., find the temperature that is warmer than all but 25% of your pixels).

2. Make a map of the fall ndvi for your coldest pixels by setting all pixels that are warmer than T_25 in your brightness temperature image to np.nan in your fall ndvi image.  The resulting map will show the status of vegetation in the coldest part of your scene during the winter

```{code-cell} ipython3
### BEGIN SOLUTION
season = "fall"
high_temp = np.nanquantile(file_dict[season]["btemp"], 0.25)
hit = file_dict[season]["btemp"] < high_temp
new_ndvi = np.array(file_dict[season]["ndvi"])
new_ndvi[~hit] = np.nan

vmin = -1.0
vmax = 1.0
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
palette = "viridis"
pal = plt.get_cmap(palette)
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("w")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
fig, ax = plt.subplots(1, 1, figsize=[10, 15], subplot_kw={"projection": crs})
col = ax.imshow(new_ndvi, origin="upper", extent=extent, transform=crs, norm=the_norm)
ax.set(title=f"{season} brightness temperature for {satellite}")
cbar_ax = fig.add_axes([0.95, 0.2, 0.05, 0.6])
cbar = ax.figure.colorbar(col, extend="both", cax=cbar_ax, orientation="vertical")
cbar.set_label("brightness temperature (K)")
### END SOLUTION
```
