import enum
import typing

from PyQt5 import QtWidgets, QtCore, QtGui

from .panel import Panel
from .typehints import RibbonType


class CategoryStyle(enum.IntEnum):
    """The buttonStyle of a category."""
    Normal = 0
    Context = 1


#: A list of context category colors
contextColors = [
    QtGui.QColor(201, 89, 156),  # 玫红
    QtGui.QColor(242, 203, 29),  # 黄
    QtGui.QColor(255, 157, 0),  # 橙
    QtGui.QColor(14, 81, 167),  # 蓝
    QtGui.QColor(228, 0, 69),  # 红
    QtGui.QColor(67, 148, 0),  # 绿
]


class DisplayOptionsButton(QtWidgets.QToolButton):
    pass


class Category(QtWidgets.QFrame):
    #: Title of the category
    _title: str
    #: The ribbon parent of this category
    _ribbon: typing.Optional[RibbonType]
    #: The buttonStyle of the category.
    _style: CategoryStyle
    #: Panels
    _panels: typing.Dict[str, Panel]
    #: color of the context category
    _color: typing.Optional[QtGui.QColor]

    #: The signal that is emitted when the display options button is clicked.
    displayOptionsButtonClicked = QtCore.pyqtSignal(bool)

    def __init__(self, title: str, style: CategoryStyle = CategoryStyle.Normal, color: QtGui.QColor = None,
                 parent=None):
        super().__init__(parent)
        self.setStyleSheet("QWidget { background-color: white; }")
        self._title = title
        self._style = style
        self._panels = {}
        self._ribbon = parent
        self._color = color

        self._scrollArea = QtWidgets.QScrollArea()
        self._scrollArea.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self._scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self._scrollLayout = QtWidgets.QHBoxLayout(self._scrollArea)
        self._scrollLayout.setContentsMargins(0, 0, 0, 0)
        self._scrollLayout.setSpacing(5)
        self._scrollLayout.addSpacerItem(
            QtWidgets.QSpacerItem(
                10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
            )
        )

        self._displayOptionsLayout = QtWidgets.QVBoxLayout()
        self._displayOptionsLayout.setContentsMargins(0, 0, 0, 0)
        self._displayOptionsLayout.setSpacing(5)
        self._displayOptionsLayout.addSpacerItem(
            QtWidgets.QSpacerItem(
                10, 10, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
            )
        )
        self._displayOptionsButton = DisplayOptionsButton()
        self._displayOptionsButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self._displayOptionsButton.setIcon(QtGui.QIcon("icons/expand-arrow.png"))
        self._displayOptionsButton.setIconSize(QtCore.QSize(16, 16))
        self._displayOptionsButton.setText("Ribbon Display Options")
        self._displayOptionsButton.setToolTip("Ribbon Display Options")
        self._displayOptionsButton.setEnabled(True)
        self._displayOptionsButton.setAutoRaise(True)
        self._displayOptionsButton.clicked.connect(self.displayOptionsButtonClicked)
        self._displayOptionsLayout.addWidget(self._displayOptionsButton, 0, QtCore.Qt.AlignBottom)
        self._displayOptionsMenu = QtWidgets.QMenu()

        self._mainLayout = QtWidgets.QHBoxLayout(self)
        self._mainLayout.setSpacing(5)
        self._mainLayout.setContentsMargins(5, 5, 5, 5)
        self._mainLayout.addWidget(self._scrollArea)
        self._mainLayout.addSpacerItem(
            QtWidgets.QSpacerItem(
                10, 10, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
            )
        )
        self._mainLayout.addLayout(self._displayOptionsLayout)

    def title(self) -> str:
        """Return the title of the category."""
        return self._title

    def setCategoryStyle(self, style: CategoryStyle):
        """Set the buttonStyle of the category.

        :param style: The buttonStyle.
        """
        self._style = style
        self.repaint()

    def categoryStyle(self):
        """Return the buttonStyle of the category.

        :return: The buttonStyle.
        """
        return self._style

    def addPanel(self, title: str) -> Panel:
        """Add a new panel to the category.

        :param title: The title of the panel.
        :return: The newly created panel.
        """
        panel = Panel(title, maxRows=6, parent=self)
        panel.setFixedHeight(self.height() -
                             self._mainLayout.spacing() -
                             self._mainLayout.contentsMargins().top() -
                             self._mainLayout.contentsMargins().bottom())
        self._panels[title] = panel
        self._scrollLayout.insertWidget(self._scrollLayout.count() - 1, panel)

        line = QtWidgets.QFrame()
        line.setFrameStyle(QtWidgets.QFrame.VLine | QtWidgets.QFrame.Sunken)
        line.setEnabled(False)
        self._scrollLayout.insertWidget(self._scrollLayout.count() - 1, line)
        self._scrollLayout.addStretch(1)
        return panel

    def removePanel(self, title: str):
        """Remove a panel from the category.

        :param title: The title of the panel.
        """
        self._scrollLayout.removeWidget(self._panels[title])
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

    def addDisplayOption(self, title: str, icon: QtGui.QIcon = None, callback: callable = None):
        """Add a display option to the category.

        :param title: The title of the display option.
        :param icon: The icon of the display option.
        :param callback: The callback of the display option.
        """
        action = QtWidgets.QAction(title, self)
        if icon is not None:
            action.setIcon(icon)
        if callback is not None:
            action.triggered.connect(callback)
        self._displayOptionsMenu.addAction(action)

    def addDisplayOptionAction(self, action: QtWidgets.QAction):
        """Add a display option to the category.

        :param action: The action of the display option.
        """
        self._displayOptionsMenu.addAction(action)
        self._displayOptionsButton.setMenu(self._displayOptionsMenu if self._displayOptionsMenu.actions() else None)


class NormalCategory(Category):

    def __init__(self, title: str, parent: QtWidgets.QWidget):
        super().__init__(title, CategoryStyle.Normal, parent=parent)


class ContextCategory(Category):

    def __init__(self, title: str, color: QtGui.QColor, parent: QtWidgets.QWidget):
        super().__init__(title, CategoryStyle.Context, color=color, parent=parent)

    def color(self) -> QtGui.QColor:
        """Return the color of the context category.

        :return: The color of the context category.
        """
        return self._color

    def showContextCategory(self):
        """Show the given category, if it is not a context category, nothing happens."""
        self._ribbon.showContextCategory(self)

    def hideContextCategory(self):
        """Hide the given category, if it is not a context category, nothing happens."""
        self._ribbon.hideContextCategory(self)

    def categoryState(self) -> bool:
        """Return whether the category is shown.

        :return: Whether the category is shown.
        """
        return self in self._ribbon.categories()

    def setCategoryState(self, state: bool):
        """Set the state of the category.

        :param state: The state.
        """
        if state:
            self.showContextCategory()
        else:
            self.hideContextCategory()
