import enum
import typing

from PyQt5 import QtWidgets, QtCore, QtGui

from .categorylayoutwidget import RibbonCategoryLayoutWidget
from .panel import RibbonPanel
from .separator import RibbonSeparator
from .typehints import RibbonType


class CategoryStyle(enum.IntEnum):
    """The button style of a category."""
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


class RibbonCategory(QtWidgets.QFrame):
    """The RibbonCategory is the logical grouping that represents the contents of a ribbon tab."""
    #: Title of the category
    _title: str
    #: The ribbon parent of this category
    _ribbon: typing.Optional[RibbonType]
    #: The button style of the category.
    _style: CategoryStyle
    #: Panels
    _panels: typing.Dict[str, RibbonPanel]
    #: color of the context category
    _color: typing.Optional[QtGui.QColor]

    #: The signal that is emitted when the display options button is clicked.
    displayOptionsButtonClicked = QtCore.pyqtSignal(bool)

    def __init__(self, title: str, style: CategoryStyle = CategoryStyle.Normal, color: QtGui.QColor = None,
                 parent=None):
        """Create a new category.

        :param title: The title of the category.
        :param style: The button style of the category.
        :param color: The color of the context category.
        :param parent: The parent widget.
        """
        super().__init__(parent)
        self._title = title
        self._style = style
        self._panels = {}
        self._ribbon = parent
        self._color = color

        self._panelLayoutWidget = RibbonCategoryLayoutWidget()
        self._mainLayout = QtWidgets.QHBoxLayout(self)
        self._mainLayout.setSpacing(5)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.addWidget(self._panelLayoutWidget, 0)

    def title(self) -> str:
        """Return the title of the category."""
        return self._title

    def setCategoryStyle(self, style: CategoryStyle):
        """Set the button style of the category.

        :param style: The button style.
        """
        self._style = style
        self.repaint()

    def categoryStyle(self):
        """Return the button style of the category.

        :return: The button tyle.
        """
        return self._style

    def addPanel(self, title: str) -> RibbonPanel:
        """Add a new panel to the category.

        :param title: The title of the panel.
        :return: The newly created panel.
        """
        panel = RibbonPanel(title, maxRows=6, parent=self)
        panel.setFixedHeight(self.height() -
                             self._mainLayout.spacing() -
                             self._mainLayout.contentsMargins().top() -
                             self._mainLayout.contentsMargins().bottom())
        self._panels[title] = panel
        self._panelLayoutWidget.addWidget(panel)
        self._panelLayoutWidget.addWidget(RibbonSeparator(width=10))
        return panel

    def removePanel(self, title: str):
        """Remove a panel from the category.

        :param title: The title of the panel.
        """
        # self._panelLayout.removeWidget(self._panels[title])
        self._panelLayoutWidget.removeWidget(self._panels[title])
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


class RibbonNormalCategory(RibbonCategory):
    """A normal category."""

    def __init__(self, title: str, parent: QtWidgets.QWidget):
        """Create a new normal category.

        :param title: The title of the category.
        :param parent: The parent widget.
        """
        super().__init__(title, CategoryStyle.Normal, parent=parent)

    def setCategoryStyle(self, style: CategoryStyle):
        """Set the button style of the category.

        :param style: The button style.
        """
        raise ValueError("You can not set the category style of a normal category.")


class RibbonContextCategory(RibbonCategory):
    """A context category."""

    def __init__(self, title: str, color: QtGui.QColor, parent: QtWidgets.QWidget):
        """Create a new context category.

        :param title: The title of the category.
        :param color: The color of the context category.
        :param parent: The parent widget.
        """
        super().__init__(title, CategoryStyle.Context, color=color, parent=parent)

    def setCategoryStyle(self, style: CategoryStyle):
        """Set the button style of the category.

        :param style: The button style.
        """
        raise ValueError("You can not set the category style of a context category.")

    def color(self) -> QtGui.QColor:
        """Return the color of the context category.

        :return: The color of the context category.
        """
        return self._color

    def setColor(self, color: QtGui.QColor):
        """Set the color of the context category.

        :param color: The color of the context category.
        """
        self._color = color
        self._ribbon.repaint()

    def showContextCategory(self):
        """Show the given category, if it is not a context category, nothing happens."""
        self._ribbon.showContextCategory(self)

    def hideContextCategory(self):
        """Hide the given category, if it is not a context category, nothing happens."""
        self._ribbon.hideContextCategory(self)

    def categoryVisible(self) -> bool:
        """Return whether the category is shown.

        :return: Whether the category is shown.
        """
        return self in self._ribbon.categories()

    def setCategoryVisible(self, state: bool):
        """Set the state of the category.

        :param state: The state.
        """
        if state:
            self.showContextCategory()
        else:
            self.hideContextCategory()
