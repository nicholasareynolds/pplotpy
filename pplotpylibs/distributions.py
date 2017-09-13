###############################################################################
#
#    pplotpy - a probability plotting tool for Python
#
#    Copyright (C) 2017,  Nicholas A. Reynolds
#
#    License Summary:
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Full License Available in LICENSE file at
#    https://github.com/nicholasareynolds/pplotpy
#
###############################################################################

from scipy import stats
from scipy.special import erfinv
from quantiles import Quantiles

import numpy as np

class CandidateDistributions:
    """
    Organize the candiate distribution objects for probability plotting.

    The main attribute of CandidateDistributions is the list 'dists'.  User-
    specified distributions for consideration are added to and removed from
    this list.  This list also serves as an iterable item when data and/or
    quantile calculation method are changed.
    """
    
    def __init__(self):
        """initialize the emtpy list for 'dists'"""

        self.dists = list()

        
    def add_distribution(self, dist_obj, samples, qmethod_str):
        """Store samples to dist_obj, compute values, and append to 'dists' """

        self._calc_results(dist_obj, samples, qmethod_str)
        self.dists.append(dist_obj)


    def _calc_results(self, dist_obj, samples, qmethod_str):
        """Store samples; calc. quantiles, perform regression for dist_obj."""

        dist_obj.feed_samples(samples)
        dist_obj.calc_quantiles(qmethod_str)
        dist_obj.eval_data()


    def calc_all(self, samples, qmethod_str):
        """Perform prob. plot calcs for all distributions in self.dists."""
        for dist_obj in self.dists:
            self._calc_results(dist_obj, samples, qmethod_str)


    def get_count(self):
        """Return the number of candidate distributions in self.dists"""

        return len(self.dists)


    def get_obj(self,index):
        """Get distribution object using its index in the list."""

        return self.dists[index]


    def remove_all(self):
        """Empty the list of candidate distributions."""

        self.dists = list()
        
    def remove_dist(self, dist_index):
        """Remove candidate distribution by its index in self.dists."""
        
        self.dists.pop(dist_index)



class SupportedDistributions():
    """
    Register, instantiate, and define methods for supported distributions.
    """

    subclasses = {}  # Empty container for distributions to be registered at

    
    def __init__(self, label):
        """Preserve tag/label of distribution as attribute self.label"""

        self.label = label


    # Decorator to store distrib. subclass and its label to self.sublasses
    @classmethod
    def register_distribution(cls, dist_str):
        def decorator(subclass):
            cls.subclasses[dist_str] = subclass
            return subclass
        return decorator
    

    # Decorator to instantiate a distribution object from its label.
    @classmethod
    def create_subclass_instance(cls, dist_str):
        if dist_str not in cls.subclasses:
            raise ValueError("Invalid distribution: %s" %dist_str)
        return cls.subclasses[dist_str](dist_str)


    # Decorator to return the value of the location parameter, if it exists
    @classmethod
    def has_optional_loc_param(cls, dist_str):
        if dist_str not in cls.subclasses:
            raise ValueError("Invalid distribution: %s" %dist_str)
        return cls.subclasses[dist_str](dist_str).loc_optional  

    def feed_samples(self, samples):
        self.samples = np.sort(samples)
        self.nsamples = np.size(samples)

    def get_label(self):
        return self.label

    def set_location(self, loc):
        if self.has_loc:
            self.loc = loc

    def get_scale_str(self):
        if self.has_scale:
            return str(self.scale)
        else:
            return "NA"
    
    def get_loc_str(self):
        if self.has_loc:
            return str(self.loc)
        else:
            return "NA"
        

    def get_shape_str(self):
        """Return shape parameter value as a string if dist has a shape param."""
 
        if self.has_shape:
            return str(self.shape)
        else:
            return "NA"

    def calc_results(self, samples, qmethod_str):
        self.feed_samples(samples)
        self.calc_quantiles(qmethod_str)
        self.set_location(loc)
        self.eval_data()
        
    def get_coeff_of_determ_str(self):
        return str(self.r2)

    def eval_data(self):
        self._pplot_transform_data()
        self._linear_regression()
        self.extract_pplot_regress_quantities()

    def _linear_regression(self):
        self.slope, self.intercept, r_value, pvalue, stderr = \
            stats.linregress(self.x, self.y)
        self.r2 = r_value**2.0

    def create_pplot(self, axes):
        liny = lambda x: self.slope * x + self.intercept
        xmin, xmax = np.min(self.x), np.max(self.x)
        ymin, ymax = liny(xmin), liny(xmax)
        axes.plot(self.x,
                 self.y,
                 'ro',
                 label="Samples")
        axes.plot([xmin, xmax],
                 [liny(xmin), liny(xmax)],
                 '-k',
                 label="Regression")
        eq = "f(t) = %6.4E*t +  %6.4E\n$R^2$=%.4f" \
            % (self.slope, self.intercept, self.r2)
        axes.text(0.1*xmax + 0.9*xmin,
                 0.1*ymin + 0.9*ymax,
                 eq)
        axes.set_xlabel("t = " + self.xlabel)
        axes.set_ylabel("f(t) = " + self.ylabel)
        axes.set_title(self.label)
        axes.legend(loc=4)
        axes.grid(which='major')
        

    def calc_quantiles(self, method):
        n = self.nsamples
        self.quantiles = \
            Quantiles.create_subclass_instance(method)().get_quantiles(n)

