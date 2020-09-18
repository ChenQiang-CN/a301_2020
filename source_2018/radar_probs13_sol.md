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
<div class="toc"><ul class="toc-item"><li><span><a href="#Marshall-Palmer-Solution" data-toc-modified-id="Marshall-Palmer-Solution-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Marshall Palmer Solution</a></span></li></ul></div>

+++ {"nbgrader": {"grade": false, "grade_id": "cell-b2a76f5ac9595c65", "locked": true, "schema_version": 2, "solution": false}}

1. (hand in camera upload or on paper):  Integrate $Z=\int D^6 n(D) dD$  assuming a Marshall Palmer size distribution and show that it integrates to:

      $$Z \approx 300 RR^{1.5}$$

   with Z in $mm^6\,m^{-3}$ and RR in mm/hr.  It's helpful to know that:

      $$\int^\infty_0 x^n \exp( -a x) dx = n! / a^{n+1}$$


# Marshall Palmer Solution


The Marshall-Palmer distrution from the [the class notes](https://clouds.eos.ubc.ca/~phil/courses/atsc301/marshall_palmer.html#radar-problems)

$$n(D) = n_0 \exp(-4.1 RR^{-0.21} D )$$

with $n_0$ in units of $m^{-3}\,mm^{-1}$, D in mm,
so that $\Lambda=4.1 RR^{-0.21}$ has to have units
of $mm^{-1}$.

If we use this to integrate:

$$Z=\int D^6 n(D) dD$$

and use the hint that


$$\int^\infty_0 x^n \exp( -a x) dx = n! / a^{n+1}$$


with n=6 we get:

$$Z=\frac{n_0 6!}{\Lambda^7}$$

with units of  $m^{-3}\,mm^{-1} \times ((mm^{-1})^7)^{-1}=mm^6\,m^{-3}$ as required.  Since $n_0=8000\ m^{-3}\,mm^{-1}$ and 6!=720, the
numerical coeficient is 8000x720/(4.1**7)=295.75 and  the final form is:

$$Z=296 RR^{1.47}$$




```{code-cell}
---
nbgrader:
  grade: false
  grade_id: cell-581c3f7af4b08a31
  locked: false
  schema_version: 2
  solution: true
---
def findPr(Z, K2, La, R, R1=None, Pt=None, b=None, Z1=None):
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
    ### BEGIN SOLUTION
    if Z1 is None:
        Z1 = 1.0
    Pr = Pt * b * K2 / La ** 2.0 * (R1 / R) ** 2.0 * (Z / Z1)
    return Pr

    ### END SOLUTION
```

```{code-cell}
---
nbgrader:
  grade: true
  grade_id: cell-d7c71b7e8e7c1929
  locked: true
  points: 5
  schema_version: 2
  solution: false
---
from numpy.testing import assert_almost_equal

# stull p. 246 sample appliation
# given

# coefficents for nexrad
R1 = 2.17e-10  # range factor, km, Stull 8.25
Pt = 750.0e3  # transmitted power, W, stull p. 246
b = 14255  # equipment factor, Stull 8.26

nexrad = dict(R1=R1, Pt=Pt, b=b)

Z = 1.0e4  # Z of 40 dbZ
R = 20  # range of 20 km
K2 = 0.93  # liquid water
La = 1  # no attenuation

power_watts = findPr(Z, K2, La, R, **nexrad)
assert_almost_equal(1.17e-8, power_watts)
```

```{code-cell}

```
