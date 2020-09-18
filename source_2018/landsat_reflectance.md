---
jupytext:
  cell_metadata_filter: all
  formats: ipynb,py:percent
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

# Radiance and reflectance

```{code-cell} ipython3
import pdb
from pathlib import Path

import numpy as np
from IPython.display import Image
from matplotlib import pyplot as plt
from PIL import Image as pil_image
from PIL.TiffTags import TAGS
from skimage import data
from skimage import exposure
from skimage import img_as_float
import context

import a301
from a301.landsat.landsat_metadata import landsat_metadata
from a301.landsat.toa_radiance import toa_radiance_457
from a301.landsat.toa_radiance import toa_radiance_8
from a301.landsat.toa_reflectance import toa_reflectance_457
from a301.landsat.toa_reflectance import toa_reflectance_8
# import rasterio
band = 7
june_2015 = a301.test_dir / Path("landsat8/LC80470262015165LGN02")
may_2015 = a301.test_dir / Path("landsat_2018_05_13")
data_dir = may_2015
data_dir = june_2015
data_dir = Path.home() / "repos/a448/data/Directed Study - Burn Severity/scene"
tiff_file = list(data_dir.glob(f"*B{band}.TIF"))[0]
meta_file = list(data_dir.glob("*MTL.txt"))[0]
meta_data = landsat_metadata(meta_file)
rad_dict = {"LANDSAT_7": toa_radiance_457, "LANDSAT_8": toa_radiance_8}
refl_dict = {"LANDSAT_7": toa_reflectance_457, "LANDSAT_8": toa_reflectance_8}
satellite = meta_data.SPACECRAFT_ID
rad_fun = rad_dict[satellite]
refl_fun = refl_dict[satellite]
print(f"calculated reflectivity for {tiff_file}")
```

```{code-cell} ipython3
%matplotlib inline
np.seterr(divide="ignore", invalid="ignore")
refl = refl_fun([band], meta_file)
print(list(refl.keys()))
hit1 = ~np.isnan(refl[band])
hit2 = refl[band] > 1.5e-1
hit = np.logical_and(hit1, hit2)
plt.hist(refl[band][hit].ravel())
plt.title(f"band {band} reflectance")
```

```{code-cell} ipython3
rad = rad_fun([band], meta_file)
hit1 = ~np.isnan(rad[band])
hit2 = rad[band] > 1.5e-1
hit = np.logical_and(hit1, hit2)
plt.hist(rad[band][hit].ravel())
plt.title(f"band {band} radiance W/m^2/micron/sr")
```
