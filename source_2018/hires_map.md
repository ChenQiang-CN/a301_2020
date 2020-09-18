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
<div class="toc"><ul class="toc-item"><li><span><a href="#Introduction" data-toc-modified-id="Introduction-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Introduction</a></span></li><li><span><a href="#Read-the-geotiff-with-rasterio" data-toc-modified-id="Read-the-geotiff-with-rasterio-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Read the geotiff with rasterio</a></span></li><li><span><a href="#Locate-UBC-on-the-map" data-toc-modified-id="Locate-UBC-on-the-map-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Locate UBC on the map</a></span></li><li><span><a href="#Higher-resolution-coastline" data-toc-modified-id="Higher-resolution-coastline-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Higher resolution coastline</a></span><ul class="toc-item"><li><span><a href="#Mapped-image-with-no-coastline" data-toc-modified-id="Mapped-image-with-no-coastline-4.1"><span class="toc-item-num">4.1&nbsp;&nbsp;</span>Mapped image with no coastline</a></span></li><li><span><a href="#Read-the-shape-file-and-add-the-coastline-to-the-image" data-toc-modified-id="Read-the-shape-file-and-add-the-coastline-to-the-image-4.2"><span class="toc-item-num">4.2&nbsp;&nbsp;</span>Read the shape file and add the coastline to the image</a></span></li></ul></li></ul></div>

+++

# Introduction

Below we read in the small Vancouver image we wrote out in the image_zoom notebook, and put it on a map with a UTM-10N crs.  We then add a high resolution coastline read from the openstreetmap coastline database.

```{code-cell}
import pprint
from pathlib import Path

import cartopy
import numpy as np
import rasterio
from affine import Affine
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pyproj import Proj
from pyproj import transform as proj_transform
from rasterio.windows import Window

import a301
from a301.landsat.toa_reflectance import toa_reflectance_8
from a301.utils.data_read import download
```

# Read the geotiff with rasterio

```{code-cell}
tif_filename = a301.data_dir / Path("small_file.tiff")
with rasterio.open(tif_filename) as raster:
    affine_transform = raster.transform
    crs = raster.crs
    profile = raster.profile
    refl = raster.read(1)
plt.hist(refl[~np.isnan(refl)].flat)
plt.title("band 5 reflectance for Vancouver section")
```

```{code-cell}
print(f"profile: \n{pprint.pformat(profile)}")
```

# Locate UBC on the map

We need to project the center of campus from lon/lat to UTM 10N x,y using pyproj.transform

```{code-cell}
p_utm = Proj(crs)
p_latlon = Proj(proj="latlong", datum="WGS84")
ubc_lon = -123.2460
ubc_lat = 49.2606
ubc_x, ubc_y = proj_transform(p_latlon, p_utm, ubc_lon, ubc_lat)
height, width = refl.shape
ubc_ul_xy = affine_transform * (0, 0)
ubc_lr_xy = affine_transform * (width, height)
ubc_ul_xy, ubc_lr_xy
```

# Higher resolution coastline

+++

Here is what Point Grey looks like with the [open street maps](https://automating-gis-processes.github.io/2017/lessons/L7/retrieve-osm-data.html) coastline database.

Optional: If you want to do this for your own image your're going to need to reduce the size of the coastlines database.  There is a good article about different sources for map data on the blog [python4oceanographers](
https://ocefpaf.github.io/python4oceanographers/blog/2015/06/22/osm/).  The basic steps that worked for me:

1. Download the 513 Mbyte shape file of the WGS84 coastline database from [openstreetmap](http://openstreetmapdata.com/data/coastlines)

2. Unzipping the file (it will be about 700 Mbytes) will create a folder called
   coastlines-split-4326  (4326 is the epsg number for WGS84 lon/lat)

3. Figure out the lon/lat coordinates of a bounding box that contains your scene

4. Get a fiona prompt, which provides the command line program ogr2ogr
   (ogr stands for"OpenGIS Simple Features Reference Implementation"). For Vancouver, I used this command (all one line, lons are negative, lats are positive).  Substitute your own lons and lats (note all - signs are single, not double hyphens)

       ogr2ogr -skipfailures -f "ESRI Shapefile"  -clipsrc -123.5 49 -123.1 49.4   ubc_coastlines coastlines-split-4326

   this extracts the segments and writes them to a new  folder called [ubc_coastlines](https://github.com/phaustin/a301_code/tree/master/test_data/ubc_coastlines) which is less than 140 K and which provides the coastlines below.



+++

## Mapped image with no coastline

Sanity check to make sure we've got the right image

```{code-cell}
vmin = 0.0
vmax = 0.5
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
palette = "viridis"
pal = plt.get_cmap(palette)
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("w")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
cartopy_crs = cartopy.crs.epsg(crs.to_epsg())
fig, ax = plt.subplots(1, 1, figsize=[15, 25], subplot_kw={"projection": cartopy_crs})
image_extent = [ubc_ul_xy[0], ubc_lr_xy[0], ubc_lr_xy[1], ubc_ul_xy[1]]
ax.imshow(
    refl,
    origin="upper",
    extent=image_extent,
    transform=cartopy_crs,
    cmap=pal,
    norm=the_norm,
)
ax.plot(ubc_x, ubc_y, "ro", markersize=25)
ax.set_extent(image_extent, crs=cartopy_crs)
```

## Read the shape file and add the coastline to the image

Note that PlateCarree is another name for WGS84 datum, simple lat/lon which is the projection of the coastlines-split-4326 shapefile.

```{code-cell}
from cartopy.io import shapereader

shape_project = cartopy.crs.PlateCarree()
shp = shapereader.Reader(str(a301.test_dir / Path("ubc_coastlines/lines.shp")))
for record, geometry in zip(shp.records(), shp.geometries()):
    ax.add_geometries(
        [geometry], shape_project, facecolor="none", edgecolor="red", lw=2
    )
display(fig)
```

```{code-cell}

```
