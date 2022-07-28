import sys
import typing

from qtpy import QtWidgets, QtGui

qApp = None  # type: typing.Optional[QtWidgets.QApplication]


def mkQApp(name=None):
    global qApp
    qApp = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv or ["pyqtribbon"])
    qApp.setFont(QtGui.QFont("Times New Roman", 8))

    if name is not None:
        qApp.setApplicationName(name)
    return qApp


def exec_():
    app = mkQApp()
    return app.exec() if hasattr(app, 'exec') else app.exec_()
