"""module for importing Qt modules and creating a QApplication instance from pyqtgraph."""
import os
import sys

from qtpy import QtCore, QtWidgets
from qtpy import QT_VERSION as QtVersion

QAPP = None


def mkQApp(name=None):
    global QAPP

    def onPaletteChange(palette):
        color = palette.base().color()
        app = QtWidgets.QApplication.instance()
        darkMode = color.lightnessF() < 0.5
        app.setProperty('darkMode', darkMode)

    QAPP = QtWidgets.QApplication.instance()
    if QAPP is None:
        # hidpi handling
        qtVersionCompare = tuple(map(int, QtVersion.split(".")))
        if qtVersionCompare > (6, 0):
            # Qt6 seems to support hidpi without needing to do anything so continue
            pass
        elif qtVersionCompare > (5, 14):
            os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
            QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(
                QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        else:  # qt 5.12 and 5.13
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

        QAPP = QtWidgets.QApplication(sys.argv)
        QAPP.paletteChanged.connect(onPaletteChange)  # type: ignore
        QAPP.paletteChanged.emit(QAPP.palette())  # type: ignore

    if name is not None:
        QAPP.setApplicationName(name)
    return QAPP


def exec_():
    app = mkQApp()
    return app.exec() if hasattr(app, 'exec') else app.exec_()
