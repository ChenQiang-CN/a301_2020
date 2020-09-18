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
<div class="toc"><ul class="toc-item"><li><span><a href="#Your-assignment" data-toc-modified-id="Your-assignment-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Your assignment</a></span></li><li><span><a href="#Original-Radar-equation" data-toc-modified-id="Original-Radar-equation-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Original Radar equation</a></span></li><li><span><a href="#Complete-the-function-below-to-find-dbZ-given-Pr" data-toc-modified-id="Complete-the-function-below-to-find-dbZ-given-Pr-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Complete the function below to find dbZ given Pr</a></span></li><li><span><a href="#Complete-the-function-below-to-find-RR-(mm/hour)-given-dbZ" data-toc-modified-id="Complete-the-function-below-to-find-RR-(mm/hour)-given-dbZ-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Complete the function below to find RR (mm/hour) given dbZ</a></span></li><li><span><a href="#Complete-the-function-below-to-find-RR-given-dbZ" data-toc-modified-id="Complete-the-function-below-to-find-RR-given-dbZ-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Complete the function below to find RR given dbZ</a></span></li></ul></div>

+++ {"nbgrader": {"grade": false, "grade_id": "cell-0a34cf5b2266f058", "locked": true, "schema_version": 2, "solution": false}}

1. Suppose a Nexrad radar (Stull p.~246)  is
   receiving a signal with power $P_r = -58\ dBm$.  Using the radar
   equation find the precipitation rate under the assumption that
   there is no attenuation and that it is a rainstorm (i.e.~liquid water)
   100 km away from the radar.  How does your precipitation estimate (in mm/hour)
   change if $P_r$ remains the same but you:
  
   1.  mistakenly assume it's a snowstorm with no attenuation
  
   1.  miss the fact that there is really a factor of 2 (3 dbZ) attenuation
       between the storm and the radar
    
  
* For 1A, use the relationship that the precip rate in mm/hour and the reflectivity
  are related approximately by $Z=2000R^2$ where the units are as above)
  
# Your assignment

Complete the functions find_dbz, find_RR_liquid and find_RR_snow below.  I'll autotest them
with tests 1, 2 and 3

+++ {"nbgrader": {"grade": false, "grade_id": "cell-06639935fd87f931", "locked": true, "schema_version": 2, "solution": false}}

# Original Radar equation

This is a copy from assignment 13

```{code-cell}
---
nbgrader:
  grade: false
  grade_id: cell-dd262aca7f21c706
  locked: true
  schema_version: 2
  solution: false
---
from numpy import log10
from numpy.testing import assert_almost_equal
import a301
from pathlib import Path

def findPr(Z,K2,La,R,R1=None,Pt=None,b=None,Z1=None):
   """
    solve stull eqn 8.23
    
    Parameters
    ----------
    
    input: Z (mm^6/m^3), K2 (unitless), La (unitless),R (km)
           plus radar coefficients appropriate to given radar (like Nexrad)
           
    Returns
    -------
    
    Pr in W 
   """ 
   if Z1 is None:
      Z1=1.
   Pr=Pt*b*K2/La**2.*(R1/R)**2.*(Z/Z1)
   return Pr

  
#coefficents for nexrad
R1=2.17e-10#range factor, km, Stull 8.25
Pt=750.e3 #transmitted power, W, stull p. 246
b=14255 #equipment factor, Stull 8.26
nexrad=dict(R1=R1,Pt=Pt,b=b)


```

+++ {"nbgrader": {"grade": false, "grade_id": "cell-60cd282d3fe0713e", "locked": true, "schema_version": 2, "solution": false}}

Read in my answer key when I run this notebook

```{code-cell}
---
nbgrader:
  grade: false
  grade_id: cell-8f6b0b453cc2ace3
  locked: true
  schema_version: 2
  solution: false
---
import json, a301
has_key=False
ans_file = a301.test_dir / Path('assign14_sol.json')
if ans_file.is_file():
    with open(ans_file,'r') as f:
        sol=json.load(f)
    has_key=True
```

# Complete the function below to find dbZ given Pr

```{code-cell}
---
nbgrader:
  grade: false
  grade_id: cell-b0c68b3ac8f73c10
  locked: false
  schema_version: 2
  solution: true
---
def find_dbz(Pr,K2,La,R,R1=None,Pt=None,b=None):
   """
   calculate dbZ using Stull 8.28
   
   Parameters
   ----------
   
    input: Pr (W), K2 (unitless), La (unitless),R (km)
           plus radar coefficients appropriate to given radar (like Nexrad)
           
   Returns
   -------
   
   dbZ: float
      decibels referenced to 1 mm^6/m^3
   """
   ### BEGIN SOLUTION
   dbZ=10.*log10(Pr/Pt) + 20.*log10(R/R1) - \
       10.*log10(K2/La**2.) - 10.*log10(b)
   return dbZ
   ### END SOLUTION
```

