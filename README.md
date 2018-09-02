# HET_observability

This is a simple tool to plot your targets against available HET queue time in a given trimester

How to do it:

0. Download/fork/whatever this repository.
1. Add your targets to the file: PI_targets.dat
2. Edit the beginning of three_lines_PI.py to set the current trimester/year of interest (c_t and c_y).
3. Run three_lines_PI.py, which produces LST_VISITS_PI_20XX-X.pdf
    This histogram shows your targets and the available visits for all, grey+dark, and dark time.
