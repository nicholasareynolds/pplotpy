# pplotpy


Probability PLOT PYthon is a package that will help a user in identifying the probabilistic distribution to which a set of data belongs.  Probability plotting is a powerful method for quantifying goodness-of-fit.  pplotpy accepts a user-supplied set of samples, calculates the associated quantiles through order statistic operations, and estimates the values of distribution parameters for user-specified distributions. pplotpy is available both as a GUI and through a command line interface. 

Probability plotting is advantageous over other goodness-of-fit tests in certain respects.  Unlike with Chi-Square, probability plotting does not require that the samples be sorted into  not binned into bins.  Unlike with Kolmogerov-Smirnov wherein the values of a candidate distribution's parameter must be known a priori, the samples can be used to estimate the values of those parameters in probability plotting.  Lastly, unlike with Anderson-Darling, probability plotting does not depend on pre-tabulated values specific to each distribution and significance level.  Instead, probability plotting relies on the cumulative distribution function (CDF) of a distribution.  

Qunatile values computed from the samples, are used as estimates of the CDF. and the sample values are used as the argument.  The pairs of values are transformed through the sample algebraic operations necessary to transform the CDF equation into a linear equation.  The values are the distribution parameters are then estimated through a simple linear regression.

Written in:
    - Python 3.6

Required libraries:

- PyQT5

- numpy

- matplotlib
