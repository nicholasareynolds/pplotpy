################################################################################
#
#    pplotpy - a probability plotting tool for Python
#    Copyright (C) 2017,  Nicholas A. Reynolds
#
#    Full License Available in LICENSE file at
#    https://github.com/nicholasareynolds/pplotpy
#
################################################################################

from numpy import zeros, array

class Quantiles():
    """Parent class that registers subclasses, which calculate quantiles"""

    subclasses = {}

    
    # Register subclass quantile methods via decorator with a string argument
    @classmethod
    def register_method(cls, method_str):
        def decorator(subclass):
            cls.subclasses[method_str] = subclass
            return subclass
        return decorator

    
    # Instantiate a subclass, based on string argument in a 
    @classmethod
    def create_subclass_instance(cls, method_str):
        if method_str not in cls.subclasses:
            raise ValueError("Invalid distribution: %s" % method_str)
        return cls.subclasses[method_str]


    def get_quantiles(self, n):
        """Return quantile values based on number of samples (and subclass)"""

        pass


@Quantiles.register_method("Filliben")
class Filliben(Quantiles):
    """Calculate quantile values using Filliben's estimate"""


    # Filliben, J. J. (February 1975), The Probability Plot Correlation
    #  Coefficient Test for Normality, Technometrics, pp. 111-117.

    
    def get_quantiles(self, n):
        quantiles = zeros(n)
        quantiles[0] = 1.0 - ( 0.5**(1.0/n ) )
        quantiles[-1] =0.5**(1.0/n)
        quantiles[1:n] = [(ii + 1.0 - 0.3175) / (n + 0.365) for ii in range(1,n)]
        return quantiles


@Quantiles.register_method("i/(N+1)")
class NPlus1(Quantiles):
    """Calculate quantile values based on uniform order statistics"""
    
    # http://www-math.mit.edu/~rmd/650/ordstats-quant.pdf


    def get_quantiles(self, n):
        quantiles = array([(ii+1.0)/(n+1.0) for ii in range(n)])
        return quantiles


@Quantiles.register_method("(i-0.5)/N")
class IMinusHalf(Quantiles):
    """Calculate quantile values according to various texts (see citation)"""

    # http://www.itl.nist.gov/div898/handbook/apr/section2/apr221.htm

    def get_quantiles(self, n):
        quantiles = array([(ii + 0.5)/n for ii in range(n)])
        return quantiles


@Quantiles.register_method("Median Rank")
class MedianRank(Quantiles):
    """Calculate quantile values according to Filliben's method, with rounding"""

    # http://www.itl.nist.gov/div898/handbook/apr/section2/apr221.htm
    # Probably equivalent to Filliben's, but with rounding
    def get_quantiles(self, n):
        quantiles = array([(ii + 0.7)/(n+0.4) for ii in range(n)])
        return quantiles
