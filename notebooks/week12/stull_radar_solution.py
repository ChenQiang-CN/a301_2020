# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     notebook_metadata_filter: all,-language_info,-toc,-latex_envs
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.1-dev
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import numpy as np
from numpy import log10
from numpy.testing import assert_almost_equal


# %%
class radar(object):
   #class variables
   R1=2.17e-10#range factor, km, Stull 8.25
   Pt=750.e3 #transmitted power, W, stull p. 246
   b=14255 #equipment factor, Stull 8.26
   Z1=1 #mm^6/m^3
   a1_rain=0.017  #mm/hour in Stull 8.29
   a2_rain=0.0714  #dbZ^{-1} in Stull 8.29
   a3_rain=300  #sutll 8.30
   a4_rain=1.4  #Stull 8.30   Z=300*RR**1.4
   a1_snow=0.02236   #(1/2000.)**0.5
   a2_snow=0.5   #RR=(1/2000)**0.5*Z**0.5
   a3_snow=2000  #day 28 problem set
   a4_snow=2   #dsay 28 problem set  #Z=2000*RR**2.
   
   def __init__(self,R,K2,La):
       """initialize scan values
         
        parameters
        ----------
         Pr: returned power
         R:  range (km)
         K2:  squared refractive index (unitless)
         La:  attenuation (number >= 1)
       """
       self.R=R
       self.K2=K2
       self.La=La
   
   def finddbz(self,Pr):
       """calculate dbZ using Stull 8.28
          with Pr the returned power in Watts
       """
       dbZ=10.*log10(Pr/radar.Pt) + 20.*log10(self.R/radar.R1) - \
           10.*log10(self.K2/self.La**2.) - 10.*log10(radar.b)
       return dbZ
   
   def findPr(self,Z):
       """
        stull eqn 8.23 -- returns Pr in W given Z in
        mm^6/m^3
       """ 
       Pr=radar.Pt*radar.b*self.K2/self.La**2.*(radar.R1/self.R)**2.*Z
       return Pr
       
   def findRR_snow(self,dbZ):
       """
        find the rain rate in mm/hr using Stull 8.29
        dbZ:  reflectivity in dbZ referenced to 1 mm^6/m^3
       """
       Z=10**(dbZ/10.)
       RR=radar.a1_snow*Z**radar.a2_snow
       return RR


   def findZ_snow(self,RR):
       """
         find the reflectivity in mm^6/m^3
         give the RR in mm/hr using Stull 8.30
         and assuming liquid phase
       """
       Z=radar.a3_snow*RR**radar.a4_snow
       return Z

   def findRR_rain(self,dbZ):
       """
        find the rain rate in mm/hr using Stull 8.29
        dbZ:  reflectivity in dbZ referenced to 1 mm^6/m^3
       """
       RR=radar.a1_rain*10**(radar.a2_rain*dbZ)
       return RR
  
   def findZ_rain(self,RR):
       """
         find the reflectivity in mm^6/m^3
         give the RR in mm/hr using Stull 8.30
         and assuming liquid phase
       """
       Z=radar.a3_rain*RR**radar.a4_rain
       return Z


# %%
def test_dbz():
    """Demonstrate an automatic test of the radar class
       This is a "roundtrip" test of the findPr method
       Run this at the command line by typing
       > nosetests day28_radar.py
    """
    Z=1.e4  #Z of 40 dbZ
    R=20    #range of 20 km
    K2=0.93  #liquid water
    La=1   #no attenuation
    test1=radar(R,K2,La)
    power_watts=test1.findPr(Z)
    dbZ=test1.finddbz(power_watts)
    assert_almost_equal(dbZ,40,decimal=5)


# %%
if __name__=="__main__":
   #stull p. 246 sample appliation
   # given
   Z=1.e4  #Z of 40 dbZ
   R=20    #range of 20 km
   K2=0.93  #liquid water
   La=1   #no attenuation
   test1=radar(R,K2,La)
   power_watts=test1.findPr(Z)
   dbZ=test1.finddbz(power_watts)
   the_text="""
               Stull problem on p. 246: start with 40 dbZ at 20 km and
               find Pr:
               Here is the Pr: {0:10.5g} Watts
               Here is  dbm -- decibels re 1 mWatt: {1:5.3f},
               Check: do we get back 40 dbZ?  answer is: {2:5.2f} dbZ
            """ 
   print(the_text.format(power_watts,10*log10(power_watts*1.e3),dbZ))

   #
   # problem 2
   #
   the_text="""
               Day 28 problem 2a: start with -58 dbm at 100 km and
               find dbZ:
               Here is the Pr: {0:10.5g} Watts
               Here is  dbm -- decibels re 1 mWatt: {1:5.3f}
               Check: do we get back 45 dbZ?  answer is: {2:5.2f} dbZ
               The rain rate at {2:5.2f} dbZ is {3:5.2f} mm/hr
            """ 
   dbm=-58.
   Pr=10**(dbm/10.)*1.e-3  #-58 dbm returned power in Watts
   R=100  #range in km
   K2=0.93  #liquid water
   La=1   #no attenuation
   prob2a=radar(R,K2,La)
   dbz=prob2a.finddbz(Pr)
   RR=prob2a.findRR_rain(dbz)
   print(the_text.format(Pr,dbm,dbz,RR))

   #Now assume the same Pr came from a snow storm
   #with no attenuation
   K2=0.208  #snow (Stull, p. 245)
   La=1   #no attenuation
   R=100  #km
   prob2b=radar(R,K2,La)
   dbz=prob2b.finddbz(Pr)
   RR=prob2b.findRR_snow(dbz)
   the_text="""
               Day 28 problem 2b: keep the power at Pr, but change K2 to snow
               and find the new  dbZ:
               Here is the Pr: {0:10.5g} Watts
               Here is  dbm -- decibels re 1 mWatt: {1:5.3f}
               If this was snow then the reflectivity is: {2:5.2f} dbZ
               The snow rate at {2:5.2f} dbZ is {3:5.2f} mm liquid equivalent/hr
            """ 
   print(the_text.format(Pr,dbm,dbz,RR))

   K2=0.93 #rain (Stull, p. 245)
   La=2   #factor of 2 attenuation
   R=100  #km
   prob2c=radar(R,K2,La)
   dbz=prob2c.finddbz(Pr)
   RR=prob2b.findRR_rain(dbz)
   the_text="""
               Day 28 problem 2c: keep the power at Pr, set K2 to rain
               but find the new reflectivity assuming La=2:
               Here is the Pr: {0:10.5g} Watts
               Here is  dbm -- decibels re 1 mWatt: {1:5.3f}
               If there was a factor of 2 one-way attenuation the reflectivity is: {2:5.2f} dbZ
               The rain rate at {2:5.2f} dbZ is {3:5.2f} mm/hr
            """ 
   print(the_text.format(Pr,dbm,dbz,RR))

# %%
