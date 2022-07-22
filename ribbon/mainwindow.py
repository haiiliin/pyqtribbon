from PyQt5 import QtWidgets

from .ribbonbar import RibbonBar


class RibbonMainWindow(QtWidgets.QMainWindow):
    """Main window with ribbon bar."""

    def __init__(self, parent=None):
        """Create a new main window with ribbon bar.

        :param parent: The parent widget.
        """
        super().__init__(parent)
        self.setCentralWidget(QtWidgets.QWidget(self))
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralWidget())
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.ribbon = RibbonBar()
        self.mainLayout.addWidget(self.ribbon)
