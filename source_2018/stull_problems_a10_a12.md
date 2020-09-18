---
jupytext:
  encoding: '# -*- coding: utf-8 -*-'
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
<div class="toc"><ul class="toc-item"><li><span><a href="#Stull-problem-8-A.10" data-toc-modified-id="Stull-problem-8-A.10-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Stull problem 8-A.10</a></span><ul class="toc-item"><li><span><a href="#my-test-for-a12" data-toc-modified-id="my-test-for-a12-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>my test for a12</a></span></li></ul></li></ul></div>

+++

# Stull problem 8-A.10

+++

Chapter 8-A10. Write a python function to find the beamwidth angle in degrees for a radar pulse
for the following sets of 
[wavelength (cm) , antenna
dish diameter (m)]:
        
a. [ 20, 8] b. [20, 10] c. [10, 10] d. [10, 5] e. [10, 3]
f. [5, 7] g. [5, 5] h. [5, 2] i. [5, 3] j. [3, 1]

```{code-cell}
---
deletable: false
nbgrader:
  cell_type: code
  checksum: f78f1384818ecfda9aeae223ea83ec88
  grade: false
  grade_id: cell-76c7d3f2f1ade0a7
  locked: false
  schema_version: 2
  solution: true
---
import numpy as np
import pytest
import json

def find_beamwidth(the_wavel,dish_size):
    """
    find the beamwidth using Stulll eq. 8.13
    
    Parameters
    ----------
    
    the_wavel : wavelength (float)
       units (cm)
            
    dish_size : antenna dish diameter (float)
       units (m)
       
    Returns
    -------
    
    beamwidth : beamwidth angle  
       units (degrees)
    """
    #
    # Stull eq. 8.13
    #
    # YOUR CODE HERE
    raise NotImplementedError()
```

```{code-cell}
## my test for a10
```

```{code-cell}
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: b325d081ec1cf53fcfb189ecd9604c75
  grade: true
  grade_id: cell-fd6801804d7e081b
  locked: true
  points: 4
  schema_version: 2
  solution: false
---
the_wavel=[20,20,10,10,10,5,5,5,5,3]  #wavelength (cm)
dish_size=[8,10,10,5,3,7,5,2,3,1]   #dishsize (meters)
input_vals=list(zip(the_wavel,dish_size))
assert(len(input_vals)==10)
beamwidth=[find_beamwidth(wavel,dish_size) for wavel,dish_size in input_vals]
#
# test the beamwidth values
#
answer_file='ch8_a10_answer.json'
if Path(answer_file).is_file():
    with open(answer_file,'r') as f:
        answer=json.load(f)
    np.testing.assert_array_almost_equal(beamwidth,answer,decimal=3)
```

```{raw-cell}
# Stull problem 8-A.12

Write a python function to find the range to a radar target, given the
round-trip (return) travel times (µs) of:

a. 2 b. 5 c. 10 d. 25 e. 50
f. 75 g. 100 h. 150 i. 200 j. 300
```

```{code-cell}
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 219c6f3d2faccba6ef83fbf664329f6e
  grade: false
  grade_id: cell-8bce491044638790
  locked: false
  schema_version: 2
  solution: true
---
def find_range(delT):
    """
    tind the range to radar using Stull eq. 8.16
    
    Parameters
    ----------
    
    delT: float
       the round-trip travel times (units: micro sec)
       
    Returns
    -------
    
    radar_range: float
       range from target to radar (units: km)
    """
    
    # YOUR CODE HERE
    raise NotImplementedError()
```

## my test for a12

```{code-cell}
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: f6408a71822220e4a6bfdb7ca4bb31c4
  grade: true
  grade_id: cell-1fcb43fed3abde1d
  locked: true
  points: 4
  schema_version: 2
  solution: false
---
import json
times=[2,5,10,25,50,75,100,150,200,300]  #microseconds
the_range=[find_range(delT) for delT in times]
assert(len(times) == 10)
answer_file='ch8_a12_answer.json'
if Path(answer_file).is_file():
    with open(answer_file,'r') as f:
        answer=json.load(f)
    np.testing.assert_array_almost_equal(the_range,answer,decimal=1)
```

```{code-cell}

```
