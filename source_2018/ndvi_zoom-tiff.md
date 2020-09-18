---
jupytext:
  cell_metadata_filter: all
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

```{code-cell} ipython3
import a301
print(a301.__file__)
```

+++ {"toc": true}

<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#Introduction" data-toc-modified-id="Introduction-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Introduction</a></span></li><li><span><a href="#Get-the-tiff-files-and-calculate-band-5-reflectance" data-toc-modified-id="Get-the-tiff-files-and-calculate-band-5-reflectance-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Get the tiff files and calculate band 5 reflectance</a></span></li><li><span><a href="#Save-the-crs-and-the-map_transform" data-toc-modified-id="Save-the-crs-and-the-map_transform-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Save the crs and the map_transform</a></span></li><li><span><a href="#Locate-UBC-on-the-map" data-toc-modified-id="Locate-UBC-on-the-map-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Locate UBC on the map</a></span></li><li><span><a href="#Locate-UBC-on-the-image" data-toc-modified-id="Locate-UBC-on-the-image-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Locate UBC on the image</a></span></li><li><span><a href="#make-our-subscene-400-pixels-wide-and-600-pixels-tall" data-toc-modified-id="make-our-subscene-400-pixels-wide-and-600-pixels-tall-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>make our subscene 400 pixels wide and 600 pixels tall</a></span></li><li><span><a href="#Plot-the-raw-band-5-image,-clipped-to-reflectivities-below-0.6" data-toc-modified-id="Plot-the-raw-band-5-image,-clipped-to-reflectivities-below-0.6-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>Plot the raw band 5 image, clipped to reflectivities below 0.6</a></span></li><li><span><a href="#put-this-on-a-map" data-toc-modified-id="put-this-on-a-map-8"><span class="toc-item-num">8&nbsp;&nbsp;</span>put this on a map</a></span></li><li><span><a href="#Use--rasterio--to-write-a-new-tiff-file" data-toc-modified-id="Use--rasterio--to-write-a-new-tiff-file-9"><span class="toc-item-num">9&nbsp;&nbsp;</span>Use  rasterio  to write a new tiff file</a></span></li><li><span><a href="#Now-write-this-out-to-small_file.tiff" data-toc-modified-id="Now-write-this-out-to-small_file.tiff-10"><span class="toc-item-num">10&nbsp;&nbsp;</span>Now write this out to small_file.tiff</a></span></li><li><span><a href="#Higher-resolution-coastline" data-toc-modified-id="Higher-resolution-coastline-11"><span class="toc-item-num">11&nbsp;&nbsp;</span>Higher resolution coastline</a></span></li></ul></div>

+++

# Introduction

We need to be able to select a small region of a landsat image to work with.  This notebook 

1. zooms in on a 200 pixel x 200 pixel subscene centered on the UBC Vancouver campus using pyproj an affine transform to map from lat,lon to x,y in UTM zone 10N to row, column in the landsat image

2. Uses a rasterio window to calculate the new affine transform for that subscene 

3. writes the subscene  out to a much smaller tiff file.

4. plots the subscene on a cartopy map and marks the center with a red dot

5. reads in a coastline from the openstreetmaps project and plots that.

```{code-cell} ipython3
import rasterio
import a301
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable
import cartopy
from rasterio.windows import Window
from pyproj import transform as proj_transform
from pyproj import Proj
from a301.landsat.toa_reflectance import toa_reflectance_8
import pprint
from a301.utils.data_read import download
from pathlib import Path
from affine import Affine

filenames=["LC08_L1TP_047026_20150614_20180131_01_T1_B4.TIF",
    "LC08_L1TP_047026_20150614_20180131_01_T1_B5.TIF",
    "LC08_L1TP_047026_20150614_20180131_01_T1_MTL.txt"]
dest_folder=Path("/Users/phil/repos/a301_code/test_data/landsat8")
```

# Get the tiff files and calculate band 5 reflectance

```{code-cell} ipython3
band4=list(dest_folder.glob("**/*_B4.TIF"))[0]
band5=list(dest_folder.glob("**/*_B5.TIF"))[0]
mtl_file=list(dest_folder.glob("**/*MTL.txt"))[0]
```

# Save the crs and the map_transform

