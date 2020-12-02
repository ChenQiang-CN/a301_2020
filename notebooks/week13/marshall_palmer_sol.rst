.. _marshall_palmer_solution:

Marshall Palmer Solution
________________________

.. math::

   n(D) = n_0 \exp(-4.1 RR^{-0.21} D )

with :math:`n_0` in units of :math:`m^{-3}\,mm^{-1}`, D in mm,
so that :math:`\Lambda=4.1 RR^{-0.21}` has to have units
of :math:`mm^{-1}`.

If we use this to integrate:

.. math::

   Z=\int D^6 n(D) dD

and use the hint that

.. math::

   \int^\infty_0 x^n \exp( -a x) dx = n! / a^{n+1}


with n=6 we get:

.. math::

   Z=\frac{n_0 6!}{\Lambda^7}

with units of  :math:`m^{-3}\,mm^{-1}/(mm^{-1})^7=mm^6\,m^{-3}` as required.  Since :math:`n_0=8000\ m^{-3}\,mm^{-1}` and 6!=720, the
numerical coeficient is 8000x720/(4.1**7)=295.75 and  the final form is:

.. math::

   Z=296 RR^{1.47}
   
