pplotpy - a probability plotting tool for Python

pplotpy is licensed under the GNU GPL v3 license.  Please see the LICENSE file at https://github.com/nicholasareynolds/pplotpy .

Probability PLOT PYthon is a package that will help a user in identifying the probabilistic distribution to which a set of data belongs.  pplotpy accepts a user-supplied set of samples, calculates the associated quantiles through order statistic operations, and estimates the values of distribution parameters for user-specified distributions. pplotpy is available both as a GUI and through a command line interface.

Probability plotting is a powerful method for quantifying goodness-of-fit with several advantages over other goodness-of-fit tests.  Unlike with the Chi-Square goodness-of-fit test, probability plotting does not require that the samples be grouped into bins.  Unlike with Kolmogerov-Smirnov goodness-of-fit test, wherein the values of a candidate distribution's parameter must be known a priori, the samples can be used to estimate the values of those parameters in probability plotting.  Lastly, unlike with Anderson-Darling goodness-of-fit test, probability plotting does not depend on pre-tabulated values specific to each distribution and significance level.  

Instead, probability plotting relies on the cumulative distribution function (CDF) of a distribution, with quantile values computed from the samples being used as the CDF values.  The pairs of values are transformed through the sample algebraic operations necessary to transform the CDF equation into a linear equation.  The values are the distribution parameters are then estimated through a simple linear regression.

Supported Distributions:
- Normal

- Lognormal

- Exponential

- Extreme Value, Type I

- Weibull

- Logistic

- Uniform

Written in:
- Python 3.6

Required libraries:

- PyQT5

- numpy

- matplotlib
