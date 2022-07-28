import sys

from qtpy import QtWidgets, QtGui


def mkQApp(name=None):
    qApp = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    qApp.setFont(QtGui.QFont("Times New Roman", 8))

    if name is not None:
        qApp.setApplicationName(name)
    return qApp


def exec_():
    app = mkQApp()
    return app.exec() if hasattr(app, 'exec') else app.exec_()
