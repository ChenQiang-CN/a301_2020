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
<div class="toc"><ul class="toc-item"><li><span><a href="#Introduction" data-toc-modified-id="Introduction-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Introduction</a></span></li><li><span><a href="#Get-the-vancouver-image" data-toc-modified-id="Get-the-vancouver-image-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Get the vancouver image</a></span></li><li><span><a href="#Read-in-the-bands-2-(blue),-3-(green)-and-4-(red)" data-toc-modified-id="Read-in-the-bands-2-(blue),-3-(green)-and-4-(red)-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Read in the bands 2 (blue), 3 (green) and 4 (red)</a></span><ul class="toc-item"><li><span><a href="#The-profile-for-this-image" data-toc-modified-id="The-profile-for-this-image-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>The profile for this image</a></span></li></ul></li><li><span><a href="#Create--new-3-dimensional-array-and-copy-the-bands" data-toc-modified-id="Create--new-3-dimensional-array-and-copy-the-bands-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Create  new 3-dimensional array and copy the bands</a></span></li><li><span><a href="#Stretch-and-write-out-the-combined-image" data-toc-modified-id="Stretch-and-write-out-the-combined-image-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Stretch and write out the combined image</a></span></li><li><span><a href="#Write-out-the-geotiff-file" data-toc-modified-id="Write-out-the-geotiff-file-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Write out the geotiff file</a></span></li><li><span><a href="#Read-the-geotiff-file-and-convert-to-png-and-jpeg" data-toc-modified-id="Read-the-geotiff-file-and-convert-to-png-and-jpeg-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>Read the geotiff file and convert to png and jpeg</a></span></li><li><span><a href="#Display-the-jpeg-file" data-toc-modified-id="Display-the-jpeg-file-8"><span class="toc-item-num">8&nbsp;&nbsp;</span>Display the jpeg file</a></span></li><li><span><a href="#Compare-with-the-glovis-&quot;natural-color&quot;-image" data-toc-modified-id="Compare-with-the-glovis-&quot;natural-color&quot;-image-9"><span class="toc-item-num">9&nbsp;&nbsp;</span>Compare with the glovis "natural color" image</a></span></li></ul></div>

+++

# Introduction

This notebook reads in the red, blue and green bands from a landsat 8 image
and uses [rasterio](https://rasterio.readthedocs.io/en/latest/index.html) to write
out new 3-channel color tiff, jpeg and png files

```{code-cell}
import pprint
from pathlib import Path

import numpy as np
import rasterio

import a301
from a301.utils.data_read import download
```

# Get the vancouver image

```{code-cell}

filenames = [
    "LC08_L1TP_047026_20150614_20180131_01_T1_B2.TIF",
    "LC08_L1TP_047026_20150614_20180131_01_T1_B3.TIF",
    "LC08_L1TP_047026_20150614_20180131_01_T1_B4.TIF",
    "LC08_L1TP_047026_20150614_20180131_01_T1_MTL.txt",
]
dest_folder = a301.data_dir / Path("landsat8/vancouver")
```

```{code-cell}
for the_file in filenames:
    landsat_tif = Path("landsat_scenes/l8_vancouver") / Path(the_file)
    download(str(landsat_tif), dest_folder=dest_folder)
band2 = list(dest_folder.glob("*_B2.TIF"))[0]
band3 = list(dest_folder.glob("*_B3.TIF"))[0]
band4 = list(dest_folder.glob("*_B4.TIF"))[0]
```

# Read in the bands 2 (blue), 3 (green) and 4 (red)

Note that rasterio is a pretty complicated object with a lot of functionality.

The full documentation is at https://rasterio.readthedocs.io/en/latest/

Save the image profile, coordinate reference system (crs) and affine transform for inspection -- these will be the same for every band in the image

```{code-cell}
with rasterio.open(band2) as b2_raster:
    b2_data = b2_raster.read(1)
    transform = b2_raster.transform
    crs = b2_raster.crs
    profile = b2_raster.profile
with rasterio.open(band3) as b3_raster:
    b3_data = b3_raster.read(1)
with rasterio.open(band4) as b4_raster:
    b4_data = b4_raster.read(1)
```

## The profile for this image

```{code-cell}
print(f"\nprofile: {pprint.pformat(profile)}\n")
```

# Create  new 3-dimensional array and copy the bands

+++

Make an empty 3-d array to hold the three channels.  We are going to scale
each band to the range 0-255 so specify 8 bit np.uint8 words

```{code-cell}
channels = np.empty([3, b2_data.shape[0], b2_data.shape[1]], dtype=np.uint8)
```

# Stretch and write out the combined image

+++

Do a histogram stretch on each band using skimage.exposure and save it
into the 3-d array.

```{code-cell}
from skimage import img_as_ubyte
from skimage import exposure

for index, image in enumerate([b4_data, b3_data, b2_data]):
    stretched = exposure.equalize_hist(image)
    channels[index, :, :] = img_as_ubyte(stretched)
```

# Write out the geotiff file

```{code-cell}
tif_filename = dest_folder / Path("vancouver_432.tiff")
num_chans, height, width = channels.shape
with rasterio.open(
    tif_filename,
    "w",
    driver="GTiff",
    height=height,
    width=width,
    count=num_chans,
    dtype=channels.dtype,
    crs=crs,
    transform=transform,
    nodata=0.0,
) as dst:
    dst.write(channels)
    keys = ["4", "3", "2"]
    for index, chan_name in enumerate(keys):
        dst.update_tags(index + 1, name=chan_name)
```

# Read the geotiff file and convert to png and jpeg

```{code-cell}
with rasterio.open(tif_filename) as infile:
    print(f"\nnew profile: {pprint.pformat(infile.profile)}\n")
    profile = infile.profile
    #
    # change the driver name from GTiff to PNG
    #
    profile["driver"] = "PNG"
    #
    # pathlib makes it easy to add a new suffix to a
    # filename
    #
    png_filename = tif_filename.with_suffix(".png")
    raster = infile.read()
    with rasterio.open(png_filename, "w", **profile) as dst:
        dst.write(raster)
    #
    # now do jpeg
    #
    profile["driver"] = "JPEG"
    jpeg_filename = tif_filename.with_suffix(".jpeg")
    with rasterio.open(jpeg_filename, "w", **profile) as dst:
        dst.write(raster)
```

# Display the jpeg file

```{code-cell}
from IPython.display import Image

Image(str(jpeg_filename))
```

# Compare with the glovis "natural color" image

Question:  Why do these two images look so different?

```{code-cell}
glovis = a301.test_dir / Path("glovis_vancouver.png")
Image(str(glovis))
```

```{code-cell}

```
