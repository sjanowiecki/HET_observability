# HET_observability

This is a simple tool to plot your targets against available HET queue time in a given trimester

How to do it:

1. clone this repository with:
     git clone https://github.com/sjanowiecki/HET_observability/
   Then cd into the directory HET_observability/

2. Replace the example target data in PI_targets.dat with yours.
      RA,Dec(J2000) in decimal degrees, exposure time in seconds, and N visits

3. Edit the beginning of HET_obs.py to set the desired trimester (c_t and c_y).

4. Run HET_obs.py via:
       python HET_obs.py

   which will produce LST_VISITS_PI_20XX-X.pdf.
   This histogram shows the visits required for your targets
      and the available visits for all, grey+dark, and dark time.
