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
<div class="toc"><ul class="toc-item"><li><span><a href="#2014-final----solutions" data-toc-modified-id="2014-final----solutions-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>2014 final -- solutions</a></span></li></ul></div>

+++

### 2014 final -- solutions

```{code-cell}
%matplotlib inline
```

```{code-cell}
import numpy as np
```

##Q1

+++

a) (3)  Explain as clearly as you can what numpy's searchsorted function does.  Include your best
guess about what the variable vals contains after we execute statement [9].

+++

Give an example of  how searchsorted is used in python programs we've encountered
in class -- you don't have to regurgitate the code, just describe why it is needed and what
specifically it accomplishes in one or more of our programs.

```{code-cell}
np.searchsorted([2, 4, 5, 6, 10, 12], [-2, -5, 10, 1, 4, 6, 0, 4, 14], "right")
```

##Q2

+++

Derivation of Schwartzchild equation

```{code-cell}
from numpy import pi, exp, cos
import matplotlib.pyplot as plt


plt.close("all")
thetime = np.arange(0.0, 2.5 * pi, 0.05)
thewave = thetime
four5 = 45.0 * pi / 180.0
thirty = 30 * pi / 180.0
sixty = 2.0 * thirty
onefifty = 5.0 * thirty


fig1, axis1 = plt.subplots(1, 1)
axis1.plot(thewave, np.cos(thetime + four5), "k-", lw=5, label="pulse 1")
axis1.plot(thewave, np.cos(thetime + onefifty), "k+", lw=5, label="pulse 2")
axis1.set_xlabel("horizontal position (one wavelength=2pi)")
axis1.set_ylabel("amplitude")
axis1.set_title(" ")
pos = [
    0.0,
    0.25 * pi,
    0.5 * pi,
    0.75 * pi,
    1.0 * pi,
    1.25 * pi,
    1.5 * pi,
    1.75 * pi,
    2 * pi,
    2.25 * pi,
]
labels = ["0", "pi/4", "pi/2", "3pi/4", "pi", "5pi/4", "6pi/4", "7pi/4", "2pi", "9pi/4"]
axis1.grid()
axis1.set_xticks(pos)
axis1.set_xticklabels(labels)
axis1.legend(loc="best")
fig1.savefig("phase_shift_final.png")
```

```{code-cell}
# pulse1
I = 0.707
Q = -(-0.707)  # = 0.707
# pulse2
I = -0.866
Q = -(-0.5)  # =0.5
# first angle= +45
# pulse2=150 degrees
mrmax = 0.1 * 600.0 / 4.0
```

```{code-cell}
mrmax
```

```{code-cell}
# smallest angle is 150 - 45.
(150.0 - 45.0) / 180.0 * 15  # 8.75 m/s into the radar
angle = 150 - 45.0
# second guess
angle2 = 360.0 - angle
(angle2) / 180.0 * 15  # away from the radar
```

```{code-cell}
sigma = 5.67e-8
tau1 = 0.001 * 1500
tau2 = 0.001 * 1000.0
tr1 = exp(-5 / 3.0 * tau1)
temp1 = 260.0
temp2 = 280.0
tempsfc = 300.0
tr2 = exp(-5.0 / 3.0 * tau2)
eps1 = 1.0 - tr1
eps2 = 1.0 - tr2
Fsfc = sigma * tempsfc ** 4.0
F1 = eps1 * sigma * temp1 ** 4.0
F2 = eps2 * sigma * temp2 ** 4.0
print(Fsfc)
print(Fsfc * tr1)
print(Fsfc * tr1 * tr2)
print(F2)
print(F1)
print(F1 * tr2)
```

```{code-cell}
tr1
```

```{code-cell}
-(7 + 283 + 45)
```

```{code-cell}
-37 + 283 - 237
```

```{code-cell}
-335 - 9
```

```{code-cell}
(-334.0 / 1500.0) / 1004.0 * 3600.0 * 24.0
```

```{code-cell}
B1 = 7
B2 = 4.9
angle = 30.0 * pi / 180.0
# angle=60.*pi/180.
tau2 = 1.5 / cos(angle)
tau1 = 1.0 / cos(angle)
tr1 = exp(-tau1)
tr2 = exp(-tau2)
eps1 = 1.0 - tr1
eps2 = 1.0 - tr2
```

```{code-cell}
I = eps2 * B2 * tr1 + eps1 * B1
I
```

```{code-cell}
flux = I * 0.01 * 2.0
```

```{code-cell}
flux
```

```{code-cell}

```
