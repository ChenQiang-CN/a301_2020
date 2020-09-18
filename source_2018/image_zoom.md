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
<div class="toc"><ul class="toc-item"><li><span><a href="#Introduction" data-toc-modified-id="Introduction-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Introduction</a></span></li><li><span><a href="#Get-the-tiff-files-and-calculate-band-5-reflectance" data-toc-modified-id="Get-the-tiff-files-and-calculate-band-5-reflectance-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Get the tiff files and calculate band 5 reflectance</a></span></li><li><span><a href="#Save-the-crs-and-the-full_affine" data-toc-modified-id="Save-the-crs-and-the-full_affine-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Save the crs and the full_affine</a></span></li><li><span><a href="#Locate-UBC-on-the-map" data-toc-modified-id="Locate-UBC-on-the-map-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Locate UBC on the map</a></span></li><li><span><a href="#Locate-UBC-on-the-image" data-toc-modified-id="Locate-UBC-on-the-image-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Locate UBC on the image</a></span></li><li><span><a href="#make-our-subscene-400-pixels-wide-and-600-pixels-tall,-using-UBC-as-a-reference-point" data-toc-modified-id="make-our-subscene-400-pixels-wide-and-600-pixels-tall,-using-UBC-as-a-reference-point-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>make our subscene 400 pixels wide and 600 pixels tall, using UBC as a reference point</a></span></li><li><span><a href="#Plot-the-raw-band-5-image,-clipped-to-reflectivities-below-0.6" data-toc-modified-id="Plot-the-raw-band-5-image,-clipped-to-reflectivities-below-0.6-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>Plot the raw band 5 image, clipped to reflectivities below 0.6</a></span></li><li><span><a href="#put-this-on-a-map" data-toc-modified-id="put-this-on-a-map-8"><span class="toc-item-num">8&nbsp;&nbsp;</span>put this on a map</a></span></li><li><span><a href="#Use--rasterio--to-write-a-new-tiff-file" data-toc-modified-id="Use--rasterio--to-write-a-new-tiff-file-9"><span class="toc-item-num">9&nbsp;&nbsp;</span>Use  rasterio  to write a new tiff file</a></span><ul class="toc-item"><li><span><a href="#Set-the-affine-transform-for-the-scene" data-toc-modified-id="Set-the-affine-transform-for-the-scene-9.1"><span class="toc-item-num">9.1&nbsp;&nbsp;</span>Set the affine transform for the scene</a></span></li><li><span><a href="#Now-write-this-out-to-small_file.tiff" data-toc-modified-id="Now-write-this-out-to-small_file.tiff-9.2"><span class="toc-item-num">9.2&nbsp;&nbsp;</span>Now write this out to small_file.tiff</a></span></li></ul></li></ul></div>

+++

# Introduction

We need to be able to select a small region of a landsat image to work with.  This notebook

1. zooms in on a 400 pixel wide x 600 pixel high subscene centered on  Vancouver,  using pyproj and the affine transform to map from lat,lon to x,y in UTM zone 10N to row, column in the landsat image

2. Puts on crude coastlines in the UTM-10N crs

3. Calculates the new affine transform for the subcene, and writes the image out to a 1 Mbyte tiff file

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

filenames = [
    "LC08_L1TP_047026_20150614_20180131_01_T1_B4.TIF",
    "LC08_L1TP_047026_20150614_20180131_01_T1_B5.TIF",
    "LC08_L1TP_047026_20150614_20180131_01_T1_MTL.txt",
]
dest_folder = a301.data_dir / Path("landsat8/vancouver")
for the_file in filenames:
    landsat_tif = Path("landsat_scenes/l8_vancouver") / Path(the_file)
    download(str(landsat_tif), dest_folder=dest_folder)
```

# Get the tiff files and calculate band 5 reflectance

```{code-cell}
band4 = list(dest_folder.glob("*_B4.TIF"))[0]
band5 = list(dest_folder.glob("*_B5.TIF"))[0]
mtl_file = list(dest_folder.glob("*MTL.txt"))[0]
```

# Save the crs and the full_affine

We need to keep both full_affine (the affine transform for the full scene, and the coordinate reference system for pyproj (called crs below)

```{code-cell}
with rasterio.open(band5) as b5_raster:
    full_affine = b5_raster.transform
    crs = b5_raster.crs
    full_profile = b5_raster.profile
    refl = toa_reflectance_8([5], mtl_file)
    b5_refl = refl[5]
