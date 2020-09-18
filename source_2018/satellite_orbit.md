
```{code-cell}

# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Introduction" data-toc-modified-id="Introduction-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Introduction</a></span></li><li><span><a href="#Find-the-part-of-the-orbiting-that-corresponds-to-the-3-minutes-containing-the-storm" data-toc-modified-id="Find-the-part-of-the-orbiting-that-corresponds-to-the-3-minutes-containing-the-storm-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Find the part of the orbiting that corresponds to the 3 minutes containing the storm</a></span></li><li><span><a href="#convert-time-to-distance-by-using-pyproj-to-get-the-greatcircle-distance-between-shots" data-toc-modified-id="convert-time-to-distance-by-using-pyproj-to-get-the-greatcircle-distance-between-shots-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>convert time to distance by using pyproj to get the greatcircle distance between shots</a></span></li><li><span><a href="#Make-the-plot-assuming-that-height-is-the-same-for-every-shot" data-toc-modified-id="Make-the-plot-assuming-that-height-is-the-same-for-every-shot-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Make the plot assuming that height is the same for every shot</a></span></li></ul></div>
```

```{code-cell}


from IPython.core.debugger import set_trace


# # Introduction
# 
# This notebook uses the 2C-RAIN-PROFILE data to compare rain rate and precipitable liquid water with
# the cloudsat reflectivity.
#  Read in the height and reflectivity fields
```

```{code-cell}


from importlib import reload
import numpy as np
import datetime as dt
from datetime import timezone as tz
from matplotlib import pyplot as plt
import pyproj
from numpy import ma
import a301
from a301.cloudsat import get_geo
from pathlib import Path
#
# new functions to read vdata and sds arrays
#
from a301.cloudsat import HDFvd_read, HDFsd_read
plt.style.use('ggplot')
```

```{code-cell}


import pdb
hr_file= list(a301.test_dir.glob('*FLXHR*hdf'))[0]
lats,lons,date_times,prof_times,dem_elevation=get_geo(hr_file)
lats=lats.squeeze()
lons=lons.squeeze()
qr, qr_attrs = HDFsd_read(hr_file,'QR')
#pdb.set_trace()
qr_height, height_attrs = HDFsd_read(hr_file,'Height')
factor = HDFvd_read(hr_file,'QR.factor',vgroup='Swath Attributes')[0][0]
missing = HDFvd_read(hr_file,'QR.missing',vgroup='Swath Attributes')[0][0]
units = HDFvd_read(hr_file,'QR.units',vgroup='Swath Attributes')[0][0]
hit = (qr == missing)
qr = qr.astype(np.float64)/factor
qr[hit]=np.nan
print(units)
print(qr.shape)


# # Find the part of the orbiting that corresponds to the 3 minutes containing the storm
# 
# You need to enter the start_hour and start_minute for the start time of your cyclone in the granule
```

```{code-cell}


def find_times(date_times,start_hour,start_minute,del_minutes):
    first_time=date_times[0]
    print(f'orbit start: {first_time}')
    storm_start=dt.datetime(first_time.year,first_time.month,first_time.day,
                                        start_hour,start_minute,0,tzinfo=tz.utc)
    #
    # get x minutes of data from the storm_start
    #
    storm_stop=storm_start + dt.timedelta(minutes=del_minutes)
    time_hit = np.logical_and(date_times > storm_start,date_times < storm_stop)
    return time_hit

start_hour=6
start_minute=45
del_minutes=3.
time_hit = find_times(date_times,start_hour,start_minute,del_minutes)


#pdb.set_trace()
storm_lats = lats[time_hit]
storm_lons=lons[time_hit]
storm_prof_times=prof_times[time_hit]
storm_qr=qr[:,time_hit,:]
storm_height=qr_height[time_hit,:]
storm_date_times=date_times[time_hit]
print(f'storm start: {storm_date_times[0]}')
```

```{code-cell}


storm_qr.shape


# # convert time to distance by using pyproj to get the greatcircle distance between shots
```

