import typing
from enum import IntEnum

from PyQt5 import QtWidgets, QtCore, QtGui

from .category import RibbonCategory, RibbonContextCategory, RibbonNormalCategory, CategoryStyle, contextColors
from .separator import RibbonHorizontalSeparator
from .titlewidget import RibbonTitleWidget
from .utils import package_source_dir


class RibbonStyle(IntEnum):
    Default = 0
    Debug = 1


class RibbonBar(QtWidgets.QFrame):
    """The RibbonBar class is top level widget that contains the ribbon.
    """
    #: Signal, The help button was clicked.
    helpButtonClicked = QtCore.pyqtSignal(bool)

    #: The categories of the ribbon.
    _categories: typing.List[RibbonCategory] = []
    _contextCategoryCount = 0

    #: Whether the ribbon is visible.
    _ribbonVisible = True

    #: heights of the ribbon elements
    _ribbonHeight = 240

    def __init__(self, title='PyQtRibbon', parent=None):
        """Create a new ribbon.

        :param title: The title of the ribbon.
        :param parent: The parent widget of the ribbon.
        """
        super().__init__(parent)
        self._categories = []
        self.setFixedHeight(self._ribbonHeight)

        self._titleWidget = RibbonTitleWidget(title, self)
        self._separator = RibbonHorizontalSeparator(width=1, parent=self)
        self._stackedWidget = QtWidgets.QStackedWidget(self)

        # Main layout
        self._mainLayout = QtWidgets.QVBoxLayout(self)
        self._mainLayout.setContentsMargins(5, 5, 5, 5)
        self._mainLayout.setSpacing(5)
        self._mainLayout.addWidget(self._titleWidget, 0)
        self._mainLayout.addWidget(self._separator, 0)
        self._mainLayout.addWidget(self._stackedWidget, 1)
        self._mainLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)

        # Connect signals
        self._titleWidget.helpButtonClicked.connect(self.helpButtonClicked)
        self._titleWidget.collapseRibbonButtonClicked.connect(self._collapseButtonClicked)
        self._titleWidget.tabBar().currentChanged.connect(
            lambda index: self._stackedWidget.setCurrentIndex(index)
        )
        self.setRibbonStyle(RibbonStyle.Default)

    def setRibbonStyle(self, style: RibbonStyle):
        """Set the style of the ribbon.

        :param style: The style to set.
        """
        stylefiles = {
            RibbonStyle.Default: 'default',
            RibbonStyle.Debug: 'debug'
        }
        if style == RibbonStyle.Default:
            self.setStyleSheet(open(package_source_dir() + '/' + f"styles/{stylefiles[style]}.qss", "r").read())

    def applicationOptionButton(self):
        """Return the application button."""
        return self._titleWidget.applicationButton()

    def setApplicationIcon(self, icon: QtGui.QIcon):
        """Set the application icon.

        :param icon: The icon to set.
        """
        self._titleWidget.applicationButton().setIcon(icon)

    def addApplicationOptionAction(self, action: QtWidgets.QAction):
        """Add a display option to the ribbon.

        :param action: The action of the display option.
        """
        self._titleWidget.applicationMenu().addAction(action)
        self._titleWidget.applicationButton().setMenu(self._titleWidget.applicationMenu()
                                                      if self._titleWidget.applicationMenu().actions() else None)

    def ribbonHeight(self) -> int:
        """Get the total height of the ribbon.

        :return: The height of the ribbon.
        """
        return self._ribbonHeight

    def setRibbonHeight(self, height: int):
        """Set the total height of the ribbon.

        :param height: The height to set.
        """
        self._ribbonHeight = height
        self.setFixedHeight(height)

    def tabBar(self):
        """Return the tab bar of the ribbon.

        :return: The tab bar of the ribbon.
        """
        return self._titleWidget.tabBar()

    def tabBarHeight(self) -> int:
        """Get the height of the tab bar.

        :return: The height of the tab bar.
        """
        return self._titleWidget.tabBarHeight()

    def setTabBarHeight(self, height: int = 50):
        """Set the height of the tab bar.

        :param height: The height to set.
        """
        self._titleWidget.setTabBarHeight(height)

    def quickAccessToolBar(self) -> QtWidgets.QToolBar:
        """Return the quick access toolbar of the ribbon.

        :return: The quick access toolbar of the ribbon.
        """
        return self._titleWidget.quickAccessToolBar()

    def addQuickAccessButton(self, button: QtWidgets.QToolButton):
        """Add a widget to the quick access bar.

        :param button: The button to add.
        """
        button.setAutoRaise(True)
        self._titleWidget.quickAccessToolBar().addWidget(button)

    def setQuickAccessButtonHeight(self, height: int = 40):
        """Set the height of the quick access buttons.

        :param height: The height to set.
        """
        self._titleWidget.setQuickAccessButtonHeight(height)

    def title(self):
        """Return the title of the ribbon.

        :return: The title of the ribbon.
        """
        return self._titleWidget.title()

    def setTitle(self, title: str):
        """Set the title of the ribbon.

        :param title: The title to set.
        """
        self._titleWidget.setTitle(title)

    def rightToolBar(self) -> QtWidgets.QToolBar:
        """Return the right toolbar of the ribbon.

        :return: The right toolbar of the ribbon.
        """
        return self._titleWidget.rightToolBar()

    def addRightToolButton(self, button: QtWidgets.QToolButton):
        """Add a widget to the right button bar.

        :param button: The button to add.
        """
        button.setAutoRaise(True)
        self._titleWidget.addRightToolButton(button)

    def setRightToolBarHeight(self, height: int = 24):
        """Set the height of the right buttons.

        :param height: The height to set.
        """
        self._titleWidget.setRightToolBarHeight(height)

    def setHelpButtonIcon(self, icon: QtGui.QIcon):
        """Set the icon of the help button.

        :param icon: The icon to set.
        """
        self._titleWidget.setHelpButtonIcon(icon)

    def removeHelpButton(self):
        """Remove the help button from the ribbon."""
        self._titleWidget.removeHelpButton()

    def categories(self) -> typing.List[RibbonCategory]:
        """Return a list of categories of the ribbon.

        :return: A list of categories of the ribbon.
        """
        return self._categories

    def addCategory(
        self,
        title: str,
        style=CategoryStyle.Normal,
        color: QtGui.QColor = None,
    ) -> typing.Union[RibbonNormalCategory, RibbonContextCategory]:
        """Add a new category to the ribbon.

        :param title: The title of the category.
        :param style: The buttonStyle of the category.
        :param color: The color of the context category, only used if style is Context, if None, the default color
                      will be used.
        :return: The newly created category.
        """
        if style == CategoryStyle.Context:
            if color is None:
                color = contextColors[self._contextCategoryCount % len(contextColors)]
            self._contextCategoryCount += 1
        category = (RibbonContextCategory(title, color, self) if style == CategoryStyle.Context else
                    RibbonNormalCategory(title, self))
        category.setFixedHeight(self._ribbonHeight -
                                self._mainLayout.spacing() * 2 -
                                self._mainLayout.contentsMargins().top() -
                                self._mainLayout.contentsMargins().bottom() -
                                self._titleWidget.height() -
                                self._separator.height() - 4)  # 4: extra space for drawing lines when debugging
        if style == CategoryStyle.Normal:
            self._categories.append(category)
            self._titleWidget.tabBar().addTab(title, color)
            self._stackedWidget.addWidget(category)
        elif style == CategoryStyle.Context:
            category.hide()
        return category

    def addNormalCategory(self, title: str) -> RibbonNormalCategory:
        """Add a new category to the ribbon.

        :param title: The title of the category.
        :return: The newly created category.
        """
        return self.addCategory(title, CategoryStyle.Normal)

    def addContextCategory(self, title: str, color: QtGui.QColor = None) -> RibbonContextCategory:
        """Add a new context category to the ribbon.

        :param title: The title of the category.
        :param color: The color of the context category, if None, the default color will be used.
        :return: The newly created category.
        """
        return self.addCategory(title, CategoryStyle.Context, color)

    def showContextCategory(self, category: RibbonContextCategory):
        """Show the given category, if it is not a context category, nothing happens.

        :param category: The category to show.
        """
        self._categories.append(category)
        self._titleWidget.tabBar().addTab(category.title(), category.color())
        self._titleWidget.tabBar().setCurrentIndex(self._titleWidget.tabBar().count() - 1)
        self._stackedWidget.addWidget(category)
        self._stackedWidget.setCurrentIndex(self._titleWidget.tabBar().count() - 1)

    def hideContextCategory(self, category: RibbonContextCategory):
        """Hide the given category, if it is not a context category, nothing happens.

        :param category: The category to hide.
        """
        self._categories.remove(category)
        self.tabBar().removeTab(self.tabBar().indexOf(category.title()))
        self._stackedWidget.removeWidget(category)

    def tabRect(self, category: RibbonCategory) -> QtCore.QRect:
        """Get the rectangle of the tab of the given category.

        :param category: The category to get the tab rectangle of.
        :return: The rectangle of the tab.
        """
        return self.tabBar().tabRect(self._categories.index(category))

    def removeCategory(self, category: RibbonCategory):
        """Remove a category from the ribbon.

        :param category: The category to remove.
        """
        index = self._categories.index(category)
        self.tabBar().removeTab(index)
        self._stackedWidget.removeWidget(self._stackedWidget.widget(index))

    def setCurrentCategory(self, category: RibbonCategory):
        """Set the current category.

        :param category: The category to set.
        """
        index = self._categories.index(category)
        self.tabBar().setCurrentIndex(index)
        self._stackedWidget.setCurrentIndex(index)

    def collapseRibbonButton(self) -> QtWidgets.QToolButton:
        """Return the collapse ribbon button.

        :return: The collapse ribbon button.
        """
        return self._titleWidget.collapseRibbonButton()

    def setCollapseButtonIcon(self, icon: QtGui.QIcon):
        """Set the icon of the min button.

        :param icon: The icon to set.
        """
        self._titleWidget.setCollapseButtonIcon(icon)

    def removeCollapseButton(self):
        """Remove the min button from the ribbon."""
        self._titleWidget.removeCollapseButton()

    def minimumSizeHint(self) -> QtCore.QSize:
        """Return the minimum size hint of the widget.

        :return: The minimum size hint.
        """
        return QtCore.QSize(super().minimumSizeHint().width(), self._ribbonHeight)

    def _collapseButtonClicked(self):
        self.tabBar().currentChanged.connect(self.showRibbon)
        if self._stackedWidget.isVisible():
            self.hideRibbon()
        else:
            self.showRibbon()

    def showRibbon(self):
        """Show the ribbon."""
        if not self._ribbonVisible:
            self._ribbonVisible = True
            self.collapseRibbonButton().setToolTip("Collapse Ribbon")
            self.collapseRibbonButton().setIcon(QtGui.QIcon('icons/up.png'))
            self._separator.setVisible(True)
            self._stackedWidget.setVisible(True)
            self.setFixedSize(self.sizeHint())

    def hideRibbon(self):
        """Hide the ribbon."""
        if self._ribbonVisible:
            self._ribbonVisible = False
            self.collapseRibbonButton().setToolTip("Expand Ribbon")
            self.collapseRibbonButton().setIcon(QtGui.QIcon('icons/down.png'))
            self._separator.setVisible(False)
            self._stackedWidget.setVisible(False)
            self.setFixedSize(self.sizeHint().width(), self._titleWidget.tabBarHeight() + 5)

    def ribbonVisible(self) -> bool:
        """Get the visibility of the ribbon.

        :return: True if the ribbon is visible, False otherwise.
        """
        return self._ribbonVisible

    def setRibbonVisible(self, visible: bool):
        """Set the visibility of the ribbon.

        :param visible: True to show the ribbon, False to hide it.
        """
        if visible:
            self.showRibbon()
        else:
            self.hideRibbon()
