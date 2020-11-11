---
jupytext:
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
import a301_lib
import rasterio

notebook_dir=Path().resolve().parent
print(notebook_dir)
week10_scene = notebook_dir / "week10/small_file.tiff"

with rasterio.open(week10_scene) as van_raster:
    b3_refl = van_raster.read(1)
    b4_refl = van_raster.read(2)
    b5_refl = van_raster.read(3)
```

```{code-cell} ipython3

```
