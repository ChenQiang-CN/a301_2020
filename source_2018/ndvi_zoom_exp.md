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
<div class="toc"><ul class="toc-item"><li><span><a href="#Introduction" data-toc-modified-id="Introduction-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Introduction</a></span></li><li><span><a href="#Get-the-tiff-files-and-calculate-band-5-reflectance" data-toc-modified-id="Get-the-tiff-files-and-calculate-band-5-reflectance-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Get the tiff files and calculate band 5 reflectance</a></span></li><li><span><a href="#Save-the-crs-and-the-map_transform" data-toc-modified-id="Save-the-crs-and-the-map_transform-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Save the crs and the map_transform</a></span></li><li><span><a href="#Locate-UBC-on-the-map" data-toc-modified-id="Locate-UBC-on-the-map-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Locate UBC on the map</a></span></li><li><span><a href="#Locate-UBC-on-the-image" data-toc-modified-id="Locate-UBC-on-the-image-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Locate UBC on the image</a></span></li><li><span><a href="#Plot-the-raw-band-5-image-in-grey,-clipped-to-reflectivities-below-0.6" data-toc-modified-id="Plot-the-raw-band-5-image-in-grey,-clipped-to-reflectivities-below-0.6-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Plot the raw band 5 image in grey, clipped to reflectivities below 0.6</a></span></li><li><span><a href="#Use-a-rasterio-window-to-write-a-new-tiff-file" data-toc-modified-id="Use-a-rasterio-window-to-write-a-new-tiff-file-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>Use a rasterio window to write a new tiff file</a></span></li><li><span><a href="#Make-the-new-affine-transform" data-toc-modified-id="Make-the-new-affine-transform-8"><span class="toc-item-num">8&nbsp;&nbsp;</span>Make the new affine transform</a></span></li><li><span><a href="#Now-write-this-out-to-small_file.tiff" data-toc-modified-id="Now-write-this-out-to-small_file.tiff-9"><span class="toc-item-num">9&nbsp;&nbsp;</span>Now write this out to small_file.tiff</a></span></li><li><span><a href="#Put-this-on-a-cartopy-map" data-toc-modified-id="Put-this-on-a-cartopy-map-10"><span class="toc-item-num">10&nbsp;&nbsp;</span>Put this on a cartopy map</a></span></li><li><span><a href="#Higher-resolution-coastline" data-toc-modified-id="Higher-resolution-coastline-11"><span class="toc-item-num">11&nbsp;&nbsp;</span>Higher resolution coastline</a></span></li></ul></div>

+++

# Introduction

We need to be able to select a small region of a landsat image to work with.  This notebook 

1. zooms in on a 200 pixel x 200 pixel subscene centered on the UBC Vancouver campus using pyproj an affine transform to map from lat,lon to x,y in UTM zone 10N to row, column in the landsat image

2. Uses a rasterio window to calculate the new affine transform for that subscene 

3. writes the subscene  out to a much smaller tiff file.

4. plots the subscene on a cartopy map and marks the center with a red dot

5. reads in a coastline from the openstreetmaps project and plots that.

```{code-cell}
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
import pdb
from a301.landsat.landsat_metadata import landsat_metadata

filenames=["LC08_L1TP_047026_20150614_20180131_01_T1_B4.TIF",
    "LC08_L1TP_047026_20150614_20180131_01_T1_B5.TIF",
    "LC08_L1TP_047026_20150614_20180131_01_T1_MTL.txt"]
dest_folder=a301.data_dir / Path("landsat8/vancouver")
for the_file in filenames:
    landsat_tif = Path('landsat_scenes/l8_vancouver') / Path(the_file)
    download(str(landsat_tif),dest_folder=dest_folder)
```

# Get the tiff files and calculate band 5 reflectance

```{code-cell}
band2=list(dest_folder.glob("*_B2.TIF"))[0]
band3=list(dest_folder.glob("*_B3.TIF"))[0]
band4=list(dest_folder.glob("*_B4.TIF"))[0]
band5=list(dest_folder.glob("*_B5.TIF"))[0]
mtl_file=list(dest_folder.glob("*MTL.txt"))[0]
meta_dict=landsat_metadata(mtl_file).__dict__
```

# Save the crs and the map_transform

