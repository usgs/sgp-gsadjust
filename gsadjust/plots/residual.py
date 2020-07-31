"""
gsa_plots.py
===============

GSadjust plotting module.
--------------------------------------------------------------------------------

This software is preliminary, provisional, and is subject to revision. It is
being provided to meet the need for timely best science. The software has not
received final approval by the U.S. Geological Survey (USGS). No warranty,
expressed or implied, is made by the USGS or the U.S. Government as to the
functionality of the software and related material nor shall the fact of release
constitute any such warranty. The software is provided on the condition that
neither the USGS nor the U.S. Government shall be held liable for any damages
resulting from the authorized or unauthorized use of the software.
"""
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class PlotDgResidualHistogram(QtWidgets.QDialog):
    """
    Matplotlib histogram of delta-g residuals
    """

    # the histogram of the data
    def __init__(self, survey, parent=None):
        super(PlotDgResidualHistogram, self).__init__(parent)
        self.survey = survey

        self.setWindowTitle('GSadjust results')
        self.figure = matplotlib.figure.Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        rlist = self.get_data()
        if rlist:
            self.plot(rlist)

    def get_data(self):
        survey = self.survey
        try:
            nrows = survey.delta_model.rowCount()
            rlist = []
            for i in range(nrows):
                idx = survey.delta_model.index(i, 8)
                results = survey.delta_model.data(idx, role=Qt.DisplayRole)
                d = float(results)
                if d > -998:
                    rlist.append(float(results))
            return rlist
        except Exception as e:
            return False

    def plot(self, rlist):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.hist(rlist, 20, facecolor='green', alpha=0.75)
        ax.set_title('Adjusted g minus measured g (microGal)')
        ax.set_xlabel('Residual (microGal)')
        ax.set_ylabel('Relative frequency')
        ax.grid()
        self.canvas.draw()
