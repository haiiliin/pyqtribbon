import typing

from PyQt5 import QtWidgets, QtCore, QtGui

from .category import RibbonCategory, RibbonContextCategory, RibbonNormalCategory, CategoryStyle, contextColors
from .tabwidget import RibbonTabWidget


class RibbonDisplayOptionsButton(QtWidgets.QToolButton):
    pass


class Ribbon(QtWidgets.QFrame):
    #: Signal: The help button was clicked.
    helpButtonClicked = QtCore.pyqtSignal(bool)

    #: The signal that is emitted when the display options button is clicked.
    displayOptionsButtonClicked = QtCore.pyqtSignal(bool)

    #: The categories of the ribbon.
    _categories: typing.List[RibbonCategory] = []
    _contextCategoryCount = 0

    #: Whether the ribbon is visible.
    _ribbonVisible = True

    #: heights of the ribbon elements
    _ribbonHeight = 240
    _displayOptionsButtonHeight = 24

    def __init__(self, parent=None):
        super().__init__(parent)
        self._categories = []
        self.setFixedHeight(self._ribbonHeight)

        self._tabWidget = RibbonTabWidget(self)
        self._tabWidget.helpButtonClicked.connect(self.helpButtonClicked)

        # stacked widget
        self._stackedWidget = QtWidgets.QStackedWidget(self)

        # Display options button
        self._displayOptionsLayout = QtWidgets.QVBoxLayout()
        self._displayOptionsLayout.setContentsMargins(0, 0, 0, 0)
        self._displayOptionsLayout.setSpacing(5)
        self._displayOptionsLayout.addSpacerItem(
            QtWidgets.QSpacerItem(
                10, 10, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
            )
        )
        self._displayOptionsButton = RibbonDisplayOptionsButton()
        self._displayOptionsButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self._displayOptionsButton.setIcon(QtGui.QIcon("icons/down.png"))
        self._displayOptionsButton.setIconSize(QtCore.QSize(self._displayOptionsButtonHeight,
                                                            self._displayOptionsButtonHeight))
        self._displayOptionsButton.setText("Ribbon Display Options")
        self._displayOptionsButton.setToolTip("Ribbon Display Options")
        self._displayOptionsButton.setEnabled(True)
        self._displayOptionsButton.setAutoRaise(True)
        self._displayOptionsButton.clicked.connect(self.displayOptionsButtonClicked)
        self._displayOptionsLayout.addWidget(self._displayOptionsButton, 0, QtCore.Qt.AlignBottom)
        self._displayOptionsMenu = QtWidgets.QMenu()

        # layout for the display options button and stacked widget
        self._horizontalWidget = QtWidgets.QFrame(self)
        # self._horizontalWidget.setStyleSheet("QFrame { background-color: white; }")
        self._horizontalLayout = QtWidgets.QHBoxLayout(self._horizontalWidget)
        self._horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self._horizontalLayout.setSpacing(5)
        self._horizontalLayout.addWidget(self._stackedWidget, 1)
        self._horizontalLayout.addLayout(self._displayOptionsLayout, 0)

        # Main layout
        self._mainLayout = QtWidgets.QVBoxLayout(self)
        self._mainLayout.setContentsMargins(5, 5, 5, 5)
        self._mainLayout.setSpacing(5)
        self._mainLayout.addWidget(self._tabWidget, 0)
        self._mainLayout.addWidget(self._horizontalWidget, 1)

        # Connect signals
        self._tabWidget.collapseRibbonButtonClicked.connect(self._collapseButtonClicked)
        self._tabWidget.tabBar().currentChanged.connect(
            lambda index: self._stackedWidget.setCurrentIndex(index)
        )

    def applicationOptionButton(self):
        """Return the application button."""
        return self._tabWidget.applicationButton()

    def setApplicationIcon(self, icon: QtGui.QIcon):
        """Set the application icon.

        :param icon: The icon to set.
        """
        self._tabWidget.applicationButton().setIcon(icon)

    def addApplicationOptionAction(self, action: QtWidgets.QAction):
        """Add a display option to the category.

        :param action: The action of the display option.
        """
        self._tabWidget.applicationMenu().addAction(action)
        self._tabWidget.applicationButton().setMenu(self._tabWidget.applicationMenu()
                                                    if self._tabWidget.applicationMenu().actions() else None)

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
        return self._tabWidget.tabBar()

    def tabBarHeight(self) -> int:
        """Get the height of the tab bar.

        :return: The height of the tab bar.
        """
        return self._tabWidget.tabBarHeight()

    def setTabBarHeight(self, height: int = 50):
        """Set the height of the tab bar.

        :param height: The height to set.
        """
        self._tabWidget.setTabBarHeight(height)

    def quickAccessToolBar(self) -> QtWidgets.QToolBar:
        """Return the quick access toolbar of the ribbon.

        :return: The quick access toolbar of the ribbon.
        """
        return self._tabWidget.quickAccessToolBar()

    def addQuickAccessButton(self, button: QtWidgets.QToolButton):
        """Add a widget to the quick access bar.

        :param button: The button to add.
        """
        self._tabWidget.quickAccessToolBar().addWidget(button)

    def setQuickAccessButtonHeight(self, height: int = 40):
        """Set the height of the quick access buttons.

        :param height: The height to set.
        """
        self._tabWidget.setQuickAccessButtonHeight(height)

    def rightToolBar(self) -> QtWidgets.QToolBar:
        """Return the right toolbar of the ribbon.

        :return: The right toolbar of the ribbon.
        """
        return self._tabWidget.rightToolBar()

    def addRightToolButton(self, button: QtWidgets.QToolButton):
        """Add a widget to the right button bar.

        :param button: The button to add.
        """
        self._tabWidget.addRightToolButton(button)

    def setRightToolBarHeight(self, height: int = 24):
        """Set the height of the right buttons.

        :param height: The height to set.
        """
        self._tabWidget.setRightToolBarHeight(height)

    def setHelpButtonIcon(self, icon: QtGui.QIcon):
        """Set the icon of the help button.

        :param icon: The icon to set.
        """
        self._tabWidget.setHelpButtonIcon(icon)

    def removeHelpButton(self):
        """Remove the help button from the ribbon."""
        self._tabWidget.removeHelpButton()

    def displayOptionsButton(self) -> RibbonDisplayOptionsButton:
        """Return the display options button.

        :return: The display options button.
        """
        return self._displayOptionsButton

    def addDisplayOptionAction(self, action: QtWidgets.QAction):
        """Add a display option to the category.

        :param action: The action of the display option.
        """
        self._displayOptionsMenu.addAction(action)
        self._displayOptionsButton.setMenu(self._displayOptionsMenu if self._displayOptionsMenu.actions() else None)

    def setDisplayOptionsButtonHeight(self, height: int = 24):
        """Set the height of the display options button.

        :param height: The height to set.
        """
        self._displayOptionsButtonHeight = height
        self._displayOptionsButton.setIconSize(QtCore.QSize(height, height))

    def categories(self) -> typing.List[RibbonCategory]:
        """Return the list of categories of the ribbon.

        :return: The list of categories of the ribbon.
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
                                self._tabWidget.sizeHint().height() -
                                self._mainLayout.spacing() -
                                self._mainLayout.contentsMargins().top() -
                                self._mainLayout.contentsMargins().bottom() -
                                self._tabWidget.layout().spacing() -
                                self._tabWidget.layout().contentsMargins().top() -
                                self._tabWidget.layout().contentsMargins().bottom() -
                                self._horizontalLayout.spacing() -
                                self._horizontalLayout.contentsMargins().top() -
                                self._horizontalLayout.contentsMargins().bottom() - 4)
        category.displayOptionsButtonClicked.connect(self.displayOptionsButtonClicked)
        if style == CategoryStyle.Normal:
            self._categories.append(category)
            self._tabWidget.tabBar().addTab(title, color)
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
        self._tabWidget.tabBar().addTab(category.title(), category.color())
        self._tabWidget.tabBar().setCurrentIndex(self._tabWidget.tabBar().count() - 1)
        self._stackedWidget.addWidget(category)
        self._stackedWidget.setCurrentIndex(self._tabWidget.tabBar().count() - 1)

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
        return self._tabWidget.collapseRibbonButton()

    def setCollapseButtonIcon(self, icon: QtGui.QIcon):
        """Set the icon of the min button.

        :param icon: The icon to set.
        """
        self._tabWidget.setCollapseButtonIcon(icon)

    def removeCollapseButton(self):
        """Remove the min button from the ribbon."""
        self._tabWidget.removeCollapseButton()

    def minimumSizeHint(self) -> QtCore.QSize:
        """Return the minimum size hint of the widget.

        :return: The minimum size hint.
        """
        return QtCore.QSize(super().minimumSizeHint().width(), self._ribbonHeight)

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(self.width(), self._ribbonHeight)

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
            self._horizontalWidget.setVisible(True)
            self.setFixedSize(self.sizeHint())

    def hideRibbon(self):
        """Hide the ribbon."""
        if self._ribbonVisible:
            self._ribbonVisible = False
            self.collapseRibbonButton().setToolTip("Expand Ribbon")
            self.collapseRibbonButton().setIcon(QtGui.QIcon('icons/down.png'))
            self._horizontalWidget.setVisible(False)
            self.setFixedSize(self.sizeHint().width(), self._tabWidget.tabBarHeight())

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
