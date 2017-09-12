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