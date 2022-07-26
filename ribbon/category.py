import enum
import typing

from qtpy import QtWidgets, QtGui

from .categorylayoutwidget import RibbonCategoryLayoutWidget
from .panel import RibbonPanel
from .separator import RibbonSeparator
from .typehints import RibbonType


class RibbonCategoryStyle(enum.IntEnum):
    """The button style of a category."""
    Normal = 0
    Context = 1


Normal = RibbonCategoryStyle.Normal
Context = RibbonCategoryStyle.Context


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
    _style: RibbonCategoryStyle
    #: Panels
    _panels: typing.Dict[str, RibbonPanel]
    #: color of the context category
    _color: typing.Optional[QtGui.QColor]

    @typing.overload
    def __init__(self, title: str = '', style: RibbonCategoryStyle = RibbonCategoryStyle.Normal,
                 color: QtGui.QColor = None, parent=None):
        pass

    @typing.overload
    def __init__(self, parent=None):
        pass

    def __init__(self, *args, **kwargs):
        """Create a new category.

        :param title: The title of the category.
        :param style: The button style of the category.
        :param color: The color of the context category.
        :param parent: The parent widget.
        """
        if (args and not isinstance(args[0], QtWidgets.QWidget)) or ('title' in kwargs or
                                                                     'style' in kwargs or
                                                                     'color' in kwargs):
            title = args[0] if len(args) > 0 else kwargs.get('title', '')
            style = args[1] if len(args) > 1 else kwargs.get('style', RibbonCategoryStyle.Normal)
            color = args[2] if len(args) > 2 else kwargs.get('color', None)
            parent = args[3] if len(args) > 3 else kwargs.get('parent', None)
        else:
            title = ''
            style = RibbonCategoryStyle.Normal
            color = None
            parent = args[0] if len(args) > 0 else kwargs.get('parent', None)
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

    def setCategoryStyle(self, style: RibbonCategoryStyle):
        """Set the button style of the category.

        :param style: The button style.
        """
        self._style = style
        self.repaint()

    def categoryStyle(self) -> RibbonCategoryStyle:
        """Return the button style of the category.

        :return: The button style.
        """
        return self._style

    def addPanel(self, title: str, showPanelOptionButton=True) -> RibbonPanel:
        """Add a new panel to the category.

        :param title: The title of the panel.
        :param showPanelOptionButton: Whether to show the panel option button.
        :return: The newly created panel.
        """
        panel = RibbonPanel(title, maxRows=6, showPanelOptionButton=showPanelOptionButton, parent=self)
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

    def takePanel(self, title: str) -> RibbonPanel:
        """Remove and return a panel from the category.

        :param title: The title of the panel.
        :return: The removed panel.
        """
        panel = self._panels[title]
        self.removePanel(title)
        return panel

    def panel(self, title: str) -> RibbonPanel:
        """Return a panel from the category.

        :param title: The title of the panel.
        :return: The panel.
        """
        return self._panels[title]
    
    def panels(self) -> typing.Dict[str, RibbonPanel]:
        """Return all panels in the category.

        :return: The panels.
        """
        return self._panels


class RibbonNormalCategory(RibbonCategory):
    """A normal category."""

    def __init__(self, title: str, parent: QtWidgets.QWidget):
        """Create a new normal category.

        :param title: The title of the category.
        :param parent: The parent widget.
        """
        super().__init__(title, RibbonCategoryStyle.Normal, parent=parent)

    def setCategoryStyle(self, style: RibbonCategoryStyle):
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
        super().__init__(title, RibbonCategoryStyle.Context, color=color, parent=parent)

    def setCategoryStyle(self, style: RibbonCategoryStyle):
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
        return self._ribbon.categoryVisible(self)

    def setCategoryVisible(self, visible: bool):
        """Set the state of the category.

        :param visible: The state.
        """
        if visible:
            self.showContextCategory()
        else:
            self.hideContextCategory()


class RibbonContextCategories(typing.Dict[str, RibbonContextCategory]):
    """A list of context categories."""
    _ribbon: RibbonType

    def __init__(
        self,
        name: str,
        color: QtGui.QColor,
        categories: typing.Dict[str, RibbonContextCategory],
        ribbon,
    ):
        self._name = name
        self._color = color
        self._ribbon = ribbon
        super().__init__(categories)

    def name(self) -> str:
        """Return the name of the context categories."""
        return self._name

    def setName(self, name: str):
        """Set the name of the context categories."""
        self._name = name

    def color(self) -> QtGui.QColor:
        """Return the color of the context categories."""
        return self._color

    def setColor(self, color: QtGui.QColor):
        """Set the color of the context categories."""
        self._color = color

    def showContextCategories(self):
        """Show the categories"""
        self._ribbon.showContextCategory(self)

    def hideContextCategories(self):
        """Hide the categories"""
        self._ribbon.hideContextCategory(self)

    def categoriesVisible(self) -> bool:
        """Return whether the categories are shown."""
        for category in self.values():
            if category.categoryVisible():
                return True
        return False

    def setCategoriesVisible(self, visible: bool):
        """Set the state of the categories."""
        if visible:
            self.showContextCategories()
        else:
            self.hideContextCategories()
