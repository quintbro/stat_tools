# statstools
This is a repository with code that assists with doing statistical analysis in Python. Many of the functions here were made to replicate R Functions.

# Installation
```
pip install git+https://github.com/quintbro/stat_tools.git
```

## car.py
This file contains a function for making added variable plots, similar to car::avPlots() in R

## exponential_variance.py
This file contains a class for generating weights using an exponential variance function, similar to nlme::varExp() in R

## spatial.py
This file contains a function moranBasis() that generates spatial basis functions for Areal Spatial Regression

## patchwork.py
This file contains a class that replicates the patchwork package in R. It allows the user to combine 
plotnine, and matplotlib plots in grids using + and / syntax
