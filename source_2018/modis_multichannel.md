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
<div class="toc"><ul class="toc-item"><li><span><a href="#Changes-to-modis_level1b_read" data-toc-modified-id="Changes-to-modis_level1b_read-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Changes to modis_level1b_read</a></span></li><li><span><a href="#Introduction" data-toc-modified-id="Introduction-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Introduction</a></span></li><li><span><a href="#If-you-want-to-work-with-my-day-222:" data-toc-modified-id="If-you-want-to-work-with-my-day-222:-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>If you want to work with my day 222:</a></span></li><li><span><a href="#Reading-modis-data" data-toc-modified-id="Reading-modis-data-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Reading modis data</a></span><ul class="toc-item"><li><span><a href="#Using-pydf-to-get-metadata" data-toc-modified-id="Using-pydf-to-get-metadata-4.1"><span class="toc-item-num">4.1&nbsp;&nbsp;</span>Using pydf to get metadata</a></span></li><li><span><a href="#open-one-of-the-datasets-(number-4,-EV_1KM_Emissive)-and-get-its-shape-and-data-type" data-toc-modified-id="open-one-of-the-datasets-(number-4,-EV_1KM_Emissive)-and-get-its-shape-and-data-type-4.2"><span class="toc-item-num">4.2&nbsp;&nbsp;</span>open one of the datasets (number 4, EV_1KM_Emissive) and get its shape and data type</a></span></li><li><span><a href="#Get-the-first-row-of-the-first-channel-and-find-its-numpy-dtype" data-toc-modified-id="Get-the-first-row-of-the-first-channel-and-find-its-numpy-dtype-4.3"><span class="toc-item-num">4.3&nbsp;&nbsp;</span>Get the first row of the first channel and find its numpy dtype</a></span></li><li><span><a href="#get-all-the-rows-and-columns-for-the-first-channel" data-toc-modified-id="get-all-the-rows-and-columns-for-the-first-channel-4.4"><span class="toc-item-num">4.4&nbsp;&nbsp;</span>get all the rows and columns for the first channel</a></span></li><li><span><a href="#Find-the-attributes-for-EV_1KM_Emissive" data-toc-modified-id="Find-the-attributes-for-EV_1KM_Emissive-4.5"><span class="toc-item-num">4.5&nbsp;&nbsp;</span>Find the attributes for EV_1KM_Emissive</a></span></li><li><span><a href="#Print-the-first-100-characters-of-the-Metadata.0-string" data-toc-modified-id="Print-the-first-100-characters-of-the-Metadata.0-string-4.6"><span class="toc-item-num">4.6&nbsp;&nbsp;</span>Print the first 100 characters of the Metadata.0 string</a></span></li></ul></li><li><span><a href="#Now-write-channels-out-into-a-new-hdf" data-toc-modified-id="Now-write-channels-out-into-a-new-hdf-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Now write channels out into a new hdf</a></span><ul class="toc-item"><li><span><a href="#find-the-index-for-channel-30" data-toc-modified-id="find-the-index-for-channel-30-5.1"><span class="toc-item-num">5.1&nbsp;&nbsp;</span>find the index for channel 30</a></span></li><li><span><a href="#Let-python-figure-this-out" data-toc-modified-id="Let-python-figure-this-out-5.2"><span class="toc-item-num">5.2&nbsp;&nbsp;</span>Let python figure this out</a></span></li><li><span><a href="#Read-channel-30-at-index-9-into-a-numpy-array-of-type-uint16" data-toc-modified-id="Read-channel-30-at-index-9-into-a-numpy-array-of-type-uint16-5.3"><span class="toc-item-num">5.3&nbsp;&nbsp;</span>Read channel 30 at index 9 into a numpy array of type uint16</a></span></li></ul></li><li><span><a href="#Calibrate-the-raw-counts-for-both-channels" data-toc-modified-id="Calibrate-the-raw-counts-for-both-channels-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Calibrate the raw counts for both channels</a></span></li><li><span><a href="#Write-the-calibrated-channel-out-for-safekeeping" data-toc-modified-id="Write-the-calibrated-channel-out-for-safekeeping-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>Write the calibrated channel out for safekeeping</a></span></li></ul></div>

