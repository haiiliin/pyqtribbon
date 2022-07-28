import sys

from qtpy import QtWidgets

from ribbon import RibbonBar
from ribbon.tests import RibbonScreenShotWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = RibbonScreenShotWindow('ribbonbar.png')

    # Ribbon bar
    ribbonbar = RibbonBar()
    window.setMenuBar(ribbonbar)

    # Show the window
    window.resize(1000, 250)
    window.show()

    sys.exit(app.exec_())