```{code-cell}


def find_distance(storm_lons,storm_lats):
    meters2km=1.e3
    great_circle=pyproj.Geod(ellps='WGS84')
    distance=[0]
    start=(storm_lons[0],storm_lats[0])
    for index in np.arange(1,len(storm_lons)):
        azi12,azi21,step= great_circle.inv(storm_lons[index-1],storm_lats[index-1],
                                           storm_lons[index],storm_lats[index])
        distance.append(distance[index-1] + step)
    distance=np.array(distance)/meters2km
    return distance

distance=find_distance(storm_lons,storm_lats)
shortwave_qr=storm_qr[0,:,:]
longwave_qr=storm_qr[1,:,:]


# # Make the plot assuming that height is the same for every shot
# 
# We need to customize the subplots so we can share the x axis between the radar reflectivity
# and the rain_rate, and adjust the sizes to hold a colorbar
```

```{code-cell}


get_ipython().run_line_magic('matplotlib', 'inline')

from matplotlib import cm
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plot_field2(distance,height,field,fig,cmap=None,norm=None):
    """
    draw a 2 panel plot with different panel sizes.  Put the radar reflectivity
    in the top panel with a colorbar along the bottom, and pass the second
    axis back to be filled in later
    
    uses the sharex keyword to give both plots the same x axis (distance) 
    and the gridspec class to lay out the grid
    
    https://stackoverflow.com/questions/10388462/matplotlib-different-size-subplots
    """
    from matplotlib import gridspec
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1]) 
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1],sharex=ax1)
    if cmap is None:
        cmap=cm.inferno
    col=ax1.pcolormesh(distance,height,field,cmap=cmap,
                  norm=the_norm)
    #https://stackoverflow.com/questions/18195758/set-matplotlib-colorbar-size-to-match-graph
    # create an axes on the bottom side of ax1. The height of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.55 inch.
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("bottom", size="5%", pad=0.55)
    ax1.figure.colorbar(col,extend='both',cax=cax,orientation='horizontal')
    return ax1, ax2

meters2km=1.e3
vmin=0
vmax=15
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
cmap_ref=cm.plasma
cmap_ref.set_over('c')
cmap_ref.set_under('b',alpha=0.2)
cmap_ref.set_bad('0.75') #75% grey

cloud_height_km=qr_height[0,:]/meters2km
fig = plt.figure(figsize=(15, 8)) 
ax1, ax2 = plot_field2(distance,cloud_height_km,shortwave_qr.T,fig,cmap=cmap_ref,norm=the_norm)
ax1.set(ylim=[0,17],xlim=(0,1200))
ax1.set(xlabel='distance (km)',ylabel='height (km)',
       title='equivalent radar reflectivity in dbZe');
vmin=-20
vmax=20.
cmap_ref=cm.bwr
cmap_ref.set_over('c')
cmap_ref.set_under('b',alpha=0.2)
cmap_ref.set_bad('0.75') #75% grey
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
divider = make_axes_locatable(ax2)
cax = divider.append_axes("bottom", size="5%", pad=0.55)
col=ax2.pcolormesh(distance,cloud_height_km,longwave_qr.T,cmap=cmap_ref,
                  norm=the_norm)
ax2.figure.colorbar(col,extend='both',cax=cax,orientation='horizontal')
ax2.set(xlabel='distance (km)',ylabel='height (km)',title='room for title',ylim=[0,17]);
```

```{code-cell}


import cartopy.crs as ccrs
import cartopy
globe = ccrs.Globe(datum="WGS84",ellipse="WGS84")
projection=ccrs.PlateCarree(central_longitude=90.)
print(f'pro4 program params: {projection.proj4_params}')
fig, ax = plt.subplots(1, 1,figsize=[15,15],subplot_kw={'projection': projection})
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale='coarse', levels=[1]));
geodetic = ccrs.Geodetic();
out=projection.transform_points(geodetic,lons,lats)
track=projection.transform_points(geodetic,storm_lons,storm_lats)
ax.plot(out[:,0],out[:,1],'ro');
ax.plot(track[:,0],track[:,1],'bo');
ax.plot(out[0,0],out[0,1],'co',markersize=15)
ax.plot(out[-1,0],out[-1,1],'ko',markersize=15);
```