We need to keep both map_transform (the affine transform for the full scened, and the projection transform from pyproj (called proj_transform below)

```{code-cell} ipython3
with rasterio.open(band5) as b5_raster:
    full_affine=b5_raster.transform
    crs=b5_raster.crs
    full_profile=b5_raster.profile
    refl=toa_reflectance_8([5],mtl_file)
    b5_refl=refl[5]
plt.hist(b5_refl[~np.isnan(b5_refl)].flat)
plt.title('band 5 reflectance whole scene')
```

```{code-cell} ipython3
print(f"profile: \n{pprint.pformat(full_profile)}")
```

# Locate UBC on the map

We need to project the center of campus from lon/lat to UTM 10N x,y using pyproj.transform

```{code-cell} ipython3
p_utm = Proj(crs)
p_latlon=Proj(proj='latlong',datum='WGS84')
ubc_lon = -123.2460
ubc_lat = 49.2606
ubc_x, ubc_y =proj_transform(p_latlon,p_utm,ubc_lon, ubc_lat) 
```

# Locate UBC on the image

Now we need to use the affine transform to go between x,y and 
col, row on the image.  The next cell creates two slice objects that extend  on either side of the center point.  The tilde (~) in front of the transform indicates that we're going from x,y to col,row, instead of col,row to x,y.  (See [this blog entry](http://www.perrygeo.com/python-affine-transforms.html) for reference.)  Remember that row 0 is the top row, with rows decreasing downward to the south.

```{code-cell} ipython3
full_ul_xy=np.array(full_affine*(0,0))
print(f"orig ul corner x,y (km)={full_ul_xy*1.e-3}")
```

# make our subscene 400 pixels wide and 600 pixels tall

```{code-cell} ipython3
ubc_col, ubc_row = ~full_affine*(ubc_x,ubc_y)
ubc_col, ubc_row = int(ubc_col), int(ubc_row)
l_col_offset= -100
r_col_offset= +300
b_row_offset= +100
t_row_offset= -500
col_slice=slice(ubc_col+l_col_offset,ubc_col+r_col_offset)
row_slice=slice(ubc_row + t_row_offset, ubc_row + b_row_offset)
section=b5_refl[row_slice,col_slice]
ubc_ul_xy = full_affine*(col_slice.start,row_slice.start)
ubc_lr_xy = full_affine*(col_slice.stop,row_slice.stop)
ubc_ul_xy,ubc_lr_xy
```

# Plot the raw band 5 image, clipped to reflectivities below 0.6

Note that the origin is "upper" because the (0,0) pixel is the upper
left corner

```{code-cell} ipython3
vmin=0.0
vmax=0.6
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
palette='viridis'
pal = plt.get_cmap(palette)
pal.set_bad('0.75') #75% grey for out-of-map cells
pal.set_over('w')  #color cells > vmax red
pal.set_under('k')  #color cells < vmin black
fig, ax = plt.subplots(1,1,figsize=(15,25))
ax.imshow(section,cmap=pal,norm=the_norm,origin="upper");
```

# put this on a map

Note that the origin is "lower" in the x,y coordinate system,
since y increases upwards

```{code-cell} ipython3
cartopy_crs=cartopy.crs.epsg(crs.to_epsg())
fig, ax = plt.subplots(1, 1,figsize=[15,25],
                       subplot_kw={'projection': cartopy_crs})
image_extent=[ubc_ul_xy[0],ubc_lr_xy[0],ubc_ul_xy[1],ubc_lr_xy[1]]
ax.imshow(section,cmap=pal,norm=the_norm,origin="lower",
         extent=image_extent,transform=cartopy_crs,alpha=0.8);
ax.coastlines(resolution='10m',color='red',lw=2);
ax.plot(ubc_x, ubc_y,'ro',markersize=25)
ax.set_extent(image_extent,crs=cartopy_crs)
```

# Use  rasterio  to write a new tiff file

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

```{code-cell} ipython3
image_height, image_width = section.shape
ul_x, ul_y = ubc_ul_xy[0], ubc_ul_xy[1]
new_affine=(30.,0.,ul_x,0.,-30.,ul_y)
out_section=section[np.newaxis,...]
print(out_section.shape)
```

# Now write this out to small_file.tiff

```{code-cell} ipython3
tif_filename=a301.data_dir / Path('small_file.tiff')    
num_chans=1
with rasterio.open(tif_filename,'w',driver='GTiff',
                   height=image_height,width=image_width,
                   count=num_chans,dtype=out_section.dtype,
                   crs=crs,transform=new_affine, nodata=0.0) as dst:
        dst.write(out_section)
        section_profile=dst.profile
        
print(f"section profile: {pprint.pformat(section_profile)}")
```

# Higher resolution coastline

+++

Here is what Point Grey looks like with the [open street maps](https://automating-gis-processes.github.io/2017/lessons/L7/retrieve-osm-data.html) coastline database

```{code-cell} ipython3
cartopy_crs=cartopy.crs.epsg(crs.to_epsg())
fig, ax = plt.subplots(1, 1,figsize=[15,25],
                       subplot_kw={'projection': cartopy_crs})
image_extent=[ubc_ul_xy[0],ubc_lr_xy[0],ubc_ul_xy[1],ubc_lr_xy[1]]
ax.imshow(section,cmap=pal,norm=the_norm,origin="lower",
         extent=image_extent,transform=cartopy_crs,alpha=0.8);
ax.plot(ubc_x, ubc_y,'ro',markersize=25)
ax.set_extent(image_extent,crs=cartopy_crs)
from cartopy.io import shapereader
shape_project=cartopy.crs.PlateCarree()
coast_path = Path(f"/Users/phil/repos/a301_code_fresh/test_data")
shp = shapereader.Reader(str(coast_path / 
                             Path("ubc_coastlines/lines.shp")))
for record, geometry in zip(shp.records(), shp.geometries()):
    ax.add_geometries([geometry], shape_project,facecolor="none",
                      edgecolor='red',lw=2)
```

```{code-cell} ipython3

```
