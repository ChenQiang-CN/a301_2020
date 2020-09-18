---
jupytext:
  formats: ipynb,py:percent
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
<div class="toc"><ul class="toc-item"><li><span><a href="#Another-introduction" data-toc-modified-id="Another-introduction-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Another introduction</a></span></li><li><span><a href="#Introduction" data-toc-modified-id="Introduction-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Introduction</a></span></li><li><span><a href="#Get-bands-3,-4,-5-fullsize-(green,-red,-near-ir)" data-toc-modified-id="Get-bands-3,-4,-5-fullsize-(green,-red,-near-ir)-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Get bands 3, 4, 5 fullsize (green, red, near-ir)</a></span></li><li><span><a href="#This-cell-reads-in-your-affine-transform,-metadata-and-profile" data-toc-modified-id="This-cell-reads-in-your-affine-transform,-metadata-and-profile-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>This cell reads in your affine transform, metadata and profile</a></span></li><li><span><a href="#This-cell-gets-the-right-reflection-function-for-your-satellite" data-toc-modified-id="This-cell-gets-the-right-reflection-function-for-your-satellite-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>This cell gets the right reflection function for your satellite</a></span></li><li><span><a href="#Define-a-subscene-window-and-a-transform" data-toc-modified-id="Define-a-subscene-window-and-a-transform-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Define a subscene window and a transform</a></span></li><li><span><a href="#Read-only-the-window-pixels-from-the-band-3,-4,-5-files" data-toc-modified-id="Read-only-the-window-pixels-from-the-band-3,-4,-5-files-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>Read only the window pixels from the band 3, 4, 5 files</a></span></li><li><span><a href="#In-the-next-cell-calculate-your-ndvi" data-toc-modified-id="In-the-next-cell-calculate-your-ndvi-8"><span class="toc-item-num">8&nbsp;&nbsp;</span>In the next cell calculate your ndvi</a></span></li><li><span><a href="#In-the-next-cell-plot-a-mapped-ndvi-image-with-a-red-dot-in-your-ul-corner-and-a-white-dot-in-your-lr-corner" data-toc-modified-id="In-the-next-cell-plot-a-mapped-ndvi-image-with-a-red-dot-in-your-ul-corner-and-a-white-dot-in-your-lr-corner-9"><span class="toc-item-num">9&nbsp;&nbsp;</span>In the next cell plot a mapped ndvi image with a red dot in your ul corner and a white dot in your lr corner</a></span></li></ul></div>

+++ {"nbgrader": {"grade": false, "grade_id": "cell-f686910c4b34f225", "locked": true, "schema_version": 1, "solution": false}}

# Introduction

There are 4 cells that ask for changes below, the rest should run as long as you
use the variable names I ask for in the questions.

```{code-cell}
---
nbgrader:
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
import pprint
from a301.utils.data_read import download
from pathlib import Path
from affine import Affine
from IPython.display import Image
from a301.landsat.toa_reflectance import calc_refl_457, calc_reflc_8
from a301.landsat.toa_radiance import calc_radiance_457, calc_radiance_8
from a301.radiation import planck_invert
```

+++ {"nbgrader": {"grade": false, "grade_id": "cell-b700b41e2d83fe79", "locked": true, "schema_version": 1, "solution": false}}

# Get bands 3, 4, 5 fullsize (green, red, near-ir)

At the end of this cell you shiould have the following path objects for your spring scene:

meta_bigfile, band3_bigfile, band4_bigfile, band5_bigfile

that point to your landsat TIF and mtl.txt files.

Note that landsat7 and landsat8 have their bands in different orders:

https://www.esri.com/arcgis-blog/products/product/imagery/band-combinations-for-landsat-8/

To deal switch between landsat8 and landsat7, set the landsat8 flag to True/False respectively


