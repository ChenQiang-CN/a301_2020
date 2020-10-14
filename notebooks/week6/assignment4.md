(assignment4)=
# Assignment 4

Add cells to {ref}`scale_heights`

1\.  Print out the density and pressure scale heights for each of the five soundings

2\.  Define a function that takes a sounding dataframe and returns the "total precipitable water", which is defined as:

$$W = \int_0^{z_{top}} \rho_v dz $$

Do a change of units to convert $kg\,m^{-2}$ to $cm\,m^{-2}$ using the density of liquid water (1000 $kg\,m^{-3}$) -- that is, turn the kg of water in the 1 square meter column into cubic meters and turn that into $cm/m^{-2}$

3\.  Use your function to print out W for all five soundings