plt.hist(b5_refl[~np.isnan(b5_refl)].flat)
plt.title("band 5 reflectance whole scene")
```

```{code-cell}
print(f"profile: \n{pprint.pformat(full_profile)}")
```

# Locate UBC on the map

We need to project the center of campus from lon/lat to UTM 10N x,y using pyproj_transform and our crs (which in this case is UTM).  We can transform from lon,lat (p_lonlat) to x,y (p_utm) to anchor us to a known point in the map coordinates.

```{code-cell}
p_utm = Proj(crs)
p_lonlat = Proj(proj="latlong", datum="WGS84")
ubc_lon = -123.2460
ubc_lat = 49.2606
ubc_x, ubc_y = proj_transform(p_lonlat, p_utm, ubc_lon, ubc_lat)
```

# Locate UBC on the image

Now we need to use the affine transform to go between x,y and
col, row on the image.  The next cell creates two slice objects that extend  on either side of the center point.  The tilde (~) in front of the transform indicates that we're going from x,y to col,row, instead of col,row to x,y.  (See [this blog entry](http://www.perrygeo.com/python-affine-transforms.html) for reference.)  Remember that row 0 is the top row, with rows decreasing downward to the south.  To demonstrate, the cell below uses the tranform to calculate the x,y coordinates of the (0,0) corner.

```{code-cell}
full_ul_xy = np.array(full_affine * (0, 0))
print(f"orig ul corner x,y (km)={full_ul_xy*1.e-3}")
```

# make our subscene 400 pixels wide and 600 pixels tall, using UBC as a reference point

We need to find the right rows and columns on the image to save for the subscene.  Do this by working outward from UBC by a certain number of pixels in each direction, using the inverse of the full_affine transform to go from x,y to col,row

```{code-cell}
ubc_col, ubc_row = ~full_affine * (ubc_x, ubc_y)
ubc_col, ubc_row = int(ubc_col), int(ubc_row)
l_col_offset = -100
r_col_offset = +300
b_row_offset = +100
t_row_offset = -500
col_slice = slice(ubc_col + l_col_offset, ubc_col + r_col_offset)
row_slice = slice(ubc_row + t_row_offset, ubc_row + b_row_offset)
section = b5_refl[row_slice, col_slice]
ubc_ul_xy = full_affine * (col_slice.start, row_slice.start)
ubc_lr_xy = full_affine * (col_slice.stop, row_slice.stop)
ubc_ul_xy, ubc_lr_xy
```

# Plot the raw band 5 image, clipped to reflectivities below 0.6

This is a simple check that we got the right section.

```{code-cell}
vmin = 0.0
vmax = 0.6
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
palette = "viridis"
pal = plt.get_cmap(palette)
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("w")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
fig, ax = plt.subplots(1, 1, figsize=(15, 25))
ax.imshow(section, cmap=pal, norm=the_norm, origin="upper")
```

# put this on a map

Note that the origin is switched to "lower" in the x,y coordinate system below,
since y increases upwards.  The coastline is very crude, but at least indicates we've got the coords roughly correct.  See the "high_res_map" notebook for a better coastline.

```{code-cell}
cartopy_crs = cartopy.crs.epsg(crs.to_epsg())
fig, ax = plt.subplots(1, 1, figsize=[15, 25], subplot_kw={"projection": cartopy_crs})
image_extent = [ubc_ul_xy[0], ubc_lr_xy[0], ubc_lr_xy[1], ubc_ul_xy[1]]
ax.imshow(
    section,
    cmap=pal,
    norm=the_norm,
    origin="upper",
    extent=image_extent,
    transform=cartopy_crs,
    alpha=0.8,
)
ax.coastlines(resolution="10m", color="red", lw=2)
ax.plot(ubc_x, ubc_y, "ro", markersize=25)
ax.set_extent(image_extent, crs=cartopy_crs)
```

# Use  rasterio  to write a new tiff file

## Set the affine transform for the scene

We can write this clipped image back out to a much smaller tiff file if we can come up with the new affine transform for the smaller scene.  Referring again [to the writeup](http://www.perrygeo.com/python-affine-transforms.html) we need:

    a = width of a pixel
    b = row rotation (typically zero)
    c = x-coordinate of the upper-left corner of the upper-left pixel
    d = column rotation (typically zero)
    e = height of a pixel (typically negative)
    f = y-coordinate of the of the upper-left corner of the upper-left pixel

which will gives:

new_affine=Affine(a,b,c,d,e,f)

In addition, need to add a third dimension to the section array, because
rasterio expects [band,x,y] for its writer.  Do this with np.newaxis in the next cell

```{code-cell}
image_height, image_width = section.shape
ul_x, ul_y = ubc_ul_xy[0], ubc_ul_xy[1]
new_affine = Affine(30.0, 0.0, ul_x, 0.0, -30.0, ul_y)
out_section = section[np.newaxis, ...]
print(out_section.shape)
```

##  Now write this out to small_file.tiff

See the hires_map notebook for how to read this in and plot it

```{code-cell}
tif_filename = a301.data_dir / Path("small_file.tiff")
num_chans = 1
with rasterio.open(
    tif_filename,
    "w",
    driver="GTiff",
    height=image_height,
    width=image_width,
    count=num_chans,
    dtype=out_section.dtype,
    crs=crs,
    transform=new_affine,
    nodata=0.0,
) as dst:
    dst.write(out_section)
    section_profile = dst.profile

print(f"section profile: {pprint.pformat(section_profile)}")
```
