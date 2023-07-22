from pytestqt.qtbot import QtBot
from qtpy import QtCore

from pyqtribbon.titlewidget import RibbonTitleWidget


def test_titlewidget(qtbot: QtBot):
    # Add the widget to the test
    titlewidget = RibbonTitleWidget()
    titlewidget.setMouseTracking(True)
    titlewidget.show()
    qtbot.addWidget(titlewidget)

    # Test the mouse double click events
    titlewidget.showNormal()
    qtbot.mouseDClick(titlewidget, QtCore.Qt.LeftButton)
    assert titlewidget.topLevelWidget().isMaximized() is True
    qtbot.mouseDClick(titlewidget, QtCore.Qt.LeftButton)
    assert titlewidget.topLevelWidget().isMaximized() is False

    # Test the mouse move events
    pos = titlewidget.pos()
    qtbot.mousePress(titlewidget, QtCore.Qt.LeftButton, pos=QtCore.QPoint(0, 0))
    qtbot.mouseMove(titlewidget, pos=QtCore.QPoint(10, 10))
    # TODO: assert the position of the widget
