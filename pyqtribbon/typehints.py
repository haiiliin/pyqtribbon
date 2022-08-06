import typing

from qtpy import QtWidgets


class PyQtSignalType:
    """This is a protocol for the pyqt signal type."""

    def connect(self, slot):
        ...

    def disconnect(self, slot):
        ...

    def emit(self, *args):
        ...


class PyQtActionType:
    """This is a protocol for the pyqt action type."""

    triggered: PyQtSignalType


class RibbonType:
    """
    This is a protocol for the ribbon type for type hints in categories for getting the tabRect.
    """
    def tabBar(self) -> QtWidgets.QTabBar:
        ...

    def showContextCategory(self, category):
        ...

    def hideContextCategory(self, category):
        ...

    def setCategoryState(self, category, state):
        ...

    def categoryVisible(self, category):
        ...

    def categories(self) -> typing.Dict:
        ...

    def repaint(self):
        ...
