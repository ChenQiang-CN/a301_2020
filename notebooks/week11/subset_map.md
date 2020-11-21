---
jupytext:
  cell_metadata_filter: all
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

```{code-cell} ipython3
import datetime
import pprint
from pathlib import Path

import cartopy
import geopandas as gpd
import pytz
from matplotlib import pyplot as plt
```

```{code-cell} ipython3
import a301_lib

pacific = pytz.timezone("US/Pacific")
date = datetime.datetime.today().astimezone(pacific)
print(f"written on {date}")
```

(subset_map)=
# Finding shapefiles with fiona

This notebook shows how to use fiona (used by geopandas) to subset big shapefiles
for your landsat scene. To use this notebook edit these variables below

    extent:  the lon/lat coords of your clipping region (can be bigger than your scene)
    small_shapes:  the folder name you want the geojson written to
    read_files:  set to True for the first pass, False later to read
               from the geojson folder instead (much quicker)

The shapefiles levels are described in the [Readme](https://github.com/phaustin/a301_2020/blob/master/notebooks/week11/Readme_gshhs_wdbII.md).

Things to notice:

1) how I use the filenames as dictionary keys for the dataframes
2) how geopandas uses .cx  to slice by coordinate the find_features function
3) how I create a figure in make_map and then add to it in the next cell

```{code-cell} ipython3
#
# customize extent, read_files and small_shapes here
#
# extent order (xleft, xright, ybot, ytop)
extent = [130, 140, 30, 40]  # Osaka
# extent = [-125, -115,35, 50]  #bc/washington/oregon
read_files = True
small_shapes = Path().home() / "pha_shapes_asia"
#
#
#
small_shapes.mkdir(exist_ok=True, parents=True)
#
# read either the original shape files or the subsetted
# geojson files
#
gpd_dict = {}
if read_files:
    all_cia = a301_lib.data_share / "openstreetmap/WDBII_shp/f"
    all_cia = list(all_cia.glob("*"))
    for item in all_cia:
        gpd_dict[item.name] = gpd.read_file(item)
        print(f"read {item.name}")

    all_gshhs = a301_lib.data_share / "openstreetmap/GSHHS_shp/f"
    all_gshhs = list(all_gshhs.glob("*"))

    for item in all_gshhs:
        gpd_dict[item.name] = gpd.read_file(item)
        print(f"read {item.name}")
else:
    shape_files = list(small_shapes.glob("*"))
    pprint.pprint(small_shapes)
    for item in shape_files:
        no_suffix = item.with_suffix("")
        key = no_suffix.name
        gpd_dict[key] = gpd.read_file(item)
pprint.pprint(gpd_dict.keys())
```

## Subsetting

In this cell I choose my extent in lon/lat coords and search for the
rows that have features that fall inside the extent.  Geopandas has
a special type of coordinate indexing (`.cx`), so that this:

     hit_rows = df.cx[xleft:xright,ybot:ytop]

runs ogr2ogr to clip the rows that are inside the bounding box.

```{code-cell} ipython3
---
execution:
  iopub.execute_input: '2020-11-21T21:06:38.834739Z'
  iopub.status.busy: '2020-11-21T21:06:38.833901Z'
  iopub.status.idle: '2020-11-21T21:06:38.837895Z'
  shell.execute_reply: '2020-11-21T21:06:38.837296Z'
---
def find_features(extent, df):
    """
    given an extent and a dataframe, return a new dataframe
    containing only features that fall within the extent

    Parameters
    ----------

    extent:  list -- geographic extent in lon (deg E)/lat (deg N)
    df:  the geopandas dataframe to slice
    """
    xleft, xright, ybot, ytop = extent
    hit_rows = df.cx[xleft:xright, ybot:ytop]
    return hit_rows
```

### use find_features to clip the shapefiles

Keep only those frames that have shapes in the extent.  We only
need to do this the first time we run the notebook

```{code-cell} ipython3
---
execution:
  iopub.execute_input: '2020-11-21T21:06:38.843882Z'
  iopub.status.busy: '2020-11-21T21:06:38.843032Z'
  iopub.status.idle: '2020-11-21T21:06:38.847534Z'
  shell.execute_reply: '2020-11-21T21:06:38.846633Z'
---
subset_dict = {}
if read_files:
    for key, df in gpd_dict.items():
        df_subset = find_features(extent, df)
        if len(df_subset) > 0:
            subset_dict[key] = df_subset
    print(subset_dict.keys())
```

```{code-cell} ipython3
---
execution:
  iopub.execute_input: '2020-11-21T21:06:38.854309Z'
  iopub.status.busy: '2020-11-21T21:06:38.853448Z'
  iopub.status.idle: '2020-11-21T21:06:38.857396Z'
  shell.execute_reply: '2020-11-21T21:06:38.858195Z'
---
def make_map(extent, figsize=(15, 15)):
    """
    given an extent vector in the PlateCarre (lon/lat) projection,
    make a map

    Parameters:
        extent:  list with [xbot, xtop, ybot, ytop]
        figsize: (optional) figure size is inches

    Returns:
         fig, ax: cartopy figure and axis
    """
    cartopy_crs = cartopy.crs.PlateCarree()
    fig, ax = plt.subplots(
        1, 1, figsize=figsize, subplot_kw={"projection": cartopy_crs}
    )
    ax.set_extent(extent, cartopy_crs)
    return fig, ax
```

```{code-cell} ipython3
---
execution:
  iopub.execute_input: '2020-11-21T21:06:38.868737Z'
  iopub.status.busy: '2020-11-21T21:06:38.867715Z'
  iopub.status.idle: '2020-11-21T21:06:39.411379Z'
  shell.execute_reply: '2020-11-21T21:06:39.412508Z'
---
fig, ax = make_map(extent)
for key, df in subset_dict.items():
    print(f"adding {key} with {len(df)} features")
    if key.find("river") > -1:
        ax.add_geometries(
            df["geometry"], ax.projection, facecolor="none", edgecolor="green"
        )
    else:
        ax.add_geometries(
            df["geometry"], ax.projection, facecolor="none", edgecolor="blue"
        )
gl = ax.gridlines(
    crs=ax.projection,
    draw_labels=True,
    linewidth=2,
    color="gray",
    alpha=0.5,
    linestyle="--",
)
```

## Save the dataframes as geojson files for replotting

This will write geojson files into the `small_shapes` folder you defined at the top of the notebook.
To read these back in, set

    read_files=False

```{code-cell} ipython3
---
execution:
  iopub.execute_input: '2020-11-21T21:06:39.419050Z'
  iopub.status.busy: '2020-11-21T21:06:39.417945Z'
  iopub.status.idle: '2020-11-21T21:06:39.422448Z'
  shell.execute_reply: '2020-11-21T21:06:39.421363Z'
---
for key, df in subset_dict.items():
    filename = small_shapes / key
    filename = filename.with_suffix(".json")
    print(f"writing {filename}")
    df.to_file(filename, driver="GeoJSON")
```
