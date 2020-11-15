# ---
# jupyter:
#   jupytext:
#     notebook_metadata_filter: all,-language_info,-toc,-latex_envs
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Introduction
#
# There are 4 cells that ask for changes below, the rest should run as long as you
# use the variable names I ask for in the questions.

# %%
import rasterio
import a301_lib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from sat_lib.landsat.landsat_metadata import landsat_metadata
import cartopy
from rasterio.windows import Window
from pyproj import Proj
from sat_lib.landsat.toa_reflectance import calc_reflc_8
import pprint
from pathlib import Path
from affine import Affine
from IPython.display import Image
import copy
import datetime

# %%
str(datetime.date.today())

# %% [markdown]
# # Get bands 3, 4, 5 fullsize (green, red, near-ir)
#
# At the end of this cell you shiould have the following path objects for your spring scene:
#
# meta_bigfile, band3_bigfile, band4_bigfile, band5_bigfile
#
# that point to your landsat TIF and mtl.txt files.

# %%
notebook_dir=Path().resolve().parent
print(notebook_dir)

# %% deletable=false nbgrader={"checksum": "bd530dfcc0915ef07f406d66a6e9ab19", "grade": true, "grade_id": "cell-8d3705a4a6fbb7bc", "locked": false, "points": 5, "schema_version": 1, "solution": true}
landsat_dir = notebook_dir / "week9/landsat_scenes"
print(landsat_dir)
band3_bigfile = list(landsat_dir.glob("**/*B3.TIF"))[0]
band4_bigfile = list(landsat_dir.glob("**/*B4.TIF"))[0]
band5_bigfile = list(landsat_dir.glob("**/*B5.TIF"))[0]
mtl_file = list(landsat_dir.glob("**/*MTL.txt"))[0]

# %% [markdown]
# # This cell reads in your affine transform, metadata and profile
#
# Using band4_bigfile (arbitrary)

# %%
metadata=landsat_metadata(mtl_file)
with rasterio.open(band4_bigfile) as raster:
    big_transform=raster.transform
    big_profile=raster.profile

utm_code = big_profile['crs'].to_epsg()
crs = cartopy.crs.epsg(utm_code)
p_utm=Proj(crs.proj4_init)
p_lonlat=Proj(proj='latlong',datum='WGS84')
print(big_profile)

# %%
print(big_transform)

# %% [markdown]
# ## Read the scene corners we want from the image_zoom tiff

# %%
week10_scene = notebook_dir / "week10/small_file.tiff"
with rasterio.open(week10_scene) as raster:
    small_transform=raster.transform
    small_profile=raster.profile
print(small_transform)

# %%
print(small_profile)

# %% [markdown]
# How do we find this small rectangle on the band4_bigfile raster?
#
# We know the UTM zone 10 coordinates of the upper left corner, so we just need the row
# and column for that on the big raster.

# %%
ul_x, ul_y = small_transform*(0,0)
print(f"{ul_x=},{ul_y=:5.21}")

# %%
ul_col, ul_row = ~big_transform*(ul_x,ul_y)
print(f"{ul_col=}, {ul_row=}")
small_width = small_profile['width']
small_height = small_profile['height']
print(f"{small_width=},{small_height=}")

# %%
small_window=Window(ul_col, ul_row, small_width, small_height)

# %%
lr_x, lr_y = small_transform*(small_width,-small_height)
print(f"{lr_x=},{lr_y=}")

# %% [markdown]
# # Define a subscene window and a transform
#
# In the cell below, get the upper left col,row (ul_col,ul_row) and upper left and lower
# right x,y (ul_x,ul_y,lr_x,lr_y)
# coordinates the upper left corner of
# your subscene as in the image_zoom notebook.  Use ul_col, ul_row, ul_x, ul_y plus your subscene
# width and height to make a rasterio window and new transform.
#
#     window=Window(ul_col, ul_row, small_width, small_height)
#     new_affine=Affine(30.,0.,ul_x,0.,-30.,ul_y)
#     extent = [ul_x,lr_x,lr_y,ul_y]
#
#
# # Read only the window pixels from the band 3, 4, 5 files

# %%
refl_dict=dict()
for bandnum,filepath in zip([3,4,5],[band3_bigfile,band4_bigfile,band5_bigfile]):
    with rasterio.open(filepath) as src:
        counts = src.read(1, window=small_window)
        refl_vals = calc_reflc_8(counts,bandnum,metadata)
        refl_dict[bandnum]=refl_vals
print(f"{refl_dict[4].shape=}")

# %% [markdown]
# ## In the next cell calculate your ndvi

# %%
ndvi = (refl_dict[5]-refl_dict[4])/(refl_dict[5]+refl_dict[4])
print(f"{ndvi.shape=}")

# %%
#Save it in a variable called ndvi
plt.hist(ndvi[~np.isnan(ndvi)].flat);
plt.title('spring ndvi')
plt.savefig('spring_ndvi.png')

# %% [markdown]
# * In the next cell plot a mapped ndvi image with a red dot in your ul corner and a white dot in your lr corner
#
# Adjust this plot to fit your image.  Just delete the bottom line and work with the provided commands

# %%
vmin=0.0
vmax=0.8
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
palette='viridis'
pal = copy.copy(plt.get_cmap(palette))
pal.set_bad('0.75') #75% grey for out-of-map cells
pal.set_over('w')  #color cells > vmax red
pal.set_under('k')  #color cells < vmin black
fig, ax = plt.subplots(1, 1,figsize=[10,15],
                       subplot_kw={'projection': crs})
extent = [ul_x,lr_x,lr_y,ul_y]
col=ax.imshow(ndvi,origin="upper",
         extent=extent,transform=crs)
ax.plot(ul_x,ul_y,'ro',markersize=50)
ax.plot(lr_x,lr_y,'wo',markersize=50)
ax.set(title="spring ndvi")
cbar_ax = fig.add_axes([0.95, 0.2, 0.05, 0.6])
cbar=ax.figure.colorbar(col,extend='both',cax=cbar_ax,orientation='vertical')
cbar.set_label('ndvi index')

# %% [markdown]
# ## write out the bands 3, 4, 5 as a new geotiff

# %%
week10_dir = notebook_dir / "week10"
b3, b4, b5 = refl_dict[3], refl_dict[4], refl_dict[5]
channels = np.empty([3, b3.shape[0], b4.shape[1]],dtype=b4.dtype)
tif_filename = week10_dir / "vancouver_345_refl.tiff"
num_chans, height, width = channels.shape

for index, image in enumerate([b3, b4, b5]):
    channels[index, :, :] = image[...]

with rasterio.open(
    tif_filename,
    "w",
    driver="GTiff",
    height=height,
    width=width,
    count=num_chans,
    dtype=channels.dtype,
    crs=big_profile['crs'],
    transform=small_transform,
    nodata= -9999.,
) as dst:
    dst.write(channels)
    chan_tags = ["LC8_Band3_toa_refl", "LC8_Band4_toa_refl", "LC8_Band5_toa_refl"]
    dst.update_tags(band3_file=band3_bigfile.name,
                    band4_file=band4_bigfile.name,
                    band5_file=band5_bigfile.name,
                    history = "written by ndvi_rasterio.md",
                    written_on = str(datetime.date.today())
                    )
    for index, chan_name in enumerate(chan_tags):
        dst.update_tags(index + 1, name=chan_name)
        dst.update_tags(index + 1, valid_range="0,1")

# %%
with rasterio.open(tif_filename) as raster:
    transform=raster.transform
    profile=raster.profile
print(f"{profile=}")
print(f"{transform=}")
