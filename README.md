#
*pplotpy*

Probability PLOT PYthon is a tool that will help a user in identifying the probabilistic distribution to which a set of data belongs.  *pplotpy* accepts a user-supplied set of samples, calculates the associated quantiles through order statistic operations, and estimates the values of distribution parameters for user-specified distributions. *pplotpy* is available both as a GUI and through a command line interface.

## Introduction

### Background

Probability plotting is a powerful method for quantifying goodness-of-fit with several advantages over other goodness-of-fit tests.  Unlike with the Chi-Square goodness-of-fit test, probability plotting does not require that the samples be grouped into bins, whose size may impact the goodness-of-fit.  Unlike with Kolmogerov-Smirnov goodness-of-fit test, wherein the values of a candidate distribution's parameter must be known a priori, the samples can be used to estimate the values of those parameters in probability plotting.  Lastly, unlike with Anderson-Darling goodness-of-fit test, probability plotting does not depend on pre-tabulated values specific to each distribution and significance level.  

Instead, probability plotting relies on the cumulative distribution function (CDF) of a distribution, with quantile values computed from the samples being used as the CDF values.  The pairs of values are transformed through the sample algebraic operations necessary to transform the CDF equation into a linear equation.  The values are the distribution parameters are then estimated through a simple linear regression.


## Getting Started

### Prerequisities:

In order to use *pplotpy*, the Python 3 interpreter is needed.  This can be installed directly from python.org, or more conveniently, as part of a bundled package (e.g. [Enthought Canopy](https://www.enthought.com/product/canopy/), [Anaconda](https://www.anaconda.com/download/), etc...)  Furthermore, several supporting libraries are required:

- [SciPy](https://www.scipy.org/)

- [NumPy](http://www.numpy.org/)

- [matplotlib](https://matplotlib.org/)

- [PyQT5](https://pypi.python.org/pypi/PyQt5)

### Setting up *pplotpy*

From the [*pplotpy* GitHub repository](https://github.com/nicholasareynolds/*pplotpy*/) either Clone or download the repository.

Add the destination directory path (destpath) to the PYTHONPATH:

For Unix Systems:

```
export PYTHON=$PYTHONPATH:destpath
```

### Usage

From the command line, enter the command

```
python pplotpy.py [OPTIONS]
```

Where, OPTIONS is a list of command line options.  A complete list can be found by entering the command

```
python pplotpy.py -h
```

NOTE: The command line is used to launch both the command-line interace and the graphical user interface of *pplotpy*.

## Basic Workflow

A user provides a set of samples to *pplotpy* and specifies which method he/she would like to use in computing the quantile values.  The user also specifies which distributions he/she would like *pplotpy* to consider in performing regressions.  The user has the option of specifying the value of a location parameter on certain distributions.  *pplotpy* will then perform a regression analyses on probability-plot transformed data, and optionally display the probability plot.

### Samples

The data must be organized in a comma-separated values (.csv) format.  Samples can be listed on one or more rows and in one or more columns in the file; *pplotpy* will flatten all values into an array.

### Quantiles

Quantiles are computed from the samples based on a number of available options.  These include:
- Filliben [1]
- i/(N+1)
- (i-0.5)/N
- (i-0.3)(N+0.4)

### Supported Distributions:
- [Normal](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html)

- [Lognormal](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html)

- [Exponential](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.expon.html)

- [Extreme Value, Type I](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gumbel_l.html)

- [Weibull](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.frechet_r.html)

- [Logistic](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.logistic.html)

- [Uniform](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.uniform.html)

- [Cauchy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.cauchy.html)

- [Rayleigh](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rayleigh.html)



## Administrative

### License

*pplotpy* is licensed under the MIT License - see the [LICENSE file](https://github.com/nicholasareynolds/*pplotpy*/LICENSE.md).

### Citing/acknowledgement

As a courtesy, please acknowledge *pplotpy* in papers, reports, or publications, for which *pplotpy* was used.

### Contributions

*pplotpy* is by no means a completed project, or limited to contributions by the author.  If you wish to collaborate (or even suggest changes) please contact me ([nicholas.a.reynolds@gmail.com](mailto:nicholas.a.reynolds@gmail.com)).  Currently, there is a general plan to continue to add distributions to the distributions.py file.  

## Acknowledgements
*pplotpy* has not implemented any new scientific concepts; it has merely a methomethodology, that I learned in grad school and is openly available, in what I consider to be a convenient workflow to scientists/engineers who are not regularly involved in uncertainty quantification.

That said, [NIST's Engineering Statistics Handbook](http://www.itl.nist.gov/div898/handbook/index.htm) was an excellent resource in preparing *pplotpy*.  

## References
- [1] Filliben, J. J. (February 1975), The Probability Plot Correlation Coefficient Test for Normality, Technometrics, pp. 111-117.