# Complete the function below to find RR (mm/hour) given dbZ

```{code-cell}
---
nbgrader:
  grade: false
  grade_id: cell-7aa75e8d2a5cec77
  locked: false
  schema_version: 2
  solution: true
---
def find_RR_liquid(dbZ):
   """
    find the rain rate in mm/hr using Stull 8.29
    
    Parameters
    ----------
    
    dbZ:  reflectivity in dbZ referenced to 1 mm^6/m^3
    
    Returns
    -------
    
    RR: float
       rain rate (mm/hour)
   """
   ### BEGIN SOLUTION
   #given that for rain Z=300*RR**1.4
   #a1_rain=(1/300.)**(1/1.4) = 0.017
   #a2_rain=1/1.4  = 0.714
   Z=10**(dbZ/10.)
   a1_rain=0.017  
   a2_rain=0.714  
   RR=a1_rain*Z**a2_rain
   return RR
   ### END SOLUTION

```

# Complete the function below to find RR given dbZ

Assuming $Z=2000 \times {RR}^2$

```{code-cell}
---
nbgrader:
  grade: false
  grade_id: cell-352bd3084340f09f
  locked: false
  schema_version: 2
  solution: true
---
def find_RR_snow(dbZ):
   """
    find the snow rate in mm/hr assuming
    Z=2000*RR**2.
    
    Parameters
    ----------

    dbZ:  reflectivity in dbZ referenced to 1 mm^6/m^3
    
    Returns
    -------
    
    RR: float
      Snow rate in liquid equivalent mm/hour
   """
   ### BEGIN SOLUTION
   #given that for snow Z=2000*RR**2. 
   a1_snow=0.02236   #(1/2000.)**(1./2.)
   a2_snow=0.5   #RR=(1/2000)**(1./2.)*Z**(1/2.)
   Z=10**(dbZ/10.)
   RR=a1_snow*Z**a2_snow
   return RR
   ### END SOLUTION
```

Test 1: 
 
     Suppose a Nexrad radar (Stull p.~246)  is
     receiving a signal with returned power Pr = -58 dBm.  Using the radar
     equation find the precipitation rate under the assumption that
     there is no attenuation and that it is a rainstorm (i.e. liquid water)
     100 km away from the radar.

```{code-cell}
K2=0.93  #stull p. 245
Pr=10**(-5.8)*1.e-3  #dBm=-58, convert from mWatts to Watts
La=1
R=100.  #km
dbZ_q1=find_dbz(Pr,K2,La,R,**nexrad)
RR_q1=find_RR_liquid(dbZ_q1)
```

```{code-cell}
---
nbgrader:
  grade: true
  grade_id: cell-3a41031ec19e6408
  locked: true
  points: 2
  schema_version: 2
  solution: false
---
if has_key:
    assert_almost_equal(dbZ_q1,sol['dbZ_q1'],decimal=1)
    assert_almost_equal(RR_q1,sol['RR_q1'],decimal=1)
```

+++ {"nbgrader": {"grade": false, "grade_id": "cell-4b7d113e35157f59", "locked": true, "schema_version": 2, "solution": false}}

Test 2: 

    Now keep everything the same, but make the mistake of guessing that it's a snowstorm,
    which means that K2=0.208 and we use the snowfall Z-RR relation
    of Z=2000*RR**2.  What are your new guesses for dbZ and RR?
        
        

```{code-cell}
K2=0.208 #p. 245
dbZ_q2=find_dbz(Pr,K2,La,R,**nexrad)
RR_q2=find_RR_snow(dbZ_q2)
```

```{code-cell}
---
nbgrader:
  grade: true
  grade_id: cell-722bf3b6d8cb37c0
  locked: true
  points: 2
  schema_version: 2
  solution: false
---
if has_key:
    assert_almost_equal(dbZ_q2,sol['dbZ_q2'],decimal=1)
    assert_almost_equal(RR_q2,sol['RR_q2'],decimal=1)
```

Test 3: 
    
     Now assume it's rain, but put in an attenuation of La=1.2 between
     between the target and the rainstorm.  What are your new guesses for dbZ and RR?

```{code-cell}
K2=0.93 #p. 245
La=1.2
dbZ_q3=find_dbz(Pr,K2,La,R,**nexrad)
RR_q3=find_RR_liquid(dbZ_q3)
```

```{code-cell}
---
nbgrader:
  grade: true
  grade_id: cell-6fb1eeb32921b9b4
  locked: true
  points: 2
  schema_version: 2
  solution: false
---
if has_key:
    assert_almost_equal(dbZ_q3,sol['dbZ_q3'],decimal=1)
    assert_almost_equal(RR_q3,sol['RR_q3'],decimal=1)
```
