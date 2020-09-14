.. _beers_law:

Beers and inverse squared laws
++++++++++++++++++++++++++++++

Comments/derivations for the material in  Stull p. 38-39

.. _differences:

Differences, differentials and derivatives
==========================================

1) What is a derivative?

-  According to
   `wikipedia <https://en.wikipedia.org/wiki/Derivative>`__, a
   derivative is defined as:

   The derivative of a function of a real variable measures the
   sensitivity to change of a quantity (a function value or dependent
   variable) which is determined by another quantity (the independent
   variable).

2) What is the derivative of :math:`E = \sigma T^4` with respect to T?

.. math:: \frac{dE}{dT} = \frac{d \sigma T^4}{dT} = 4 \sigma T^3 

Does that mean that you are free to treat dE/dT as a fraction, and
cancel dT in the denominator to write:

.. math:: dE = \frac{d \sigma T^4}{dT} dT = 4 \sigma T^3 dT

Scientists (and mathematicians) do this all the time, but that isn't how
derivatives work -- dE/dT is a function, not a fraction. So what is
really going on?

3) Instead, we need to treat the differentials dE and dT as limits, not
   numbers. We know that the following is true: given a small
   temperature difference :math:`\Delta T` the flux difference
   :math:`\Delta E` is aproximately:

.. math::  \Delta E \approx  \frac{dE}{dT} \Delta T =  4 \sigma T^3 \Delta T 

i.e. -- change in x times slope = change in y.

This equation in words is called a "first order Taylor series expansion"
of the function :math:`E = \sigma T^4`. It is not exact, but it gets
better as :math:`\Delta T` gets smaller. We can make it exact by writing
out the whole Taylor series expansion which is a power series with an
infinite number of terms. (See the Wikipedia entry
`here <https://en.wikipedia.org/wiki/Taylor_series>`__)

4) What is a differential?

Roughly, the differentials dE and dT represent limits that are evaluated
by integration:

:math:`dT = \lim{\  \Delta T \to 0}`, so that
:math:`\int dT = T` and

.. math::  dE = \lim_{ \Delta T \to 0} \Delta E

So if we take the :math:`\lim{\  \Delta T \to 0}` we can write

.. math:: dE = \frac{d \sigma T^4}{dT} dT = 4 \sigma T^3 dT

Note that this is just doing the steps in Stull p. 38 in the opposite
order. He starts with my last equation and winds up with 3). The
advantage of the alternative approach we're using here is that we don't
need to treat the function :math:`\frac{dE}{dT}` as if it can be ripped
apart to get :math:`dE` and :math:`dT`. If you really care, I recommend
reading `this
answer <http://math.stackexchange.com/questions/23902/what-is-the-practical-difference-between-a-differential-and-a-derivative>`__
to a question about differentials. This is also closely related to the
`chain rule <https://en.wikipedia.org/wiki/Chain_rule>`__ for
derivatives of functions.

By taking the limit as :math:`\Delta T` approaches 0 we've turned a
*difference equation* for the number :math:`\Delta E` (which we can
solve in python) into a *differential equation* for the differential
:math:`dE` (which we can integrate using calculus).

Beers law -- using differentials
================================

Both physics (Maxwell's equations) and observations show that when a
narrow beam of photons are travelling through a material (like air or
water) of constant composition, the flux obeys "Beer's law":

.. math::  E(s) = E_i \exp (-n b s) 

where :math:`s\ (m)` is the distance travelled (the path length),
:math:`n\ (\#/m^3)` is the number denstiy of reflecting/absorbing
particles and :math:`b\ (m^2)` is the extinction cross section due to
both absorption and scattering. You can think of :math:`b` as the
*target size* of the particles (molecules, smoke particles etc.) which
may be much different than the physical size of the particle because of
quantum mechanical and wave interference effects.

To get the differential version of Beers law, take the derivitive and
use the limit argument we went through above and get:

.. math:: dE = E_i (-nb) \exp(-nbs) ds =  (-nb) E ds

or

.. math:: \frac{dE}{E} = -n b ds

If we define the differential optical depth as:

.. math:: d\tau = n b ds

.. raw:: html
         
     <a name="diffbeers"></a>
          
Then we ge:


.. math:: \frac{dE^\prime}{E^\prime} = d \ln E^\prime = -d \tau^\prime
  :label: diffbeers
          
and integrating from :math:`\tau^\prime=0,\ E^\prime=E_i` to
:math:`\tau^\prime = \tau,E^\prime = E` gives:

.. math:: \int_{E_i}^E  d \ln E^\prime = -\int_0^\tau d\tau^\prime

.. math:: \ln \left ( \frac{E}{E_i} \right ) = - \tau

.. math:: E = E_i \exp (-\tau) 

          
which is stull 2.31c. An important point is that the extinction cross
section :math:`b` can vary enormously over small wavlength ranges
(called "absorption bands") where the cross section can increase by a
factor of 100,000. This is why small concentrations of carbon dioxide
have such large impacts on climate.

Also note that now that we have the differential form of Beer's law, we
don't have to assume that :math:`n` or :math:`b` are constant, we can
make them depend on position and just do the (more complicated) integral
to get :math:`\tau`

