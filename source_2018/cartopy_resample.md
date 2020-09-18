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
<div class="toc"><ul class="toc-item"><li><span><a href="#Use-pyresample-to-make-a-projected-image" data-toc-modified-id="Use-pyresample-to-make-a-projected-image-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Use pyresample to make a projected image</a></span></li><li><span><a href="#Read-the-lons/lats-from-the-MYD03-file" data-toc-modified-id="Read-the-lons/lats-from-the-MYD03-file-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Read the lons/lats from the MYD03 file</a></span></li><li><span><a href="#get-the-map-projection-from-corners.json" data-toc-modified-id="get-the-map-projection-from-corners.json-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>get the map projection from corners.json</a></span></li><li><span><a href="#Use-pyresample-to-define-a-new-grid-in-this-projection" data-toc-modified-id="Use-pyresample-to-define-a-new-grid-in-this-projection-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Use pyresample to define a new grid in this projection</a></span></li><li><span><a href="#resample-the-longitudes-on-this-grid" data-toc-modified-id="resample-the-longitudes-on-this-grid-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>resample the longitudes on this grid</a></span></li><li><span><a href="#replace-missing-values-with-floating-point-nan" data-toc-modified-id="replace-missing-values-with-floating-point-nan-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>replace missing values with floating point nan</a></span></li><li><span><a href="#Plot-the-image-using-cartopy" data-toc-modified-id="Plot-the-image-using-cartopy-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>Plot the image using cartopy</a></span></li></ul></div>

+++

# Use pyresample to make a projected image

In the cartopy_mapping_pyproj notebook we stored projection
coords in a json file called corners.json.  This notebook
reads that information back in to plot lats/lons on a map

```{code-cell}
import json
import pprint
import shutil

import cartopy
from pyhdf.SD import SD
from pyhdf.SD import SDC
from pyresample import kd_tree

import a301
from a301.utils.data_read import download

read_data = False
if read_data:
    filename_M3 = "MYD03.A2013222.2105.006.2013223155808.hdf"
    download(filename_M3)
    for filename in [filename_M3, filename_M2]:
        local_file = Path.cwd() / Path(filename)
        to_file = a301.data_dir / Path(filename)
        print(f"copy {local_file} to {to_file}")
        shutil.copy(local_file, to_file)
```

```{code-cell}
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy
from pathlib import Path
import pprint
import numpy as np
import pdb

#
```

# Read the lons/lats from the MYD03 file

**substitute your filename**

```{code-cell}
# Read the lats and lons from the MYD03 file
filename_M3 = "MYD03.A2013222.2105.006.2013223155808.hdf"
m3_path = a301.data_dir / Path(filename_M3)
print(f"reading {m3_path}")
m3_file = SD(str(m3_path), SDC.READ)
lats = m3_file.select("Latitude").get()
lons = m3_file.select("Longitude").get()
```

# get the map projection from corners.json

Get the map  projection and extent from corners.json

```{code-cell}
json_file = a301.data_dir / Path("corners.json")
with open(json_file, "r") as f:
    map_dict = json.load(f)
pprint.pprint(map_dict)
```

# Use pyresample to define a new grid in this projection

```{code-cell}
from pyresample import load_area, save_quicklook, SwathDefinition

proj_params = map_dict["proj4_params"]
swath_def = SwathDefinition(lons, lats)
area_def = swath_def.compute_optimal_bb_area(proj_dict=proj_params)
```

```{code-cell}
dir(area_def)
```

# resample the longitudes on this grid

```{code-cell}
fill_value = -9999.0
area_name = "modis swath 5min granule"
image_lons = kd_tree.resample_nearest(
    swath_def,
    lons.ravel(),
    area_def,
    radius_of_influence=5000,
    nprocs=2,
    fill_value=fill_value,
)
print(f"\ndump area definition:\n{area_def}\n")
print(
    (
        f"\nx and y pixel dimensions in meters:"
        f"\n{area_def.pixel_size_x}\n{area_def.pixel_size_y}\n"
    )
)
```

# replace missing values with floating point nan

```{code-cell}
nan_value = np.array([np.nan], dtype=np.float32)[0]
image_lons[image_lons < -9000] = nan_value
```

# Plot the image using cartopy

```{code-cell}
crs = area_def.to_cartopy_crs()
ax = plt.axes(projection=crs)
ax.coastlines()
ax.set_global()
plt.imshow(image_lons, transform=crs, extent=crs.bounds, origin="upper")
plt.colorbar()
```

```{code-cell}
crs.globe.to_proj4_params()
```

```{code-cell}

```

```{code-cell}

```
