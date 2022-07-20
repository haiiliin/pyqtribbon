import typing

from PyQt5 import QtCore, QtWidgets


class PyQtSignalType(typing.Protocol):
    """This is a protocol for the pyqt signal type."""

    def connect(self, slot):
        ...

    def disconnect(self, slot):
        ...

    def emit(self, *args):
        ...


class PyQtActionType(typing.Protocol):
    """This is a protocol for the pyqt action type."""

    triggered: PyQtSignalType


class RibbonType(typing.Protocol):
    """
    This is a protocol for the ribbon type for type hints in categories for getting the tabRect.
    """
    def tabBar(self) -> QtWidgets.QTabBar:
        ...

    def tabRect(self, category) -> QtCore.QRect:
        ...

    def showContextCategory(self, category):
        ...

    def hideContextCategory(self, category):
        ...

    def setCategoryState(self, category, state):
        ...

    def categories(self) -> typing.List:
        ...

    def repaint(self):
        ...
