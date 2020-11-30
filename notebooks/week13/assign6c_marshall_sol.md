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

(assign6c_marshall_sol)=

# Assign 6c: Marshall Palmer Solution

Given a size distribution

$$
n(D) = n_0 \exp(-4.1 RR^{-0.21} D )
$$

with $n_0$ in units of $m^{-3}\,mm^{-1}$, D in mm,
so that $\Lambda=4.1 RR^{-0.21}$ has to have units
of $`mm^{-1}$.

If we use this to integrate:

$$
   Z=\int D^6 n(D) dD
$$

and use the hint that

$$
   \int^\infty_0 x^n \exp( -a x) dx = n! / a^{n+1}
$$

with n=6 we get:

$$
   Z=\frac{n_0 6!}{\Lambda^7}
$$

with units of  $m^{-3}\,mm^{-1}/(mm^{-1})^7=mm^6\,m^{-3}$ as required.  Since
$n_0=8000\ m^{-3}\,mm^{-1}$ and 6!=720, the
numerical coeficient is 8000x720/(4.1**7)=295.75 and  the final form is:

$$
   Z=296 RR^{1.47}
$$

```{code-cell} ipython3
import numpy as np
def marshall_dist(Dvec, RR):
    """
    Calcuate the Marshall Palmer drop size distribution
    Input: Dvec: vector of diameters in mm
           RR: rain rate in mm/hr
    output: n(Dvec), length of Dvec, in m^{-3} mm^{-1}
    """
    N0 = 8000  # m^{-3} mm^{-1}
    the_lambda = 4.1 * RR ** (-0.21)
    output = N0 * np.exp(-the_lambda * Dvec)
    return output

def numerical_Z(ndist,Dvec):
    nmid = (ndist[1:] + ndist[:-1])/2.
    Dmid = (Dvec[1:] + Dvec[:-1])/2.
    dD = np.diff(Dvec)
    Z = np.sum(nmid*Dmid**6.*dD)
    return Z

def analytic_Z(RR):
    Z=296*RR**1.47
    return Z

RR = 5  #mm/hour
Dvec = np.linspace(0,50,10000)
ndist = marshall_dist(Dvec,RR)
comp_Z=numerical_Z(ndist,Dvec)
calculus_Z=(analytic_Z(RR))
print(f"using numpy Z={comp_Z:5.2f} mm^6/m^3 for a rainrate of {RR} mm/hour")
print(f"using calculus Z={calculus_Z:5.2f} mm^6/m^3 for a rainrate of {RR} mm/hour")
```
