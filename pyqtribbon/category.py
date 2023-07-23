import typing

from qtpy import QtCore, QtGui, QtWidgets

from .constants import RibbonCategoryStyle
from .panel import RibbonPanel
from .separator import RibbonSeparator
from .utils import DataFile

if typing.TYPE_CHECKING:
    from .ribbonbar import RibbonBar  # noqa: F401


class RibbonCategoryLayoutButton(QtWidgets.QToolButton):
    """Previous/Next buttons in the category when the
    size is not enough for the widgets.
    """

    pass


class RibbonCategoryScrollArea(QtWidgets.QScrollArea):
    """Scroll area for the gallery"""

    pass


class RibbonCategoryScrollAreaContents(QtWidgets.QFrame):
    """Scroll area contents for the gallery"""

    pass


class RibbonCategoryLayoutWidget(QtWidgets.QFrame):
    """The category layout widget's category scroll area to arrange the widgets in the category."""

    displayOptionsButtonClicked = QtCore.Signal()

    def __init__(self, parent=None):
        """Create a new category layout widget.

        :param parent: The parent widget.
        """
        super().__init__(parent)

        # Contents of the category scroll area
        self._categoryScrollAreaContents = RibbonCategoryScrollAreaContents()  # type: ignore
        self._categoryScrollAreaContents.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)  # type: ignore
        self._categoryLayout = QtWidgets.QHBoxLayout(self._categoryScrollAreaContents)
        self._categoryLayout.setContentsMargins(0, 0, 0, 0)
        self._categoryLayout.setSpacing(5)
        self._categoryLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)

        # Category scroll area
        self._categoryScrollArea = RibbonCategoryScrollArea()  # type: ignore
        self._categoryScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._categoryScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._categoryScrollArea.setWidget(self._categoryScrollAreaContents)

        # Previous/Next buttons
        self._previousButton = RibbonCategoryLayoutButton(self)
        self._previousButton.setIcon(QtGui.QIcon(DataFile("icons/backward.png")))
        self._previousButton.setIconSize(QtCore.QSize(12, 12))
        self._previousButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self._previousButton.setAutoRaise(True)
        self._previousButton.clicked.connect(self.scrollPrevious)  # type: ignore
        self._nextButton = RibbonCategoryLayoutButton(self)
        self._nextButton.setIcon(QtGui.QIcon(DataFile("icons/forward.png")))
        self._nextButton.setIconSize(QtCore.QSize(12, 12))
        self._nextButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self._nextButton.setAutoRaise(True)
        self._nextButton.clicked.connect(self.scrollNext)  # type: ignore

        # Add the widgets to the main layout
        self._mainLayout = QtWidgets.QHBoxLayout(self)
        self._mainLayout.setContentsMargins(5, 0, 5, 0)
        self._mainLayout.setSpacing(5)
        self._mainLayout.addWidget(self._previousButton, 0, QtCore.Qt.AlignVCenter)
        self._mainLayout.addWidget(self._categoryScrollArea, 1)
        self._mainLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding,
                                                             QtWidgets.QSizePolicy.Minimum))  # fmt: skip
        self._mainLayout.addWidget(self._nextButton, 0, QtCore.Qt.AlignVCenter)

        # Auto set the visibility of the scroll buttons
        self.autoSetScrollButtonsVisible()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Override the paint event to draw the background."""
        super().paintEvent(a0)
        self.autoSetScrollButtonsVisible()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """Override the resize event to resize the scroll area."""
        super().resizeEvent(a0)
        self.autoSetScrollButtonsVisible()

    def autoSetScrollButtonsVisible(self):
        """Set the visibility of the scroll buttons."""
        horizontalScrollBar = self._categoryScrollArea.horizontalScrollBar()
        self._previousButton.setVisible(horizontalScrollBar.value() > horizontalScrollBar.minimum())
        self._nextButton.setVisible(horizontalScrollBar.value() < horizontalScrollBar.maximum())
        self._previousButton.setIconSize(QtCore.QSize(12, self.size().height() - 15))
        self._nextButton.setIconSize(QtCore.QSize(12, self.size().height() - 15))

    def scrollPrevious(self):
        """Scroll the category to the previous widget."""
        horizontalScrollBar = self._categoryScrollArea.horizontalScrollBar()
        horizontalScrollBar.setValue(horizontalScrollBar.value() - 50)
        self.autoSetScrollButtonsVisible()

    def scrollNext(self):
        """Scroll the category to the next widget."""
        self._categoryScrollArea.horizontalScrollBar().setValue(
            self._categoryScrollArea.horizontalScrollBar().value() + 50
        )
        self.autoSetScrollButtonsVisible()

    def addWidget(self, widget: QtWidgets.QWidget):
        """Add a widget to the category layout.

        :param widget: The widget to add.
        """
        self._categoryLayout.addWidget(widget)

    def removeWidget(self, widget: QtWidgets.QWidget):
        """Remove a widget from the category layout.

        :param widget: The widget to remove.
        """
        self._categoryLayout.removeWidget(widget)

    def takeWidget(self, widget: QtWidgets.QWidget) -> QtWidgets.QWidget:
        """Remove and return a widget from the category layout.

        :param widget: The widget to remove.
        :return: The widget that was removed.
        """
        self._categoryLayout.removeWidget(widget)
        return widget


class RibbonCategory(RibbonCategoryLayoutWidget):
    """The RibbonCategory is the logical grouping that represents the contents of a ribbon tab."""

    #: Title of the category
    _title: str
    #: The button style of the category.
    _style: RibbonCategoryStyle
    #: Panels
    _panels: typing.Dict[str, RibbonPanel]
    #: color of the context category
    _color: typing.Optional[QtGui.QColor]
    #: Maximum rows
    _maxRows: int = 6

    @typing.overload
    def __init__(
        self,
        title: str = "",
        style: RibbonCategoryStyle = RibbonCategoryStyle.Normal,
        color: QtGui.QColor = None,
        parent=None,
    ):
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
        if (args and not isinstance(args[0], QtWidgets.QWidget)) or (
            "title" in kwargs or "style" in kwargs or "color" in kwargs
        ):
            title = args[0] if len(args) > 0 else kwargs.get("title", "")
            style = args[1] if len(args) > 1 else kwargs.get("style", RibbonCategoryStyle.Normal)
            color = args[2] if len(args) > 2 else kwargs.get("color", None)
            parent = args[3] if len(args) > 3 else kwargs.get("parent", None)
        else:
            title = ""
            style = RibbonCategoryStyle.Normal
            color = None
            parent = args[0] if len(args) > 0 else kwargs.get("parent", None)
        super().__init__(parent)
        self._title = title
        self._style = style
        self._panels = {}
        self._ribbon = parent  # type: RibbonBar
        self._color = color

    def setMaximumRows(self, rows: int):
        """Set the maximum number of rows.

        :param rows: The maximum number of rows.
        """
        self._maxRows = rows

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

    def addPanelsBy(
        self,
        data: typing.Dict[
            str,  # title of the panel
            typing.Dict,  # data of the panel
        ],
    ) -> typing.Dict[str, RibbonPanel]:
        """Add panels from a dictionary.

        :param data: The dictionary. The keys are the titles of the panels. The value is a dictionary of
                     arguments. the argument showPanelOptionButton is a boolean to decide whether to show
                     the panel option button, the rest arguments are passed to the RibbonPanel.addWidgetsBy() method.
                     The dict is of the form:

                     .. code-block:: python

                        {
                            "panel-title": {
                                "showPanelOptionButton": True,
                                "widgets": {
                                    "widget-name": {
                                        "type": "Button",
                                        "arguments": {
                                            "key1": "value1",
                                            "key2": "value2"
                                        }
                                    },
                                }
                            },
                        }
        :return: A dictionary of the newly created panels.
        """
        panels = {}
        for title, panel_data in data.items():
            showPanelOptionButton = panel_data.get("showPanelOptionButton", True)
            panels[title] = self.addPanel(title, showPanelOptionButton)
            panels[title].addWidgetsBy(panel_data.get("widgets", {}))
        return panels

    def addPanel(self, title: str, showPanelOptionButton=True) -> RibbonPanel:
        """Add a new panel to the category.

        :param title: The title of the panel.
        :param showPanelOptionButton: Whether to show the panel option button.
        :return: The newly created panel.
        """
        panel = RibbonPanel(title, maxRows=self._maxRows, showPanelOptionButton=showPanelOptionButton, parent=self)
        panel.setFixedHeight(
            self.height()
            - self._mainLayout.spacing()
            - self._mainLayout.contentsMargins().top()
            - self._mainLayout.contentsMargins().bottom()
        )
        self._panels[title] = panel
        self.addWidget(panel)  # type: ignore
        self.addWidget(RibbonSeparator(width=10))  # type: ignore
        return panel

    def removePanel(self, title: str):
        """Remove a panel from the category.

        :param title: The title of the panel.
        """
        # self._panelLayout.removeWidget(self._panels[title])
        self.removeWidget(self._panels[title])
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
        self.showContextCategories() if visible else self.hideContextCategories()
