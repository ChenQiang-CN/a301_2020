.. default-role:: math

.. _mid_review1:

Sample mid-term questions I
===========================

Beers law
---------

Stull page 2.43 and the :ref:`beers_law` reading:

#. Prove that for a thin  non-reflecting layer the change in emissivity
   =  change in optical thickness, i.e. prove that:

   .. math::
      :label: thin
              
         \Delta e_\lambda \approx  \Delta \tau_\lambda



#. Repeat the problem above, but for a layer with an optical depth of `\tau_\lambda=1`.
   How does that change :eq:`thin` ?


#. Suppose you put ozone molecules in a 1 km long tunnel and measure an optical thickness of
   0.5 using an ultraviolet laser.  You know that the ozone mixing ratio is 1 g/kg and the air
   density is 1 kg/`m^3`.  What is the extinction coefficient `k` in `m^2/kg`?


#. Find the narrow beam transmission, absorption and emission for a series of
   stacked layers of equal transmissivities and temperatures in a direction perpendicular to the layers:

   **Answer:**

   Consider 3 layers each with direct beam transmissivity
   `\hat{t} = \frac{E}{E_0} = \frac{L \Delta \omega}{L_0 \Delta \omega} = \frac{L}{L_0}`.
   The outgoing radiance from one layer is the
   incoming radiance from the next layer, so that

   .. math::

       L_3 = \hat{t} L_2 \\
       L_2 = \hat{t} L_1 \\
       L_1 = \hat{t} L_0


   and substituting in turn:

 
   .. math::
       
      L_3 = \hat{t}^3 L_0

   The amount absorbed is
     
   `(L_3 - L_0 = (1 - \hat{t^3}) L_0` so the absorptivity is
   `(1 - \hat{t}^3)` which by Kirchoff’s law is the emissivity. The
   emission is therefore:

   .. math::
      
    L = \left ( 1 - \hat{t}^3 \right ) \frac{\sigma}{\pi} T^4

   and the transmitted radiance is `\hat{t}^3 L_0`

   Note that this only works if all layers are the same temperature.  (Why?)

   **Answer:**

   We are solving the emission part of the Schwartzchild equation:

   .. math::
      
      L_{emitted} = \int B(T) d\hat{t}

   If `B(T)` is constant it can come out of the integral and we have:

   .. math::

      \begin{aligned}
      L_{emitted} &= B(T) \left . \hat{t} \right |_{t_{tot}}^1 \\
                  &= B(T)(1 - t_{tot})=B(T)(1 - \hat{t}^3)
      \end{aligned}

   which is the answer we got.  If B(T) changed with the layer, then we'd
   need that information in the integration to get the emitted radiance.


   Note also that this only works if the beam is going straight through the layers
   (i.e. not a slant path)  (Why? How would this change for a slant path?)

   **Answer:**

   For the slant path we would need to replace the vertical optical thickness:

   .. math::

      d \tau =  \kappa_\lambda \rho_g dz

   with the slant path optical thickness `\tau_s`:

   
   .. math::

      d \tau_s =  \kappa_\lambda \rho_g ds = \kappa_\lambda \rho_g dz/\cos \theta
      = \kappa_\lambda \rho_g dz/\mu

   Once we made that change, everything would work as before, just with a
   smaller transmittance due to the longer slant path for `\mu < 1`.
   
Solid angle and radiance
------------------------

From :ref:`radiance` reading:


#. Calculate the solid angle subtended by a cone with an angular width of
   `\Delta \theta` =20 degrees.

   **Answer**
   
   .. math::
      :label: solid
         
       \omega &= \int_0^{2\pi} \int_0^{10} \sin \theta d\theta d\phi = -2\pi (\cos(10) - \cos(0)) \\
        &= 2\pi (1 - \cos(10)) = 2\pi(1 - 0.985) = 0.0954\ sr


#. A laser pointer subtends the same solid angle as the sun: `7 \times 10^{-5}` sr.  You shine it at a wall that is 10 meters away.  What is the radius of the circular dot?


#.  What is the angle of the cone if `\omega = 7. \times 10^{-5}\ sr`?


#. A satellite orbits 800 km above the earth and has a telescope with a field of view
   that covers 1 `km^2` directly below (i.e. at nadir).  If that 1 `km^2` is ocean with
   an emissivity `e=1` at a temperature
   of 280 K, calculate the flux in `W\,m^2` reaching the satellite from all wavelengths
   from that pixel.


      
Flux from radiance
------------------

From :ref:`flux_from_radiance`:
   

#. Calculate the flux arriving at a sensor assuming a constant radiance and a field of view
   that is a cone with an angular width of `\Delta \theta` =20 degrees.

      
#. Prove that for an infinite flat surface the emitted radiance and flux are related by:

   .. math::

      E_\lambda = \pi L_\lambda

      
#. Suppose that a satellite's orbit changes from a height of 800 km to a height of 600 km
   above the surface.  If the telescope field of view stays the same, prove that
   the radiance stays constant.
   



Schwartzchild equation
----------------------

From Stull p. 224 and the :ref:`schwartz` reading:

#.  Show that `e_\lambda` = `a_\lambda` for a gas that absorbs and transmits but doesn't reflect.
    (hint:  put the gas between two black plates, assume that the gas and the plates are at the
    same temperature and show that the 2nd law is violated if `e_\lambda \neq a_\lambda`


   
#. Integrate the Schwartzchild equation
   
   .. math::

      \begin{gathered}
          \label{eq:sch1}
           dL_{\lambda,absorption} + dL_{\lambda,emission}  = -L_\lambda\, d\tau_\lambda + B_\lambda (T_{layer})\, d\tau_\lambda
        \end{gathered}

   across a constant temperature layer of thickness `\Delta \tau_\lambda` over a surface
   emitting radiance `L_{\lambda 0}`
   and show that the radiance at the top of a constant temperature layer is given by:        

   .. math::

      \begin{gathered}
      L_\lambda = L_{\lambda 0} \exp( -\Delta \tau_\lambda  ) + B_\lambda (1- \exp( -\Delta \tau_\lambda))\end{gathered}

