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

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "f2a725f0a6df3133cdabba9891cf2e7a", "grade": false, "grade_id": "cell-f686910c4b34f225", "locked": true, "schema_version": 1, "solution": false}}

# Introduction

There are 4 cells that ask for changes below, the rest should run as long as you
use the variable names I ask for in the questions.

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  checksum: ae40f07b9f3fc25eb3d3b6a8cdf9931d
  grade: false
  grade_id: cell-a3f4e924ca02ab89
  locked: true
  schema_version: 1
  solution: false
---
import rasterio
import a301
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from a301.landsat.landsat_metadata import landsat_metadata
import cartopy
from rasterio.windows import Window
from pyproj import transform as proj_transform
from pyproj import Proj
from a301.landsat.toa_reflectance import calc_reflc_8
import pprint
from a301.utils.data_read import download
from pathlib import Path
from affine import Affine
from IPython.display import Image
from a301.landsat.toa_reflectance import calc_refl_457, calc_reflc_8
from mpl_toolkits.axes_grid1 import make_axes_locatable
```

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "a6a0b678fee374f8fd780af2e8212534", "grade": false, "grade_id": "cell-b700b41e2d83fe79", "locked": true, "schema_version": 1, "solution": false}}

# Get bands 3, 4, 5 fullsize (green, red, near-ir)

At the end of this cell you shiould have the following path objects for your spring scene:

meta_bigfile, band3_bigfile, band4_bigfile, band5_bigfile

that point to your landsat TIF and mtl.txt files.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  checksum: bd530dfcc0915ef07f406d66a6e9ab19
  grade: true
  grade_id: cell-8d3705a4a6fbb7bc
  locked: false
  points: 5
  schema_version: 1
  solution: true
---
# YOUR CODE HERE
raise NotImplementedError()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "9fb67423f53a74e6d0938fdc11b576f9", "grade": false, "grade_id": "cell-dd09edb695c92076", "locked": true, "schema_version": 1, "solution": false}}

# This cell reads in your affine transform, metadata and profile

Using band4_bigfile (arbitrary)

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  checksum: fd9b887e24b2e779a87e86343a481929
  grade: false
  grade_id: cell-daebc17375c70921
  locked: true
  schema_version: 1
  solution: false
---
metadata=landsat_metadata(meta_bigfile)
with rasterio.open(band4_bigfile) as raster:
    big_transform=raster.transform
    big_profile=raster.profile

zone = metadata.UTM_ZONE  
crs = cartopy.crs.UTM(zone, southern_hemisphere=False)
p_utm=Proj(crs.proj4_init)
p_lonlat=Proj(proj='latlong',datum='WGS84')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "180ccc2ae48fe00624463a632c2ba4c5", "grade": false, "grade_id": "cell-cef7282b3b40dd6f", "locked": true, "schema_version": 1, "solution": false}}

# This cell gets the right reflection function for your satellite

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  checksum: a569fb135cf6d2c03c256eeb90dfc4cd
  grade: false
  grade_id: cell-df3ceb3d365ce669
  locked: true
  schema_version: 1
  solution: false
---
refl_dict={'LANDSAT_7':calc_refl_457,'LANDSAT_8':calc_reflc_8}         
satellite=metadata.SPACECRAFT_ID
refl_fun=refl_dict[satellite]
```

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "2a2e43c2bd396ec6c833132db854ff2e", "grade": false, "grade_id": "cell-175a34f2bd5cec2f", "locked": true, "schema_version": 1, "solution": false}}

# Define a subscene window and a transform

In the cell below, get the upper left col,row (ul_col,ul_row) and upper left and lower
right x,y (ul_x,ul_y,lr_x,lr_y)
coordinates the upper left corner of 
your subscene as in the image_zoom notebook.  Use ul_col, ul_row, ul_x, ul_y plus your subscene
width and height to make a rasterio window and new transform.

    window=Window(ul_col, ul_row, small_width, small_height)
    new_affine=Affine(30.,0.,ul_x,0.,-30.,ul_y)
    extent = [ul_x,lr_x,lr_y,ul_y]