@SupportedDistributions.register_distribution("Normal")    
class Normal(SupportedDistributions):
    pdf_eq = "$f_{X}(x) = \frac{1}{\sqrt{2\pi\sigma}}e^{-\frac{\left(x-\mu\right)^2}{2\sigma^2}}$"
    scipy_name = "norm"
    has_shape = False
    has_loc = True
    has_scale = True
    loc_optional = False
    xlabel = r"$erf^{-1}\left[2F_X(x)-1\right]$"
    ylabel = r"$x$"
        
    def _pplot_transform_data(self):
        self.x = erfinv((2.0 * self.quantiles) - 1.0)
        self.y = self.samples

    def extract_pplot_regress_quantities(self):
        self.scale = self.slope   # stdev
        self.loc = self.intercept # mean
        
    def _make_dist_obj(self):
        self.dist_obj = stats.norm(loc=self.loc,
                                   scale=self.scale)
        
    def clear(self):
        self.scale = None
        self.loc = None
    
@SupportedDistributions.register_distribution("Lognormal")    
class Lognormal(SupportedDistributions):
    scipy_name = "lognorm"
    has_shape = True
    has_loc = True  # can be specified, default 0
    has_scale = True
    loc_optional = True
    xlabel = r"$erf^{-1}\left[F_X(x)\right]$"
    ylabel = r"$\ln(x)$"
    
    def _pplot_transform_data(self):
        self.x = erfinv(self.quantiles)
        self.y = np.log(self.samples - self.loc)

    def extract_pplot_regress_quantities(self):
        self.shape = self.slope * np.log(10)
        self.scale = self.intercept # mean

    def _make_dist_obj(self):
        self.dist_obj = stats.lognorm(self.shape,
                                      loc=self.loc,
                                      scale=self.scale) 
    def clear(self):
        self.scale = None
        self.shape = None

@SupportedDistributions.register_distribution("Exponential") 
class Exponential(SupportedDistributions):
    scipy_name = "expon"
    has_scale = True
    has_loc = True # can be specified, default 0
    has_shape = False
    loc_optional = True
    xlabel = r"$x$"
    ylabel = r"$\ln\left(\frac{1}{1-F_X(x)}\right)$"
    
    def _pplot_transform_data(self):
        self.x = self.samples - self.loc
        self.y = np.log(1.0 / (1.0 - self.quantiles))

    def extract_pplot_regress_quantities(self):
        self.scale = 1.0 / self.slope
        
    def _make_dist_obj(self):
        self.dist_obj = stats.expon(loc=self.loc,
                                    scale=self.scale) 
    def clear(self):
        self.scale = None
        
@SupportedDistributions.register_distribution("Weibull") 
class Weibull(SupportedDistributions):
    scipy_name = "frechet_r"
    has_scale = True
    has_shape = True 
    has_loc = True # can be specified, default = 0
    loc_optional = True
    xlabel = r"$\ln(x)$"
    ylabel = r"$\ln\left[\ln\left(\frac{1}{1-F_X(x)}\right)\right]$"
        
    def _pplot_transform_data(self):
        self.x = np.log(self.samples - self.loc)
        self.y = np.log(np.log(1.0 / (1.0 - self.quantiles)))

    def extract_pplot_regress_quantities(self):
        self.shape = self.slope
        self.scale = np.exp(-1.0 * self.intercept/ self.slope)

    def _make_dist_obj(self):
        self.dist_obj = stats.frechet_r(self.shape,
                                        loc=self.loc,
                                        scale=self.scale) 

    def clear(self):
        self.scale = None
        self.shape = None
        
@SupportedDistributions.register_distribution("Extreme Value, Type I")
class ExtremeValueTypeI(SupportedDistributions):
    scipy_name = "gumbel_l"
    has_shape = False
    has_loc = True
    has_scale = True
    loc_optional = False
    xlabel = r"$x$"
    ylabel = r"$\ln\left[-\ln\left(1-F_X(x)\right)\right]$"

    def _pplot_transform_data(self):
        self.x = self.samples
        self.y = np.log(-1.0 * np.log(1.0 - self.quantiles))

    def extract_pplot_regress_quantities(self):      
        self.scale = 1.0 / self.slope
        self.loc = 1.0 * self.intercept * self.slope
        
    def _make_dist_obj(self):
        self.dist_obj = stats.gumbel_l(loc=self.loc,
                                       scale=self.scale) 

    def clear(self):
        self.scale = None
        self.loc = None

@SupportedDistributions.register_distribution("Logistic")
class Logistic(SupportedDistributions):
    name = "Logistic"
    scipy_name = "logistic"
    has_shape = False
    has_loc = True
    has_scale = True
    loc_optional = False
    xlabel = r"$\tanh^{-1}\left(2*F_X{x}-1\right)$"
    ylabel = r"$x$"

    def _pplot_transform_data(self):
        self.x = np.arctanh(2.0*self.quantiles - 1)
        self.y = self.samples

    def extract_pplot_regress_quantities(self):      
        self.scale = 0.5 * self.slope
        self.loc = self.intercept

    def clear(self):
        self.scale = None
        self.loc = None
        
@SupportedDistributions.register_distribution("Uniform")
class Uniform(SupportedDistributions):
    scipy_name = "uniform"
    has_shape = False
    has_loc = True
    has_scale = True
    loc_optional = False
    xlabel = r"$F_X{x}$"
    ylabel = r"$x$"

    def _pplot_transform_data(self):
        self.x = self.quantiles
        self.y = self.samples

    def extract_pplot_regress_quantities(self):      
        self.scale = self.slope
        self.loc = self.intercept        

    def clear(self):
        self.scale = None
        self.loc = None

