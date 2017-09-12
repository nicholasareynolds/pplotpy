"""
    pplotpy - a probability plotting tool for Python

    Copyright (C) 2017,  Nicholas A. Reynolds

    License Summary:
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Full License Available in LICENSE file at
    https://github.com/nicholasareynolds/pplotpy
"""

from numpy import zeros, array

class Quantiles():
    subclasses = {}
    
    @classmethod
    def register_method(cls, method_str):
        def decorator(subclass):
            cls.subclasses[method_str] = subclass
            return subclass
        return decorator
    
    @classmethod
    def create_subclass_instance(cls, method_str):
        if method_str not in cls.subclasses:
            raise ValueError("Invalid distribution: %s" % method_str)
        return cls.subclasses[method_str]

@Quantiles.register_method("Filliben")
class Filliben(Quantiles):
    
    def get_quantiles(self, n):
        quantiles = zeros(n)
        quantiles[0] = 1.0 - ( 0.5**(1.0/n ) )
        quantiles[-1] =0.5**(1.0/n)
        quantiles[1:n] = [(ii + 1.0 - 0.3175) / (n + 0.365) for ii in range(1,n)]
        return quantiles

@Quantiles.register_method("i/(N+1)")
class NPlus1(Quantiles):
    
    def get_quantiles(self, n):
        quantiles = array([(ii+1.0)/(n+1.0) for ii in range(n)])
        return quantiles

@Quantiles.register_method("(i-0.5)/N")
class IMinusHalf(Quantiles):
    
    def get_quantiles(self, n):
        quantiles = array([(ii + 0.5)/n for ii in range(n)])
        return quantiles

@Quantiles.register_method("Median Rank")
class MedianRank(Quantiles):
    
    def get_quantiles(self, n):
        quantiles = array([(ii + 0.7)/(n+0.4) for ii in range(n)])
        return quantiles