```{code-cell} ipython3
---
deletable: false
nbgrader:
  checksum: d2653ec0563ac7b9360aa2fea0b02ce1
  grade: true
  grade_id: cell-5d894d6363b58394
  locked: false
  points: 10
  schema_version: 1
  solution: true
---
# YOUR CODE HERE
raise NotImplementedError()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "6ca9ab84b73436d766da049854a344f8", "grade": false, "grade_id": "cell-cd9770b2c44fe58c", "locked": true, "schema_version": 1, "solution": false}}

# Read only the window pixels from the band 3, 4, 5 files

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  checksum: d69466c2596f10da196bc03b9eb018cf
  grade: false
  grade_id: cell-3b8481e8992f8a6a
  locked: true
  schema_version: 1
  solution: false
---
refl_dict=dict()
for bandnum,filepath in zip([3,4,5],[band3_bigfile,band4_bigfile,band5_bigfile]):
    with rasterio.open(filepath) as src:
        counts = src.read(1, window=small_window)
        refl_vals = refl_fun(counts,bandnum,metadata)
        refl_dict[bandnum]=refl_vals
```

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "078d2a6849249fe57737cadb79c70f26", "grade": false, "grade_id": "cell-f4c6415f2226afe9", "locked": true, "schema_version": 1, "solution": false}}

# In the next cell calculate your ndvi

Save it in a variable called ndvi

```{code-cell} ipython3
---
deletable: false
nbgrader:
  checksum: 8046e7b4f1d3ba44bc68a6b8295cba36
  grade: true
  grade_id: cell-6589d24a5ba25504
  locked: false
  points: 2
  schema_version: 1
  solution: true
---
# YOUR CODE HERE
raise NotImplementedError()
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  checksum: 1135f8a462ba4944dd8960243e8adb96
  grade: false
  grade_id: cell-bad1a69cdb6fa35c
  locked: true
  schema_version: 1
  solution: false
---
plt.hist(ndvi[~np.isnan(ndvi)].flat);
plt.title('spring ndvi')
plt.savefig('spring_ndvi.png')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "08629247dda3c3fd3ed08bdd0ef88ef5", "grade": false, "grade_id": "cell-b68f0e3d1ae9ea4d", "locked": true, "schema_version": 1, "solution": false}}

# In the next cell plot a mapped ndvi image with a red dot in your ul corner and a white dot in your lr corner

Adjust this plot to fit your image.  Just delete the bottom line and work with the provided commands

```{code-cell} ipython3
---
deletable: false
nbgrader:
  checksum: d88915acfe68c876b24640af663ce1f0
  grade: true
  grade_id: cell-49219670aafdaf44
  locked: false
  points: 5
  schema_version: 1
  solution: true
---
vmin=0.0
vmax=0.8
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
palette='viridis'
pal = plt.get_cmap(palette)
pal.set_bad('0.75') #75% grey for out-of-map cells
pal.set_over('w')  #color cells > vmax red
pal.set_under('k')  #color cells < vmin black
fig, ax = plt.subplots(1, 1,figsize=[10,15],
                       subplot_kw={'projection': crs})
col=ax.imshow(ndvi,origin="upper",
         extent=extent,transform=crs)
ax.plot(ul_x,ul_y,'ro',markersize=50)
ax.plot(lr_x,lr_y,'wo',markersize=50)
ax.set(title="spring ndvi")
cbar_ax = fig.add_axes([0.95, 0.2, 0.05, 0.6])
cbar=ax.figure.colorbar(col,extend='both',cax=cbar_ax,orientation='vertical')
cbar.set_label('ndvi index')
# YOUR CODE HERE
raise NotImplementedError()
```