We need to keep both map_transform (the affine transform for the full scened, and the projection transform from pyproj (called proj_transform below)

```{code-cell}
with rasterio.open(band5) as b5_raster:
    map_transform=b5_raster.transform
    crs=b5_raster.crs
    profile=b5_raster.profile
    refl=toa_reflectance_8([5],mtl_file)
    b5_refl=refl[5]
plt.hist(b5_refl[~np.isnan(b5_refl)].flat)
plt.title('band 5 reflectance whole scene')
```

```{code-cell}
print(f"profile: \n{pprint.pformat(profile)}")
```

# Locate UBC on the map

We need to project the center of campus from lon/lat to UTM 10N x,y using pyproj.transform

```{code-cell}
p_utm = Proj(crs)
p_latlon=Proj(proj='latlong',datum='WGS84')
ubc_lon = -123.2460
ubc_lat = 49.2606
ubc_x, ubc_y =proj_transform(p_latlon,p_utm,ubc_lon, ubc_lat) 
```

# Locate UBC on the image

Now we need to use the affine transform to go between x,y and 
col, row on the image.  The next cell creates two slice objects that extend 100 pixels on either side of the center point.  The tilde (~) in front of the transform indicates that we're going from x,y to col,row, instead of col,row to x,y.  (See [this blog entry](http://www.perrygeo.com/python-affine-transforms.html) for reference.)

```{code-cell}
ubc_col, ubc_row = ~map_transform*(ubc_x,ubc_y)
ubc_col, ubc_row = int(ubc_col), int(ubc_row)
ubc_col+=2600
ubc_row-=600
x_width=2000
y_height=2000
x_slice=slice(ubc_col-int(x_width/2),ubc_col+ int(x_width/2))
y_slice=slice(ubc_row - int(y_height/2), ubc_row + int(y_height/2))
#pdb.set_trace()
section=b5_refl[x_slice,y_slice]
x_slice,y_slice
hit=section > 0.1
plt.hist(section[hit].flat);
```

# Plot the raw band 5 image in grey, clipped to reflectivities below 0.6

```{raw-cell}
help(ax.imshow)
```

```{code-cell}
vmin=0.0
vmax=0.6
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
palette='gray'
pal = plt.get_cmap(palette)
pal.set_bad('0.75') #75% grey for out-of-map cells
pal.set_over('w')  #color cells > vmax red
pal.set_under('k')  #color cells < vmin black
fig, ax = plt.subplots(1,1,figsize=(15,15))
ax.imshow(section,cmap=pal,norm=the_norm);
```

# Use a rasterio window to write a new tiff file

The [window module](https://rasterio.readthedocs.io/en/latest/topics/windowed-rw.html) has a function that will produce a new affine transform for the subscene.
First we need to add a third dimension to the np.array, because
rasterio expects [band,x,y] for its writer.  Do this with np.newaxis

```{code-cell}
print(section.shape)
out=section[np.newaxis,...]
print(out.shape)
```

# Make the new affine transform

It will have a new upper left hand corner but the same 30 meter pixel size

```{code-cell}
the_win=Window(ubc_col-100,ubc_row-100,200,200)
with rasterio.open(band5) as b5_raster:
    b5_data = b5_raster.read(1,window=the_win)
    win_transform = b5_raster.window_transform(the_win)
```

# Now write this out to small_file.tiff

```{code-cell}
tif_filename=a301.data_dir / Path('small_file.tiff')    
num_chans=1
with rasterio.open(tif_filename,'w',driver='GTiff',
                   height=the_win.height,width=the_win.width,
                   count=num_chans,dtype=section.dtype,
                   crs=crs,transform=win_transform, nodata=0.0) as dst:
        dst.write(out)
        new_profile=dst.profile
        
print(f"section profile: {pprint.pformat(new_profile)}")
```

# Put this on a cartopy map

We need the extent of the image, which we can get by finding
the corners of the section in x,y coordinates from their
row and column

Mark the center with a 'ro' dot using ax.plot  (coastline doesn't seem to be working at the moment)

```{code-cell}
xmin,ymin = win_transform*(0,0)        
xmax,ymax = win_transform*(the_win.width,the_win.height)
```

```{code-cell}
xmin,xmax,ymin,ymax
```

```{code-cell}
cartopy_crs=cartopy.crs.epsg(crs.to_epsg())
xul=meta_dict['CORNER_UL_PROJECTION_X_PRODUCT']
xlr=meta_dict['CORNER_LR_PROJECTION_X_PRODUCT']
ylr=meta_dict['CORNER_LR_PROJECTION_Y_PRODUCT']
yul=meta_dict['CORNER_UL_PROJECTION_Y_PRODUCT']

ubc_lon = -123.2460
ubc_lat = 49.2606
lons=[ubc_lon-0.1,ubc_lon+0.1]
lats=[ubc_lat-0.1,ubc_lat+0.1]
ubc_x, ubc_y =proj_transform(p_latlon,p_utm,ubc_lon, ubc_lat)
xvec,yvec=proj_transform(p_latlon,p_utm,lons, lats) 
#ylr,yul=yvec[0],yvec[1]
#xul,xlr=xvec[0],xvec[1]
fig, ax = plt.subplots(1, 1,figsize=[15,15],
                        subplot_kw={'projection': cartopy_crs})
ax.set_extent([xul, xlr, yul, ylr],crs=cartopy_crs)
ax.imshow(b5_refl, origin='lower', 
          extent=[xul, xlr, yul, ylr], 
          transform=cartopy_crs, 
          interpolation='nearest')

ax.plot((xul+xlr)/2.,(yul + ylr)/2.,
        'ro',markersize=20,transform=cartopy_crs)
ax.coastlines(resolution='10m',color='red',lw=2)
ax.set_extent([xul-1.e4, xlr+1.e4, yul-10.e4, ylr-1.e4],crs=cartopy_crs);
xul,xlr,yul,ylr
```

```{code-cell}
ax.coastlines().get_transform()
```

```{code-cell}
xvec, yvec,ubc_x,ubc_y
xll=xvec[0]
xur=xvec[1]
yul
```

# Higher resolution coastline

+++

Here is what Point Grey looks like with the [open street maps](https://automating-gis-processes.github.io/2017/lessons/L7/retrieve-osm-data.html) coastline database

```{code-cell}
from cartopy.io import shapereader
shape_project=cartopy.crs.PlateCarree()
shp = shapereader.Reader(str(a301.test_dir / 
                             Path("ubc_coastlines/lines.shp")))
fig, ax = plt.subplots(1, 1,figsize=[15,15],
                       subplot_kw={'projection': shape_project})
extent=[-123.3,-123.1,49,49.4]
ax.coastlines()
ax.set_extent(extent)
for record, geometry in zip(shp.records(), shp.geometries()):
    ax.add_geometries([geometry], shape_project, facecolor='w',
                      edgecolor='black')
```

```{code-cell}
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

utm18n = ccrs.UTM(18)
merc = ccrs.Mercator()
left, bottom = 583057.357, 4511050.6293795705
right, top = 588814.059052222, 4516255.36
a = np.random.random((10, 10))

ax = plt.axes(projection=merc)
ax.set_extent((left, right, bottom, top), utm18n)
plt.title('Mercator')

ax.imshow(a, origin='upper', transform=utm18n,
          extent=(left, right, bottom, top), cmap='gray',
          interpolation='nearest')
x = [left, right, right, left, left]
y = [bottom, bottom, top, top, bottom]
ax.coastlines(resolution='10m', linewidth=4, color='red')
ax.gridlines(linewidth=2, color='lightblue', alpha=0.5, linestyle='--')
```

```{code-cell}
fig, ax = plt.subplots(1, 1,figsize=[15,15],
                        subplot_kw={'projection': cartopy_crs})
image_extent=np.array([xul+40.e3, xlr-20.e3, yul-20.e3, ylr+40.e3])
map_extent=image_extent + np.array([-1.,+1.,+1.,-1.])*4.e3
ax.set_extent(map_extent,crs=cartopy_crs)
trial=np.random.random([200,200])

ax.imshow(trial, origin='lower', 
          extent=image_extent, 
          transform=cartopy_crs, 
          interpolation='nearest',alpha=0.3)
ax.plot((xul+xlr)/2.,(yul + ylr)/2.,
        'ro',markersize=20,transform=cartopy_crs)
ax.coastlines(resolution='10m',color='red',lw=2)
ax.set_extent(map_extent,crs=cartopy_crs);
```

```{code-cell}
b5_refl.shape
```
