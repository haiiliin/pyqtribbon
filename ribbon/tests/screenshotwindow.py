from qtpy import QtWidgets, QtCore, QtGui


class RibbonScreenShotWindow(QtWidgets.QMainWindow):
    """This class is just for taking a screenshot of the window, the window will be closed 0.1s after it is shown.
    """
    _fileName = 'shot.jpg'

    def __init__(self, fileName: str = 'shot.jpg', *args, **kwargs):
        """Initialize the class.

        :param fileName: The file name for the screenshot.
        """
        super().__init__(*args, **kwargs)
        QtCore.QTimer().singleShot(1000, self.close)
        self.setScreenShotFileName(fileName)

    def setScreenShotFileName(self, fileName: str):
        """Set the file name for the screenshot.

        :param fileName: The file name for the screenshot.
        """
        self._fileName = fileName

    def closeEvent(self, *args, **kwargs):
        """Close event of the window.
        """
        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.winId())
        screenshot.save(self._fileName)
        super().closeEvent(*args, **kwargs)
