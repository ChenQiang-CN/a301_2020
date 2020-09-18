
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
from pyhdf.SD import SD, SDC
import pdb
#
# new functions to read vdata and sds arrays
#
from a301.cloudsat import HDFvd_read, HDFsd_read
plt.style.use('ggplot')
```

```{code-cell}
r_file= list(a301.test_dir.glob('*20875*2C-RAIN-PROFILE*hdf'))[0]
rain_rate = HDFvd_read(r_file,'rain_rate',vgroup='Data Fields')
lats,lons,date_times,prof_times,dem_elevation=get_geo(r_file)
invalid = (rain_rate == -9999.)
rain_rate[invalid] = np.nan
hit = rain_rate < 0.
rain_rate[hit] = np.abs(rain_rate[hit])
plt.plot(rain_rate)
ax=plt.gca()
ax.set(ylabel='rain rate in mm/hr',xlabel='shot number')
plt.savefig('whole_orbit.png')
rain_rate=rain_rate.squeeze()
hit = rain_rate > 30
print(date_times[hit])
```

```{code-cell}

```

first_time=date_times[0]
print(f'orbit start: {first_time}')
start_hour=20
start_minute=30
storm_start=starttime=dt.datetime(first_time.year,first_time.month,first_time.day,
                                        start_hour,start_minute,0,tzinfo=tz.utc)
#
# get 3 minutes of data from the storm_start
#
storm_stop=storm_start + dt.timedelta(minutes=30)
print(f'storm start: {storm_start}')
time_hit = np.logical_and(date_times > storm_start,date_times < storm_stop)
storm_lats = lats[time_hit]
storm_lons=lons[time_hit]
storm_prof_times=prof_times[time_hit]
storm_date_times=date_times[time_hit]
rain_rate=rain_rate[time_hit]
plt.show()

```{code-cell}

```
