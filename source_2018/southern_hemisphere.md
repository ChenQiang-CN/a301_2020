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
<div class="toc"><ul class="toc-item"><li><span><a href="#Introduction" data-toc-modified-id="Introduction-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Introduction</a></span></li><li><span><a href="#Read-in-a-South-American-image" data-toc-modified-id="Read-in-a-South-American-image-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Read in a South American image</a></span></li><li><span><a href="#Here-is-the-correct-orientation" data-toc-modified-id="Here-is-the-correct-orientation-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Here is the correct orientation</a></span></li><li><span><a href="#Make-two-different-crs-versions-(epsg-and-zone)" data-toc-modified-id="Make-two-different-crs-versions-(epsg-and-zone)-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Make two different crs versions (epsg and zone)</a></span></li><li><span><a href="#Show-that-we-can-get-the-correct-coastline" data-toc-modified-id="Show-that-we-can-get-the-correct-coastline-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Show that we can get the correct coastline</a></span></li><li><span><a href="#confirm-that-pyproj-and-NASA-agree" data-toc-modified-id="confirm-that-pyproj-and-NASA-agree-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>confirm that pyproj and NASA agree</a></span></li></ul></div>

+++

# Introduction

As Darian discovered, the way that the UTM zone scheme handles the equator creates problems for NASA when it tries to map composite images that cross the equator.  The money quote from USGS:

https://landsat.usgs.gov/why-do-southern-hemisphere-scenes-not-display-correct-utm-designation

"Because the use of two different false northing values creates a discontinuity of the scenes when trying to mosaic them, Landsat Level-1 products are processed with a northern UTM zone (i.e., a positive UTM zone), regardless of whether the scene is in the Northern or Southern Hemisphere. With this projection, any scene in the Southern Hemisphere will have a negative projection Y coordinate."

In regular English, what NASA is saying is that the formal definition of UTM north zones sets y=10,000,000 m at the North pole, y=0 at the equator and forbids any negative values of y.  Instead you are supposed to use the UTM south zone south of the equator, which sets y=10,000,000 m at the equator and y=0 at the south pole.  NASA ignores the south zone and keeps y=0 at the equator (no "false northing") and y=-10,000,000 at the south pole.  This is the default for pyproj, so this works with cartopy when we construct the crs with:

     cartopy.crs.UTM(zone, southern_hemisphere=False)

If instead we use the epsg constructor with a North zone code from say https://epsg.io/32656

     cartopy_crs_code=cartopy.crs.epsg(epsg_code)

We get the official UTM y limits and the extent is wrong when we set negative y values.

(see https://github.com/SciTools/cartopy/issues/867 for the details)

Below I show how this works for a southern hemisphere image.

```{code-cell}
import pdb
import pprint
from pathlib import Path

import cartopy
import numpy as np
import rasterio
from affine import Affine
from IPython.display import Image
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pyproj import Proj
from pyproj import transform as proj_transform
from rasterio.windows import Window

import a301
from a301.landsat.landsat_metadata import landsat_metadata
from a301.landsat.toa_reflectance import toa_reflectance_8
from a301.utils.data_read import download
```

# Read in a South American image

```{code-cell}
filenames = [
    "LC08_L1TP_232091_20160108_20170405_01_T1_MTL.txt",
    "LC08_L1TP_232091_20160108_20170405_01_T1_B2.TIF",
]

dest_folder = a301.data_dir / Path("landsat8/southern_hemi")
dest_folder.mkdir(parents=True, exist_ok=True)
for the_file in filenames:
    landsat_tif = Path("landsat_scenes/southern_hemi") / Path(the_file)
    download(str(landsat_tif), dest_folder=dest_folder)

band2 = list(dest_folder.glob("*_B2.TIF"))[0]
mtl_file = list(dest_folder.glob("*_MTL.txt"))[0]

with rasterio.open(band2) as b2_raster:
    full_affine = b2_raster.transform
    crs = b2_raster.crs
    full_profile = b2_raster.profile
    refl = toa_reflectance_8([2], mtl_file)
    b2_refl = refl[2]

plt.hist(b2_refl[~np.isnan(b2_refl)].flat)
plt.title("band 2 reflectance whole scene")
```

# Here is the correct orientation

```{code-cell}
Image("images/LC08_L1TP_232091_20160108_20170405_01_T1.png", width=400)
```

# Make two different crs versions (epsg and zone)

Note the different lower limits on y

```{code-cell}
meta_dict = landsat_metadata(mtl_file).__dict__
zone = meta_dict["UTM_ZONE"]
epsg_code = crs.to_epsg()
print(f"we are in zone {zone} with epsg_code {epsg_code}")
cartopy_crs_code = cartopy.crs.epsg(epsg_code)
cartopy_crs_zone = cartopy.crs.UTM(zone, southern_hemisphere=False)
print(
    f"North zone y limits from the cartopy epsg constructor {cartopy_crs_code.y_limits}"
)
cartopy_crs = cartopy_crs_zone
print(f"North zone y limits from cartopy UTM constructor {cartopy_crs_zone.y_limits}")
```

# Show that we can get the correct coastline

```{code-cell}
vmin = 0.0
vmax = 0.2
cmap_ref = plt.get_cmap("viridis")
cmap_ref.set_over("c")
cmap_ref.set_under("b", alpha=0.2)
cmap_ref.set_bad("0.75")  # 75% grey
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
ul_x = meta_dict["CORNER_UL_PROJECTION_X_PRODUCT"]
lr_x = meta_dict["CORNER_LR_PROJECTION_X_PRODUCT"]
ul_y = meta_dict["CORNER_UL_PROJECTION_Y_PRODUCT"]
lr_y = meta_dict["CORNER_LR_PROJECTION_Y_PRODUCT"]
fig, ax = plt.subplots(1, 1, figsize=[8, 8], subplot_kw={"projection": cartopy_crs})
image_extent = [ul_x, lr_x, lr_y, ul_y]
ax.imshow(
    b2_refl,
    cmap=cmap_ref,
    norm=the_norm,
    origin="upper",
    extent=image_extent,
    transform=cartopy_crs,
)
ax.coastlines(resolution="10m", color="red", lw=2)
```

# confirm that pyproj and NASA agree

Convert the lower right corner from x,y to lon, lat and
check against the metadata

```{code-cell}
print(f"x,y coords of lr corner: {lr_x,lr_y}")
p_utm_18N_nasa = Proj(cartopy_crs_zone.proj4_init)
p_latlon = Proj(proj="latlong", datum="WGS84")
out = proj_transform(p_utm_18N_nasa, p_latlon, lr_x, lr_y)
print(f"pyproj lon,lat {out}")
nasa_lr = meta_dict["CORNER_LR_LON_PRODUCT"], meta_dict["CORNER_LR_LAT_PRODUCT"]
print(f"nasa metadata lon,lat {out}")
#
# note that the transform will default to p_latlon, so we don't really
# need to specify it if we don't want to
#
out = p_utm_18N_nasa(lr_x, lr_y, inverse=True)
print(f"pyproj lon,lat for lr corner: {out}")
```
