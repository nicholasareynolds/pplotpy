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

from PyQt5 import QtCore, QtWidgets
from numpy import loadtxt
import matplotlib
matplotlib.rcParams['backend'] = "Qt5Agg"
#matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from distributions import SupportedDistributions, CandidateDistributions
from quantiles import Quantiles

class MainWindow(QtWidgets.QMainWindow):
    """Main window of pplotpy; no parent higher than this object"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize
        self.samples = None
        self.main_widget = QtWidgets.QWidget(self)
        self.cDists = CandidateDistributions()
        self.aDists = SupportedDistributions.subclasses.keys()
        self.quantile_choices = Quantiles.subclasses.keys()
        self.qmethod = list(self.quantile_choices)[0]
        self.table_headers = ["Distribution",
                              "Location",
                              "Scale",
                              "Shape",
                              "R^2"]
        
        self.initUI()
        
    def initUI(self):
        """Set up user interface"""

        self.setWindowTitle("pplotpy")
        self.resize(566, 520)
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 541, 461))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        self.dataFileButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.dataFileButton.setObjectName("dataFileButton")
        self.dataFileButton.setText("Data File")
        
        self.horizontalLayout_2.addWidget(self.dataFileButton)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.dataFilePath = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.dataFilePath.setEnabled(False)
        self.dataFilePath.setObjectName("dataFilePath")
        self.verticalLayout_3.addWidget(self.dataFilePath)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.quantileLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.quantileLabel.setObjectName("quantileLabel")
        self.quantileLabel.setText("Quantile Method:")
        self.verticalLayout_2.addWidget(self.quantileLabel, 0, QtCore.Qt.AlignHCenter)
        self.quantileComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.quantileComboBox.setObjectName("quantileComboBox")
        self.quantileComboBox.addItems(self.quantile_choices)
        self.verticalLayout_2.addWidget(self.quantileComboBox, 0, QtCore.Qt.AlignTop)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_4 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout.addWidget(self.line_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        
        # Available Distributions
        self.availDistsLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.availDistsLabel.setObjectName("availDistsLabel")
        self.availDistsLabel.setText("Available Distributions:")
        self.verticalLayout_4.addWidget(self.availDistsLabel)
        self.availDistsListWidget = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.availDistsListWidget.setEnabled(False)
        self.availDistsListWidget.setObjectName("availDistsListWidget")
        self.availDistsListWidget.addItems(self.aDists)
        self.availDistsListWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.availDistsListWidget.setCurrentRow(0)
        self.verticalLayout_4.addWidget(self.availDistsListWidget)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)

        # Location Parameter
        self.locLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.locLabel.setEnabled(False)
        self.locLabel.setObjectName("locLabel")
        self.locLabel.setText("Location:")
        self.horizontalLayout_3.addWidget(self.locLabel)
        self.locTextBox = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.locTextBox.setEnabled(False)
        self.locTextBox.setMaximumSize(QtCore.QSize(50, 16777215))
        self.locTextBox.setText("")
        self.locTextBox.setObjectName("locTextBox")
        self.horizontalLayout_3.addWidget(self.locTextBox)
        
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_3.addWidget(self.line)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        
        # Remove All (distributions)
        self.removeAllButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.removeAllButton.setObjectName("removeAllButton")
        self.removeAllButton.setText("Remove All")
        self.verticalLayout_5.addWidget(self.removeAllButton)

        # Remove (distribution)
        self.removeButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.removeButton.setObjectName("removeButton")
        self.removeButton.setText("Remove")
        self.removeButton.setDisabled(True)
        self.verticalLayout_5.addWidget(self.removeButton)

        # Add (distribution)
        self.addButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.addButton.setObjectName("addButton")
        self.addButton.setText("Add")
        self.addButton.setDisabled(True)
        self.verticalLayout_5.addWidget(self.addButton)
        
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.line_3 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        
        # Candidate Distribution Table
        self.candDistsLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.candDistsLabel.setObjectName("candDistsLabel")
        self.candDistsLabel.setText("Candidate Distributions:")
        self.verticalLayout.addWidget(self.candDistsLabel)
        self.candListsTableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.candListsTableWidget.setObjectName("candListsTableWidget")
        self.candListsTableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.candListsTableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.candListsTableWidget.setColumnCount(5)
        self.candListsTableWidget.setRowCount(0)
        self.candListsTableWidget.setHorizontalHeaderLabels(self.table_headers)
        self.candListsTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.verticalLayout.addWidget(self.candListsTableWidget)
        self.line_5 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout.addWidget(self.line_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)

        # Print SciPy information button
        self.printScipyButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.printScipyButton.setObjectName("printScipyButton")
        self.printScipyButton.setText("Print SciPy")
        self.horizontalLayout_4.addWidget(self.printScipyButton)

        # Print Distribution information button
        self.printDistButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.printDistButton.setObjectName("printDistButton")
        self.printDistButton.setText("Print Distribution")
        self.horizontalLayout_4.addWidget(self.printDistButton)

        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayoutWidget.raise_()
        self.candListsTableWidget.raise_()

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 566, 19))
        self.menubar.setObjectName("menubar")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setTitle("Help")
        self.menuAbout.setObjectName("menuAbout")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.setText("About")
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuAbout.menuAction())

        
        # --- Bind events with actions ---
        self.dataFileButton.clicked.connect(self.upload_samples)    # Data File
        self.quantileComboBox.activated.connect(self.update_query_method) # Quantile Method

        self.availDistsListWidget.itemClicked.connect(self.unlock_location)


        # Add Distributions
        self.addButton.clicked.connect(self.add_dist_by_button)
        self.availDistsListWidget.itemDoubleClicked.connect(self.add_dist_by_dclick)

        # Remove Distributions
        self.removeButton.clicked.connect(self.rm_distribution)
        self.removeAllButton.clicked.connect(self.rm_all_distributions)

        # Plot Probability Plot
        self.candListsTableWidget.itemDoubleClicked.connect(self.create_probability_plot)

        QtCore.QMetaObject.connectSlotsByName(self)

        # Display GUI
        self.show()

    # Wrapper Defintion for updating all distributions
    def update_existing(function):
        def wrapper(self, *args):
            function(self, *args)
            if self.cDists.get_count() > 0 and self.samples != None:
                self.candListsTableWidget.clearContents()
                self.cDists.calc_all(self.samples, self.qmethod)
                self.update_results()
        return wrapper      

    @update_existing
    def upload_samples(self, *args):
        fpath = QtWidgets.QFileDialog.getOpenFileName(None, 
                                                      "Select data file")[0]
        try:
            raw_data = loadtxt(fpath)
            self.samples = raw_data.flatten()
            self.statusbar.clearMessage()
            self.availDistsListWidget.setEnabled(True)
            self.addButton.setEnabled(True)
            self.dataFilePath.setText(fpath)
        except:
            self.samples = None
            self.statusbar.showMessage("Error importing data")
            self.availDistsListWidget.setDisabled(True)
            self.addButton.setDisabled(True)
            self.dataFilePath.setText("")

    def unlock_location(self, item):
        dist_name = item.text()
        if SupportedDistributions.has_optional_loc_param(dist_name) == True:
            self.locTextBox.setEnabled(True)
            self.locLabel.setEnabled(True)
            self.locTextBox.setText("0.0")
        else:
            self.locTextBox.setDisabled(True)
            self.locLabel.setDisabled(True)
            self.locTextBox.setText("")
    
    @update_existing
    def update_query_method(self, index):
        self.qmethod =self.quantileComboBox.currentText()
        
    def update_results(self):
        self.cDists.calc_all(self.samples, self.qmethod)
        for ii, dist in enumerate(self.cDists.dists):
            self.update_row(ii, dist)
        
    def update_row(self, row_index, dist_obj):
        self.candListsTableWidget.setItem(row_index,
                                          0,
                                          QtWidgets.QTableWidgetItem(dist_obj.get_label()))
        self.candListsTableWidget.setItem(row_index,
                                          1,
                                          QtWidgets.QTableWidgetItem(dist_obj.get_loc_str()))
        self.candListsTableWidget.setItem(row_index,
                                          2,
                                          QtWidgets.QTableWidgetItem(dist_obj.get_scale_str()))
        self.candListsTableWidget.setItem(row_index,
                                          3,
                                          QtWidgets.QTableWidgetItem(dist_obj.get_shape_str()))
        self.candListsTableWidget.setItem(row_index,
                                          4,
                                          QtWidgets.QTableWidgetItem(dist_obj.get_coeff_of_determ_str()))


    def add_row(self):
        row_index = self.candListsTableWidget.rowCount()
        self.candListsTableWidget.insertRow(row_index)
        return row_index

    def add_distribution(self, dist_name):
        dist_obj = SupportedDistributions.create_subclass_instance(dist_name)
        if dist_obj.loc_optional == True:
            loc_val = float(self.locTextBox.text())
            dist_obj.set_location(loc_val)
        self.cDists.add_distribution(dist_obj, self.samples, self.qmethod)
        
        row_index = self.add_row()
        self.update_row(row_index, self.cDists.get_obj(-1))
        self.removeButton.setEnabled(True)
        
    def add_dist_by_dclick(self, item):
        dist_name = item.text()
        self.add_distribution(dist_name)        

    def create_probability_plot(self, item):
        row = item.row()
        dist_obj = self.cDists.get_obj(row)
        dist_name = dist_obj.get_label()
        PlotWindow(self,dist_obj, dist_name)
        
    def add_dist_by_button(self):
        dist_name = self.availDistsListWidget.currentItem().text()
        self.add_distribution(dist_name) 
        
    def rm_distribution(self):
        try:
            row = self.candListsTableWidget.currentRow()
            self.cDists.remove_dist(row)
            self.candListsTableWidget.removeRow(row)
            if self.candListsTableWidget.rowCount() == 0:
                self.removeButton.setDisabled(True)
        except:
            self.statusbar.showMessage("Select a cand. distri. to remove")

    def rm_all_distributions(self):
        self.candListsTableWidget.clearContents()
        self.candListsTableWidget.setRowCount(0)
        self.cDists.remove_all()

class PlotWindow(QtWidgets.QMainWindow):
    
    def __init__(self, parent, dist_obj, dist_name):
        super().__init__(parent=parent)
        self.canvas = PlotCanvas(self)
        self.canvas.plot(dist_obj)
        self.main_widget = QtWidgets.QWidget(self)
        self.setWindowTitle(dist_name)
        self.initUI()

    def initUI(self):
        l = QtWidgets.QVBoxLayout(self.main_widget)
        l.addWidget(self.canvas)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.show()
    

class PlotCanvas(FigureCanvas):
 
    def __init__(self,
                 parent=None,
                 width=5,
                 height=4,
                 dpi=100,):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
  
    def plot(self, dist_obj):
        #self.axes.plot([1,3,4],[5,3,2])
        dist_obj.create_pplot(self.axes)
        self.draw()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())

