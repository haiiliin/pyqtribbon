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
        self._mainLayout = QtWidgets.QVBoxLayout(self.centralWidget())
        self._mainLayout.setContentsMargins(5, 5, 5, 5)
        self._ribbon = RibbonBar()
        self._mainLayout.addWidget(self._ribbon)

    def ribbonBar(self) -> RibbonBar:
        """Return the ribbon bar."""
        return self._ribbon

    def layout(self) -> 'QtWidgets.QVBoxLayout':
        """Return the main layout."""
        return self._mainLayout