+++

# Changes to modis_level1b_read

This notebook shows how to write both channel 30 and channel 31 out to an hdf file
called modis_chans.hdf.  It uses two new functions to avoid repetiion

```python
get_index
```

defined in section 3.2 and

```python
write_chan
```

defined in section 5

```{code-cell}
import pdb
import pprint
import shutil
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from pyhdf.SD import SD
from pyhdf.SD import SDC

import a301
from a301.scripts.modismeta_read import parseMeta
from a301.utils.data_read import download
```

# Introduction

This notebook assumes that you have gone to the LAADS DAAC archive and downloaded a Modis Level1b 5 minute granule from the Aqua satellite (a MYD021KM hdf file).  Below we use the pyhdf module to read a single channel (channel 30) centered at 9.7 microns according to [the Modis channel listing](https://modis.gsfc.nasa.gov/about/specifications.php).  We plot the raw counts from that channel using the
[matplotlib imshow](https://matplotlib.org/examples/images_contours_and_fields/image_demo.html) function to display the raw image.



+++

# If you want to work with my day 222:

execute the cell below
otherwise delete

```{code-cell}
#
# this is my MYD02 file, substitute your own here
# It needs to be copyied to a301.data_dir
#
modis_file = "MYD021KM.A2013222.2105.061.2018047235850.hdf"
download(modis_file)
generic_m2 = a301.data_dir / Path(modis_file)
shutil.copy(Path(modis_file), generic_m2)
```

```{code-cell}
#
# replace with your file name if needed
#
modis_file = "MYD021KM.A2013222.2105.061.2018047235850.hdf"
generic_m2 = a301.data_dir / Path(modis_file)
```

```{code-cell}
#
# confirm that we can read this file
#
modis_meta = parseMeta(str(generic_m2))
print(f"opened and read {modis_meta['filename']}")
#
# this is my modis multichannel output file
#
generic_rad = a301.data_dir / Path("rad_file_2018_10_1.hdf")
```

# Reading modis data

+++

## Using pydf to get metadata

I can convert the filename from a Path object to a string object and pass it to pyhdf.SD
to find out how many datasets and attributes there are in the file

In the cell below I use [f-strings](https://realpython.com/python-f-strings/) to simplify the print command,
and split the string up across multiple lines by enclosing it in a tuple.  This works because
when python sees that the individual lines aren't separated by a comma, it concatenates them together.
The character \n means "newline"

Note that I need to construct the full path to the data file so pyhdf can find it. pyhdf was
written before pathlib (which was introduced in python 3.5),
so I need to convert the Path object to a simple string using str()

```{code-cell}
the_file = SD(str(generic_m2), SDC.READ)
stars = "*" * 50
print(
    (
        f"\n{stars}\nnumber of datasets, number of attributes"
        f"={the_file.info()}\n{stars}\n"
        f"\nHere is the help file for the info funtion:\n"
    )
)
help(SD.info)
```

## open one of the datasets (number 4, EV_1KM_Emissive) and get its shape and data type

```{code-cell}
longwave_data = the_file.select("EV_1KM_Emissive")  # select sds
print(longwave_data.info())
```

## Get the first row of the first channel and find its numpy dtype

(unit16 is "unsigned 16 bit integer", which is how the modis raw counts are stored)

```{code-cell}
data_row = longwave_data[0, 0, :]  # get sds data
print(data_row.shape, data_row.dtype)
```

## get all the rows and columns for the first channel

```{code-cell}
longwave_data[0, :, :]
```

## Find the attributes for EV_1KM_Emissive

```{code-cell}
pprint.pprint(longwave_data.attributes())
```

## Print the first 100 characters of the Metadata.0 string

Date, orbit number, etc. are stored in a long string attribute called 'StructMetadata.0'.  The \t character is a tab stop.

```{code-cell}
pprint.pprint(the_file.attributes()["StructMetadata.0"][:100])
```

# Now write channels out into a new hdf

```{code-cell}
longwave_bands = the_file.select("Band_1KM_Emissive")
```

```{code-cell}
longwave_bands.attributes()
```

Note that only channels 20 to 36 are in the Emissive dataset (see [the Modis channel listing](https://modis.gsfc.nasa.gov/about/specifications.php))

+++

## find the index for channel 30

Count the following and convince yourself that channel 30 is index 9, starting from 0

```{code-cell}
band_nums = longwave_bands.get()
print(f"here are the modis channels in the emissive dataset \n{band_nums}")
```

## Let python figure this out

We don't want to have to count, so use numpy.searchsorted to find the the index with value closest to 30

We need to turn that index (type int64) into a plain python int so it can be used to specify the channel
(float doesn't work)

```{code-cell}
def get_index(band_nums, chan_num):
    """
    given the longwave_bands vecto from the level1b file, 
    find the index of the channel chan_num in the dataset
    
    Parameters
    ----------
    
    band_nums: numpy float vector
       list of channel numbers
       
    chan_num: float or int
       channel number to get index for
       
    Returns
    -------
    
    the_index: int
        index of channel in modis image

    """
    ch_index = np.searchsorted(band_nums, chan_num)
    return int(ch_index)


ch30_index = get_index(band_nums, 30.0)
ch31_index = get_index(band_nums, 31.0)
print(f"channel 30 is located at index {ch30_index} and channel 31 at {ch31_index}")
```

## Read channel 30 at index 9 into a numpy array of type uint16

```{code-cell}
ch30_data = longwave_data[ch30_index, :, :]
ch31_data = longwave_data[ch31_index, :, :]
print(ch30_data.shape)
print(ch30_data.dtype)
```

# Calibrate the raw counts for both channels

To turn the raw counts into pixel radiances, you need to apply equation 5.8 on p. 36 of the
[modis users guide](https://www.dropbox.com/s/ckd3dv4n7nxc9p0/modis_users_guide.pdf?dl=0):

$Radiances = (RawData - offset) \times scale$

We have just read the RawData,  the offset and the scale are stored in two vectors that are attributes of the Emissive dataset.  Make a version of the figure above, but plot Channel 30 radiance (in W/m^2/micron/sr), rather than raw counts.


```{code-cell}
scales = longwave_data.attributes()["radiance_scales"]
offsets = longwave_data.attributes()["radiance_offsets"]
ch30_scale = scales[ch30_index]
ch30_offset = offsets[ch30_index]
ch31_scale = scales[ch31_index]
ch31_offset = offsets[ch31_index]
print(f"ch30 scale: {ch30_scale}, ch30 offset: {ch30_offset}")
print(f"ch31 scale: {ch31_scale}, ch31 offset: {ch31_offset}")
```

```{code-cell}
ch30_calibrated = (ch30_data - ch30_offset) * ch30_scale
ch31_calibrated = (ch31_data - ch31_offset) * ch31_scale
the_file.end()
```

# Write the calibrated channel out for safekeeping

Follow the example here: https://hdfeos.org/software/pyhdf.php

```{code-cell}
def write_chan(sd, numpy_array, chan_name):
    """
    given an open pyhdf SD object, a numpy_array and a 
    string channel name, write the channel out to the sd
    """
    # Create a dataset
    sds = sd.create(chan_name, SDC.FLOAT64, numpy_array.shape)

    # Fill the dataset with a fill value
    sds.setfillvalue(0)

    # Assign an attribute to the dataset
    sds.units = "W/m^2/micron/sr"

    # Write data
    sds[:, :] = numpy_array[:, :]
    print(f"writing sds with shape {numpy_array.shape}")

    # Close the dataset
    sds.endaccess()


# Create an HDF file
sdout = SD(str(generic_rad), SDC.WRITE | SDC.CREATE)

#
# write out two channels
#
write_chan(sdout, ch30_calibrated, "ch30")
write_chan(sdout, ch31_calibrated, "ch31")

# Flush and close the HDF file
sdout.filename = modis_meta["filename"]
sdout.comment = "written by modis_multichannel.ipynb"
sdout.end()
```

```{code-cell}
from a301.scripts import hdf4ls

hdf4ls.hdf4ls(str(generic_rad))
```