```{code-cell}
---
nbgrader:
  grade: true
  grade_id: cell-8d3705a4a6fbb7bc
  locked: false
  points: 5
  schema_version: 1
  solution: true
---
### BEGIN SOLUTION
landsat8=False
file_dict={}
file_dict['spring']=dict()
file_dict['fall']=dict()
if landsat8:
    landsat_band_dict={'red':4,'green':3,'blue':2,'nearir':5,'thermal':10}
    file_dict['spring']['root']="LC08_L1TP_047026_20150614_20180131_01_T1_"
    file_dict['spring']['prefix_remote']=Path('landsat_scenes/l8_vancouver/spring')
    file_dict['spring']['prefix_local']=Path("landsat8/vancouver/spring")
    file_dict['fall']['root']="LC08_L1TP_047026_20140203_20170307_01_T1_"
    file_dict['fall']['prefix_remote']=Path('landsat_scenes/l8_vancouver/fall')
    file_dict['fall']['prefix_local']=Path("landsat8/vancouver/fall")        
else:
    landsat_band_dict={'red':3,'green':2,'blue':1,'nearir':4,'thermal':'6_VCID_1'}
    file_dict['spring']['root']="LE07_L1TP_047026_20180513_20180610_01_T1_"
    file_dict['spring']['prefix_remote']=Path('landsat_scenes/l7_vancouver/spring')
    file_dict['spring']['prefix_local']=Path("landsat7/vancouver/spring")
    file_dict['fall']['root']="LE07_L1TP_047026_20141110_20160904_01_T1_"
    file_dict['fall']['prefix_remote']=Path('landsat_scenes/l7_vancouver/fall')
    file_dict['fall']['prefix_local']=Path("landsat7/vancouver/fall")

    
dest_folder=a301.data_dir / prefix_local
dest_folder.mkdir(parents=True, exist_ok=True)

for season in ['fall','spring']:
    season_dict=file_dict['key']
    root=season_dict['root']
    name_dict=dict()
    the_file = Path(f"{root}MTL.txt")
    mtl_file=prefix_remote / the_file
    download(str(mtl_file),dest_folder=dest_folder)
    name_dict['mtl']= str(a301.data_dir / prefix_local / the_file)
    for key,band_num in landsat_band_dict.items():
        name_dict[key]=f"{root}B{band_num}.TIF"
    season_dict['filenames']=name_dict
    for key, the_file in name_dict.items():
        landsat_tif = season_dict['prefix_remote'] / Path(the_file)
        download(str(landsat_tif),dest_folder=dest_folder)
        name_dict[key]= str(a301.data_dir / prefix_local / the_file)
### END SOLUTION
```

```{code-cell}
name_dict
```

```{code-cell}
name_dict
```

+++ {"nbgrader": {"grade": false, "grade_id": "cell-dd09edb695c92076", "locked": true, "schema_version": 1, "solution": false}}

# This cell reads in your affine transform, metadata and profile

Using red band file for transform/profile information (arbitrary)

```{code-cell}
---
nbgrader:
  grade: false
  grade_id: cell-daebc17375c70921
  locked: true
  schema_version: 1
  solution: false
---
metadata=landsat_metadata(name_dict['mtl'])
with rasterio.open(name_dict['red']) as raster:
    big_transform=raster.transform
    big_profile=raster.profile

zone = metadata.UTM_ZONE  
crs = cartopy.crs.UTM(zone, southern_hemisphere=False)
p_utm=Proj(crs.proj4_init)
p_lonlat=Proj(proj='latlong',datum='WGS84')
```

```{code-cell}
metadata.__dict__['SPACECRAFT_ID']
```

+++ {"nbgrader": {"grade": false, "grade_id": "cell-cef7282b3b40dd6f", "locked": true, "schema_version": 1, "solution": false}}

# This cell gets the right reflection function for your satellite

```{code-cell}
---
nbgrader:
  grade: false
  grade_id: cell-df3ceb3d365ce669
  locked: true
  schema_version: 1
  solution: false
---
refl_dict={'LANDSAT_7':calc_refl_457,'LANDSAT_8':calc_reflc_8}     
radiance_dict={'LANDSAT_7':calc_radiance_457,'LANDSAT_8':calc_radiance_8}  
satellite=metadata.SPACECRAFT_ID
refl_fun=refl_dict[satellite]
radiance_fun=radiance_dict[satellite]
```

```{code-cell}

```

+++ {"nbgrader": {"grade": false, "grade_id": "cell-175a34f2bd5cec2f", "locked": true, "schema_version": 1, "solution": false}}

# Define a subscene window and a transform

In the cell below, get the upper left col,row (ul_col,ul_row) and upper left and lower
right x,y (ul_x,ul_y,lr_x,lr_y)
coordinates the upper left corner of 
your subscene as in the image_zoom notebook.  Use ul_col, ul_row, ul_x, ul_y plus your subscene
width and height to make a rasterio window and new transform.

    window=Window(ul_col, ul_row, small_width, small_height)
    new_affine=Affine(30.,0.,ul_x,0.,-30.,ul_y)
    extent = [ul_x,lr_x,lr_y,ul_y]

