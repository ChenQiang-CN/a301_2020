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
<div class="toc"><ul class="toc-item"><li><span><a href="#Introduction" data-toc-modified-id="Introduction-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Introduction</a></span></li><li><span><a href="#Setup" data-toc-modified-id="Setup-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Setup</a></span></li><li><span><a href="#Read-in-the-5-km-nearir-and-ir-water-vapor-images" data-toc-modified-id="Read-in-the-5-km-nearir-and-ir-water-vapor-images-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Read in the 5 km nearir and ir water vapor images</a></span><ul class="toc-item"><li><ul class="toc-item"><li><span><a href="#Here-is-wv_ir" data-toc-modified-id="Here-is-wv_ir-3.0.1"><span class="toc-item-num">3.0.1&nbsp;&nbsp;</span>Here is wv_ir</a></span></li><li><span><a href="#Here-is-wv_nearir_ir-mapped-to-the-low-resolution-area_def" data-toc-modified-id="Here-is-wv_nearir_ir-mapped-to-the-low-resolution-area_def-3.0.2"><span class="toc-item-num">3.0.2&nbsp;&nbsp;</span>Here is wv_nearir_ir mapped to the low resolution area_def</a></span></li></ul></li></ul></li><li><span><a href="#Questions" data-toc-modified-id="Questions-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Questions</a></span><ul class="toc-item"><li><span><a href="#Question-9.1" data-toc-modified-id="Question-9.1-4.1"><span class="toc-item-num">4.1&nbsp;&nbsp;</span>Question 9.1</a></span></li><li><span><a href="#Question-9.2" data-toc-modified-id="Question-9.2-4.2"><span class="toc-item-num">4.2&nbsp;&nbsp;</span>Question 9.2</a></span><ul class="toc-item"><li><span><a href="#Here-is-the-test-that-autograder-will-run" data-toc-modified-id="Here-is-the-test-that-autograder-will-run-4.2.1"><span class="toc-item-num">4.2.1&nbsp;&nbsp;</span>Here is the test that autograder will run</a></span></li></ul></li></ul></li></ul></div>

+++

# Introduction

This assignment uses the functions and files defined in level2_cartopy_plot to look
at the difference between wv_ir and wv_nearir mapped onto the low resolution
grid.

# Setup

1. Understand  and run level2_cartopy_plot

1. Setup should be the same, rerun test to check

```
      python -m a301.install_tests.assign8_test
```

```{code-cell}
import json
import pdb
import pprint
from pathlib import Path

import numpy as np
from IPython.display import display
from IPython.display import Image
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from pyhdf.SD import SD
from pyhdf.SD import SDC
from pyresample import geometry

import a301
from a301.geometry import area_def_from_dict
from a301.geometry import get_image
from a301.geometry import plot_image
from a301.scripts.modismeta_read import parseMeta
# Image('figures/MYBRGB.A2016224.2100.006.2016237025650.jpg',width=600)
```

```{code-cell}
%matplotlib inline
```

# Read in the 5 km nearir and ir water vapor images


use get_image and plot_image from the library

+++

### Here is wv_ir

```{code-cell}
foldername = a301.map_dir / Path("wv_maps")
image_wv_ir, area_def_lr = get_image(foldername, "wv_ir")
```

```{code-cell}
fig, ax = plot_image(image_wv_ir, area_def_lr)
ax.set_title("5 km IR water vapor (cm)")
```

### Here is wv_nearir_ir mapped to the low resolution area_def

```{code-cell}
image_wv_nearir_lr, area_def_hr = get_image(foldername, "wv_nearir_lr")
fig, ax = plot_image(image_wv_nearir_lr, area_def_hr)
ax.set_title("1 km IR water vapor (cm) at 5k low resolution (lr)")
print(image_wv_nearir_lr.shape)
```

# Questions

+++

## Question 9.1

in the cell below calculate the difference between the nearir_ir and wv_ir
images as a new variable called wv_difference and plot
it using plot_image

Use a diverging palette like RdYlBu (see [matplotlib palettes](https://matplotlib.org/tutorials/colors/colormaps.html))
to highlight the areas where the difference is zero and show postiive and negative departures.
Set your vmin, vmax to -1, 1  cm.

```{code-cell}
---
nbgrader:
  grade: true
  grade_id: cell-5b1d6dc0e1f43e2e
  locked: false
  points: 2
  schema_version: 2
  solution: true
---
wv_difference = image_wv_nearir_lr - image_wv_ir
### BEGIN SOLUTION
pal = plt.get_cmap("RdYlBu").reversed()
fig, ax = plot_image(wv_difference, area_def_lr, vmin=-1, vmax=+1, palette=pal)
ax.set_title("1km - 5km wv (cm)")
### END SOLUTION
```

## Question 9.2

Write out your wv_difference image and using dump_image

```{code-cell}
---
nbgrader:
  grade: false
  grade_id: cell-522681e6dc7a236d
  locked: false
  schema_version: 2
  solution: true
---
from a301.geometry import dump_image, area_def_to_dict

image_name = "wv_difference"
### BEGIN SOLUTION
metadata_dict = dict()
metadata_dict["area_def"] = area_def_to_dict(area_def_lr)
metadata_dict["image_name"] = image_name
metadata_dict["description"] = "column wv difference between nearir and ir retrievals"
metadata_dict["modis_metadata"] = parseMeta(a301.data_dir / Path("myd05_l2_10_7.hdf"))
metadata_dict["history"] = "written by level2_cartopy_resample.ipynb"
out_folder = a301.map_dir / Path("wv_maps")
dump_image(wv_difference, metadata_dict, out_folder, image_name)
### END SOLUTION
```

### Here is the test that autograder will run

Copy this code in a new cell and make sure it passes the test (i.e. doesn't complain)
This is what autograder will run automatically

```{code-cell}
---
nbgrader:
  grade: true
  grade_id: cell-f7a3d2999f2dabf4
  locked: true
  points: 5
  schema_version: 2
  solution: false
---
from a301.geometry import get_image

#
# read back the image and the area_def
#
foldername = a301.map_dir / Path("wv_maps")
image_array_name = "wv_difference"
image_array, area_def = get_image(foldername, image_array_name)
#
# make sure the area_def and image sizes agree
#
area_def_size = (area_def.y_size, area_def.x_size)
image_size = image_array.shape
assert area_def_size == image_size
```
