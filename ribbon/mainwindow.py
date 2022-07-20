from PyQt5 import QtWidgets

from .ribbon import Ribbon


class RibbonMainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCentralWidget(QtWidgets.QWidget(self))
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralWidget())
        self.mainLayout.setContentsMargins(5, 0, 5, 5)
        self.ribbon = Ribbon()
        self.mainLayout.addWidget(self.ribbon)
