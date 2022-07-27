import typing
from enum import IntEnum

from qtpy import QtWidgets, QtCore, QtGui

from .category import (RibbonCategory, RibbonContextCategory, RibbonNormalCategory,
                       RibbonCategoryStyle, contextColors, RibbonContextCategories)
from .tabbar import RibbonTabBar
from .titlewidget import RibbonTitleWidget
from .utils import data_file_path


class RibbonStyle(IntEnum):
    Default = 0
    Debug = 1


Debug = RibbonStyle.Debug
Default = RibbonStyle.Default


class RibbonStackedWidget(QtWidgets.QStackedWidget):
    """Stacked widget that is used to display the ribbon."""

    def __init__(self, parent=None):
        """Create a new ribbon stacked widget.

        :param parent: The parent widget.
        """
        super().__init__(parent)
        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setOffset(2, 2)
        self.setGraphicsEffect(effect)


class RibbonBar(QtWidgets.QMenuBar):
    """The RibbonBar class is the top level widget that contains the ribbon.
    """
    #: Signal, the help button was clicked.
    helpButtonClicked = QtCore.Signal(bool)

    #: The categories of the ribbon.
    _categories: typing.Dict[str, RibbonCategory] = {}
    _contextCategoryCount = 0

    #: Whether the ribbon is visible.
    _ribbonVisible = True

    #: heights of the ribbon elements
    _ribbonHeight = 240

    @typing.overload
    def __init__(self, title: str = '', parent=None):
        pass

    @typing.overload
    def __init__(self, parent=None):
        pass

    def __init__(self, *args, **kwargs):
        """Create a new ribbon.

        :param title: The title of the ribbon.
        :param parent: The parent widget of the ribbon.
        """
        if (args and not isinstance(args[0], QtWidgets.QWidget)) or (kwargs and 'title' in kwargs):
            title = args[0] if len(args) > 0 else kwargs.get('title', '')
            parent = kwargs.get('parent', None)
        else:
            title = ''
            parent = args[1] if len(args) > 1 else kwargs.get('parent', None)
        super().__init__(parent)
        self._categories = {}
        self.setFixedHeight(self._ribbonHeight)

        self._titleWidget = RibbonTitleWidget(title, self)
        self._stackedWidget = RibbonStackedWidget(self)

        # Main layout
        self._mainLayout = QtWidgets.QVBoxLayout(self)
        self._mainLayout.setContentsMargins(5, 5, 5, 5)
        self._mainLayout.setSpacing(5)
        self._mainLayout.addWidget(self._titleWidget, 0)
        self._mainLayout.addWidget(self._stackedWidget, 1)
        self._mainLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)

        # Connect signals
        self._titleWidget.helpButtonClicked.connect(self.helpButtonClicked)
        self._titleWidget.collapseRibbonButtonClicked.connect(self._collapseButtonClicked)
        self._titleWidget.tabBar().currentChanged.connect(self.showCategoryByIndex)
        self.setRibbonStyle(RibbonStyle.Default)

    def actionAt(self, QPoint):
        raise NotImplementedError('RibbonBar.actionAt() is not implemented in the ribbon bar.')

    def actionGeometry(self, QAction):
        raise NotImplementedError('RibbonBar.actionGeometry() is not implemented in the ribbon bar.')

    def activeAction(self):
        raise NotImplementedError('RibbonBar.activeAction() is not implemented in the ribbon bar.')

    def addMenu(self, *__args):
        raise NotImplementedError('RibbonBar.addMenu() is not implemented in the ribbon bar.')

    def addAction(self, *__args):
        raise NotImplementedError('RibbonBar.addAction() is not implemented in the ribbon bar.')

    def addSeparator(self):
        raise NotImplementedError('RibbonBar.addSeparator() is not implemented in the ribbon bar.')

    def clear(self):
        raise NotImplementedError('RibbonBar.clear() is not implemented in the ribbon bar.')

    def cornerWidget(self, corner=None):
        raise NotImplementedError('RibbonBar.cornerWidget() is not implemented in the ribbon bar.')

    def insertMenu(self, QAction, QMenu):
        raise NotImplementedError('RibbonBar.insertMenu() is not implemented in the ribbon bar.')

    def insertSeparator(self, QAction):
        raise NotImplementedError('RibbonBar.insertSeparator() is not implemented in the ribbon bar.')

    def isDefaultUp(self):
        raise NotImplementedError('RibbonBar.isDefaultUp() is not implemented in the ribbon bar.')

    def isNativeMenuBar(self):
        raise NotImplementedError('RibbonBar.isNativeMenuBar() is not implemented in the ribbon bar.')

    def setActiveAction(self, QAction):
        raise NotImplementedError('RibbonBar.setActiveAction() is not implemented in the ribbon bar.')

    def setCornerWidget(self, QWidget, corner=None):
        raise NotImplementedError('RibbonBar.setCornerWidget() is not implemented in the ribbon bar.')

    def setDefaultUp(self, up):
        raise NotImplementedError('RibbonBar.setDefaultUp() is not implemented in the ribbon bar.')

    def setNativeMenuBar(self, bar):
        raise NotImplementedError('RibbonBar.setNativeMenuBar() is not implemented in the ribbon bar.')

    def setRibbonStyle(self, style: RibbonStyle):
        """Set the style of the ribbon.

        :param style: The style to set.
        """
        self.setStyleSheet(open(data_file_path(f"styles/base.qss"), "r").read() +
                           open(data_file_path(f"styles/{style.name.lower()}.qss"), "r").read())

    def applicationOptionButton(self) -> QtWidgets.QToolButton:
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

    def tabBar(self) -> RibbonTabBar:
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
        """Add a button to the quick access bar.

        :param button: The button to add.
        """
        button.setAutoRaise(True)
        self._titleWidget.quickAccessToolBar().addWidget(button)

    def setQuickAccessButtonHeight(self, height: int = 40):
        """Set the height of the quick access buttons.

        :param height: The height to set.
        """
        self._titleWidget.setQuickAccessButtonHeight(height)

    def title(self) -> str:
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
        
    def helpRibbonButton(self) -> QtWidgets.QToolButton:
        """Return the help button of the ribbon.

        :return: The help button of the ribbon.
        """
        return self._titleWidget.helpRibbonButton()

    def setHelpButtonIcon(self, icon: QtGui.QIcon):
        """Set the icon of the help button.

        :param icon: The icon to set.
        """
        self._titleWidget.setHelpButtonIcon(icon)

    def removeHelpButton(self):
        """Remove the help button from the ribbon."""
        self._titleWidget.removeHelpButton()

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
        
    def category(self, name: str) -> RibbonCategory:
        """Return the category with the given name.

        :param name: The name of the category.
        :return: The category with the given name.
        """
        return self._categories[name]

    def categories(self) -> typing.Dict[str, RibbonCategory]:
        """Return a list of categories of the ribbon.

        :return: A dict of categories of the ribbon.
        """
        return self._categories

    def addCategory(
        self,
        title: str,
        style=RibbonCategoryStyle.Normal,
        color: QtGui.QColor = None,
    ) -> typing.Union[RibbonNormalCategory, RibbonContextCategory]:
        """Add a new category to the ribbon.

        :param title: The title of the category.
        :param style: The button style of the category.
        :param color: The color of the context category, only used if style is Context, if None, the default color
                      will be used.
        :return: The newly created category.
        """
        if title in self._categories:
            raise ValueError(f"Category with title {title} already exists.")
        if style == RibbonCategoryStyle.Context:
            if color is None:
                color = contextColors[self._contextCategoryCount % len(contextColors)]
                self._contextCategoryCount += 1
        category = (RibbonContextCategory(title, color, self) if style == RibbonCategoryStyle.Context else
                    RibbonNormalCategory(title, self))
        category.setFixedHeight(self._ribbonHeight -
                                self._mainLayout.spacing() * 2 -
                                self._mainLayout.contentsMargins().top() -
                                self._mainLayout.contentsMargins().bottom() -
                                self._titleWidget.height())  # 4: extra space for drawing lines when debugging
        self._categories[title] = category
        self._stackedWidget.addWidget(category)
        if style == RibbonCategoryStyle.Normal:
            self._titleWidget.tabBar().addTab(title, color)
        elif style == RibbonCategoryStyle.Context:
            category.hide()
        return category

    def addNormalCategory(self, title: str) -> RibbonNormalCategory:
        """Add a new category to the ribbon.

        :param title: The title of the category.
        :return: The newly created category.
        """
        return self.addCategory(title, RibbonCategoryStyle.Normal)

    def addContextCategory(
        self,
        title: str,
        color: typing.Union[QtGui.QColor, QtCore.Qt.GlobalColor] = None,
    ) -> RibbonContextCategory:
        """Add a new context category to the ribbon.

        :param title: The title of the category.
        :param color: The color of the context category, if None, the default color will be used.
        :return: The newly created category.
        """
        return self.addCategory(title, RibbonCategoryStyle.Context, color)

    def addContextCategories(
        self,
        name: str,
        titles: typing.List[str],
        color: typing.Union[QtGui.QColor, QtCore.Qt.GlobalColor] = None,
    ) -> RibbonContextCategories:
        """Add a group of context categories with the same tab color to the ribbon.

        :param name: The name of the context categories.
        :param titles: The title of the category.
        :param color: The color of the context category, if None, the default color will be used.
        :return: The newly created category.
        """
        if color is None:
            color = contextColors[self._contextCategoryCount % len(contextColors)]
            self._contextCategoryCount += 1
        categories = RibbonContextCategories(
            name, color, {title: self.addContextCategory(title, color) for title in titles}, self,
        )
        return categories

    def showCategoryByIndex(self, index: int):
        """Show category by tab index

        :param index: tab index
        """
        title = self._titleWidget.tabBar().tabText(index)
        if title in self._categories:
            self._stackedWidget.setCurrentWidget(self._categories[title])

    def showContextCategory(self, category: typing.Union[RibbonContextCategory, RibbonContextCategories]):
        """Show the given category or categories, if it is not a context category, nothing happens.

        :param category: The category to show.
        """
        if isinstance(category, RibbonContextCategory):
            self._titleWidget.tabBar().addTab(category.title(), category.color())
            self._titleWidget.tabBar().setCurrentIndex(self._titleWidget.tabBar().count() - 1)
            self._stackedWidget.setCurrentWidget(category)
        elif isinstance(category, RibbonContextCategories):
            categories = category
            titles = list(categories.keys())
            self._titleWidget.tabBar().addAssociatedTabs(categories.name(), titles, categories.color())
            self._titleWidget.tabBar().setCurrentIndex(self._titleWidget.tabBar().count() - len(titles))
            self._stackedWidget.setCurrentWidget(categories[titles[0]])

    def hideContextCategory(self, category: typing.Union[RibbonContextCategory, RibbonContextCategories]):
        """Hide the given category or categories, if it is not a context category, nothing happens.

        :param category: The category to hide.
        """
        if isinstance(category, RibbonContextCategory):
            self.tabBar().removeTab(self.tabBar().indexOf(category.title()))
        elif isinstance(category, RibbonContextCategories):
            categories = category
            for c in categories:
                self.tabBar().removeTab(self.tabBar().indexOf(c.title()))

    def categoryVisible(self, category: RibbonCategory) -> bool:
        """Return whether the category is shown.

        :param category: The category to check.

        :return: Whether the category is shown.
        """
        return category.title() in self._titleWidget.tabBar().tabTitles()

    def removeCategory(self, category: RibbonCategory):
        """Remove a category from the ribbon.

        :param category: The category to remove.
        """
        index = self._titleWidget.tabBar().indexOf(category.title())
        self.tabBar().removeTab(index)
        self._stackedWidget.removeWidget(category)

    def removeCategories(self, categories: RibbonContextCategories):
        """Remove a list of categories from the ribbon.

        :param categories: The categories to remove.
        """
        for category in categories.values():
            self.removeCategory(category)

    def setCurrentCategory(self, category: RibbonCategory):
        """Set the current category.

        :param category: The category to set.
        """
        self._stackedWidget.setCurrentWidget(category)
        if category.title() in self._titleWidget.tabBar().tabTitles():
            self._titleWidget.tabBar().setCurrentIndex(self._titleWidget.tabBar().indexOf(category.title()))
        else:
            raise ValueError(f"Category {category.title()} is not in the ribbon, "
                             f"please show the context category/categories first.")

    def currentCategory(self) -> RibbonCategory:
        """Return the current category.

        :return: The current category.
        """
        return self._categories[self._titleWidget.tabBar().tabText(self._titleWidget.tabBar().currentIndex())]

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
            self.collapseRibbonButton().setIcon(QtGui.QIcon(data_file_path('icons/up.png')))
            self._separator.setVisible(True)
            self._stackedWidget.setVisible(True)
            self.setFixedSize(self.sizeHint())

    def hideRibbon(self):
        """Hide the ribbon."""
        if self._ribbonVisible:
            self._ribbonVisible = False
            self.collapseRibbonButton().setToolTip("Expand Ribbon")
            self.collapseRibbonButton().setIcon(QtGui.QIcon(data_file_path('icons/down.png')))
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