```{code-cell}
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
ubc_x, ubc_y =proj_transform(p_lonlat,p_utm,ubc_lon, ubc_lat) 
ubc_col, ubc_row = ~big_transform*(ubc_x,ubc_y)
ubc_col, ubc_row = int(ubc_col), int(ubc_row)
l_col_offset= -100
t_row_offset= -100
width=200
height=200
ul_col=ubc_col + l_col_offset
ul_row=ubc_row + t_row_offset
ul_x,ul_y = big_transform*(ul_col,ul_row)
lr_x,lr_y = big_transform*(ul_col + width, ul_row + height)
small_window=Window(ul_col, ul_row, width, height)
new_affine=Affine(30.,0.,ul_x,0.,-30.,ul_y)
extent = [ul_x,lr_x,lr_y,ul_y]
### END SOLUTION
```

+++ {"nbgrader": {"grade": false, "grade_id": "cell-cd9770b2c44fe58c", "locked": true, "schema_version": 1, "solution": false}}

# Read only the window pixels from the band 3, 4, 5 files

```{code-cell}
---
nbgrader:
  grade: false
  grade_id: cell-3b8481e8992f8a6a
  locked: true
  schema_version: 1
  solution: false
---
metadata_string=str(name_dict['mtl'])
refl_dict=dict()
for key in ['red','green','blue','nearir']:
    filepath=name_dict[key]
    bandnum=landsat_band_dict[key]
    with rasterio.open(filepath) as src:
        counts = src.read(1, window=small_window)
        counts=counts.astype(np.float32)
        counts[counts==0.]=np.nan
        #counts = src.read(1)
        refl_vals = refl_fun(counts,bandnum,metadata_string)
        refl_dict[key]=refl_vals
        
key='thermal'        
filepath=name_dict[key]
bandnum=landsat_band_dict[key]
with rasterio.open(filepath) as src:
    counts = src.read(1, window=small_window)
    counts=counts.astype(np.float32)
    counts[counts==0.]=np.nan
    #counts = src.read(1)
    thermal_rad = radiance_fun(counts,bandnum,metadata_string)

metadata=landsat_metadata(name_dict['mtl'])
plt.hist(thermal_rad[~np.isnan(thermal_rad)].flat);
```

```{code-cell}
plt.imshow(refl_dict['nearir'])
```

+++ {"nbgrader": {"grade": false, "grade_id": "cell-f4c6415f2226afe9", "locked": true, "schema_version": 1, "solution": false}}

# In the next cell calculate your ndvi

Save it in a variable called ndvi

```{code-cell}
---
nbgrader:
  grade: true
  grade_id: cell-6589d24a5ba25504
  locked: false
  points: 2
  schema_version: 1
  solution: true
---
### BEGIN SOLUTION
ndvi = (refl_dict['nearir'] - refl_dict['red'])/(refl_dict['nearir'] + refl_dict['red'])
### END SOLUTION
```

```{code-cell}
plt.hist(ndvi[~np.isnan(ndvi)].flat);
```

```{code-cell}
---
nbgrader:
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

+++ {"nbgrader": {"grade": false, "grade_id": "cell-b68f0e3d1ae9ea4d", "locked": true, "schema_version": 1, "solution": false}}

# In the next cell plot a mapped ndvi image with a red dot in your ul corner and a white dot in your lr corner

Adjust this plot to fit your image.  Just delete the bottom line and work with the provided commands

```{code-cell}
---
nbgrader:
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
### BEGIN SOLUTION
#your plot should appear below
### END SOLUTION
print('through cell IV --- xxxx  -- try this -- hello what the heak -- hello')
print('and finally II lslsls')
```

```{code-cell}
with rasterio.open(name_dict['thermal']) as raster:
    thermal_transform=raster.transform

btemp=planck_invert(10.e-6,thermal_rad*1.e6)
vmin=260.
vmax=300.
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
palette='viridis'
pal = plt.get_cmap(palette)
pal.set_bad('0.75') #75% grey for out-of-map cells
pal.set_over('w')  #color cells > vmax red
pal.set_under('k')  #color cells < vmin black
fig, ax = plt.subplots(1, 1,figsize=[10,15],
                       subplot_kw={'projection': crs})
col=ax.imshow(btemp,origin="upper",
         extent=extent,transform=crs)
ax.plot(ul_x,ul_y,'ro',markersize=50)
ax.plot(lr_x,lr_y,'wo',markersize=50)
ax.set(title="spring ndvi")
cbar_ax = fig.add_axes([0.95, 0.2, 0.05, 0.6])
cbar=ax.figure.colorbar(col,extend='both',cax=cbar_ax,orientation='vertical')
cbar.set_label('ndvi index')
### BEGIN SOLUTION
#your plot should appear below
### END SOLUTION
thermal_transform
name_dict['thermal']
thermal_transform
```
