import enum
import typing

from PyQt5 import QtWidgets, QtCore
from .panel import Panel


class CategoryStyle(enum.IntEnum):
    """The buttonStyle of a category."""

    Normal = 0
    Contextual = 1


class Category(QtWidgets.QWidget):
    #: The buttonStyle of the category.
    _style: CategoryStyle
    #: Panels
    _panels: typing.Dict[str, Panel]

    def __init__(self, style: CategoryStyle = CategoryStyle.Normal, parent=None):
        super().__init__(parent)
        self._style = style
        self._panels = {}

        self._scrollArea = QtWidgets.QScrollArea()
        self._scrollArea.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self._scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self._mLayout = QtWidgets.QVBoxLayout(self)
        self._mLayout.setSpacing(0)
        self._mLayout.setContentsMargins(0, 0, 0, 0)
        self._mLayout.addWidget(self._scrollArea)

        self._mainLayout = QtWidgets.QHBoxLayout()
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(5)
        self._mainLayout.addSpacerItem(
            QtWidgets.QSpacerItem(
                10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
            )
        )
        self._scrollArea.setLayout(self._mainLayout)

    def addPanel(self, title: str) -> Panel:
        """Add a new panel to the category.

        :param title: The title of the panel.
        :return: The newly created panel.
        """
        panel = Panel(title, maxRows=3, parent=self)
        self._panels[title] = panel
        self._mainLayout.insertWidget(self._mainLayout.count() - 1, panel)

        line = QtWidgets.QFrame()
        line.setFrameStyle(QtWidgets.QFrame.VLine | QtWidgets.QFrame.Sunken)
        line.setEnabled(False)
        self._mainLayout.insertWidget(self._mainLayout.count() - 1, line)
        self._mainLayout.addStretch(1)
        return panel

    def removePanel(self, title: str):
        """Remove a panel from the category.

        :param title: The title of the panel.
        """
        self._mainLayout.removeWidget(self._panels[title])
        self._panels.pop(title)

    def takePanel(self, title: str):
        """Remove and return a panel from the category.

        :param title: The title of the panel.
        :return: The removed panel.
        """
        panel = self._panels[title]
        self.removePanel(title)
        return panel

    def panel(self, title: str):
        """Return a panel from the category.

        :param title: The title of the panel.
        :return: The panel.
        """
        return self._panels[title]
