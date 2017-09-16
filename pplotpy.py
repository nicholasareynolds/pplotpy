################################################################################
#
#    pplotpy - a probability plotting tool for Python
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
################################################################################

import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from pplotpylibs.quantiles import Quantiles 
from pplotpylibs.distributions import SupportedDistributions 


epilog = \
"""pplotpy Copyright (C) 2017 Nicholas A. Reynolds

This software is licensed under the GNU General Public License, v3.0
This program comes with ABSOLUTELY NO WARRANTY; this is free software, and you
are welcome to redistribute it under certain conditions.  For more information,
see the license file at the GitHub repository:
    
https://github.com/nicholasareynolds/pplotpy/

"""

description = \
"""pplotpy probability plotting both (1) to help scientists and
engineers identify the underlying distribution for his or her set of random
samples, and (2) to predict the values of the parameters in that distribution.

"""

parser = ArgumentParser(description=description,
                        epilog=epilog,
                        formatter_class=RawTextHelpFormatter)

parser.add_argument('--cli',
                    dest='cliBool',
                    action='store_true',
                    default=False,
                    help='execute pplotpy from the command line')

parser.add_argument('-i',
                    dest='samplesFile',
                    action='store',
                    default=None,
                    help='specify the *.csv file containing the samples')

parser.add_argument('-d',
                    dest='Distribution',
                    action='store',
                    default=None,
                    choices=list(SupportedDistributions.subclasses.keys()),
                    help='specify the candidate distribution')

parser.add_argument('-q',
                    dest='QuantileMethod',
                    action='store',
                    choices=list(Quantiles.subclasses.keys()),
                    default = "Filliben",
                    help='specify the quantile computational method')
                    
parser.add_argument('--loc',
                    dest='Location',
                    action='store',
                    type=float,
                    default=0.0,
                    help='specify value of the location parameter; only valid for some distributions')

parser.add_argument('--plot',
                    dest='plotBool',
                    action='store_true',
                    default=False,
                    help='show the probability plot')


if __name__ == "__main__":
    options = parser.parse_args()
    
    # Execute from command line
    if options.cliBool == True:
        import os

        # Distribution
        if options.Distribution == None:
            print("Error: a valid distribution must be specified")
            sys.exit()
        else:
            dist_obj = \
                SupportedDistributions.create_subclass_instance(options.Distribution)
        
        # Load Samples
        if options.samplesFile == None:
            print("Error: a samples file must be specified if '--cli' is invoked")
            sys.exit()
        else:
            path = os.path.abspath(options.samplesFile)
            if not os.path.exists(path):   # File must exist
                print("Error: specified file does not exist")
                sys.exit()
            elif not path.endswith('csv'): # Must be a *.csv
                print("Error: samples file must be in *.csv format")
                sys.exit()
            else:
                import numpy as np
                samples_tmp = np.loadtxt(path, delimiter=',')
                samples = samples_tmp.flatten()
                dist_obj.feed_samples(samples)

        # Quantiles
        dist_obj.calc_quantiles(options.QuantileMethod)
        
        # Location Parameter (if applicable):
        if dist_obj.loc_optional == True:
            dist_obj.set_location(options.Location)
            
        # Perform Linear Regression
        dist_obj.eval_data()
        
        # Print Summary:
        print("\n%4sDistribution: %s" % ("", dist_obj.get_label()))
        if dist_obj.has_shape == True:
            print("%8s%-10s%s" % ('',"Shape:", dist_obj.get_shape_str()))
        if dist_obj.has_scale == True:
            print("%8s%-10s%s" % ('',"Scale:", dist_obj.get_scale_str()))
        if dist_obj.has_loc == True:
            print("%8s%-10s%s"  % ('',"Location:", dist_obj.get_loc_str()))
        print("%8s%-10s%s"  % ('',"R^2:", dist_obj.get_coeff_of_determ_str()),
              end="\n\n")
        
        # Plot
        if options.plotBool == True:
            import matplotlib.pyplot as plt
            plt.close('all')
            fig = plt.figure()
            axes = fig.add_subplot(111)
            dist_obj.create_pplot(axes)
            plt.show()
        
    # GUI Option
    else:
        from PyQt5 import QtWidgets
        from pplotpylibs.pplotpygui import MainWindow
        app = QtWidgets.QApplication(sys.argv)
        ui = MainWindow()
        sys.exit(app.exec_())

