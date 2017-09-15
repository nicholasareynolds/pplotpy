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
from pplotpylib.distributions import SupportedDistributions 
from pplotpylib.distributions import Quantiles 


epilogue = \
"""pplotpy Copyright (C) 2017 Nicholas A. Reynolds

This software is licensed under the GNU General Public License, v3.0
This program comes with ABSOLUTELY NO WARRANTY; this is free software, and you
are welcome to redistribute it under certain conditions.  For more information,
see the license file at the GitHub repository:
    
https://github.com/nicholasareynolds/pplotpy/blob/master/LICENSE"""

description = \
"""pplotpy probability plotting both (1) to help scientists and
engineers identify the underlying distribution for his or her set of random
samples, and (2) to predict the values of the parameters in that distribution."""

parser = ArgumentParser(description=description,
                        epilogue=epiloge,
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
                    help='specify value of the location parameter; only valid for some distribution')

if __name__ == "__main__":
    options = parser.parse_args()
    if options.cliBool == True:
        import os
        if options.samplesFile == None:
            raise("Error: a samples file must be specified if '--cli' is invoked")
        else:
            path = os.path.abspath(options.samplesFile)
            if not os.path.exists(path):
                raise("Error: specified file does not exist")
            elif not path.endswith('csv'):
                raise("Error: samples file must be in *.csv format")
            else:
                import numpy as np
                samples_tmp = np.loadtxt(path, delimiter=',')
                samples = samples_tmp.flatten()
            
        
    else:
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())


parser.parse_args