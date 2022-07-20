import typing

from PyQt5 import QtWidgets, QtCore, QtGui

from .category import Category, ContextCategory, NormalCategory, CategoryStyle, contextColors
from .tabbar import TabBar


class Ribbon(QtWidgets.QWidget):
    #: Signal: The help button was clicked.
    helpButtonClicked = QtCore.pyqtSignal(bool)

    #: The signal that is emitted when the display options button is clicked.
    displayOptionsButtonClicked = QtCore.pyqtSignal(bool)

    #: The categories of the ribbon.
    _categories: typing.List[Category] = []
    _contextCategoryCount = 0

    #: Buttons
    _quickAccessButtons = []
    _rightToolButtons = []

    #: heights of the ribbon elements
    _ribbonHeight = 220
    _quickAccessButtonHeight = 32
    _rightButtonHeight = 24

    def __init__(self, parent=None):
        super().__init__(parent)
        self._categories = []
        self.setFixedHeight(self._ribbonHeight)

        # Tab bar layout
        self._tabsWidget = QtWidgets.QWidget(self)
        self._tabsLayout = QtWidgets.QHBoxLayout(self)
        self._tabsLayout.setContentsMargins(0, 0, 0, 0)
        self._tabsLayout.setSpacing(0)
        self._tabsWidget.setLayout(self._tabsLayout)

        # Application
        self._applicationButton = QtWidgets.QToolButton()
        self._applicationButton.setIcon(QtGui.QIcon('icons/python.png'))
        self._applicationButton.setIconSize(QtCore.QSize(self._quickAccessButtonHeight, self._quickAccessButtonHeight))
        self._applicationButton.setText("File")
        self._applicationButton.setStyleSheet(
            "QToolButton { border: none; padding: 0px; } "
            "QToolButton::menu-indicator { image: none; } "
        )
        self._applicationButton.setToolTip("File")
        self._fileMenu = QtWidgets.QMenu(self)
        self._applicationButton.setMenu(self._fileMenu)

        self._quickAccessToolBarLayout = QtWidgets.QHBoxLayout()
        self._quickAccessToolBarLayout.setContentsMargins(0, 0, 0, 0)
        self._quickAccessToolBarLayout.setSpacing(0)
        self._quickAccessToolBarLayout.addWidget(self._applicationButton, 0, QtCore.Qt.AlignBottom)

        # right toolbar
        self._rightToolBar = QtWidgets.QToolBar()
        self._rightToolBar.setOrientation(QtCore.Qt.Horizontal)
        self._rightToolBar.setIconSize(QtCore.QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._collapseRibbonButton = QtWidgets.QToolButton(self)
        self._collapseRibbonButton.setIconSize(QtCore.QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._collapseRibbonButton.setIcon(QtGui.QIcon('icons/collapse-arrow.png'))
        self._collapseRibbonButton.setAutoRaise(True)
        self._collapseRibbonButton.setToolTip("Collapse Ribbon")
        self._helpButton = QtWidgets.QToolButton(self)
        self._helpButton.setIconSize(QtCore.QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._helpButton.setIcon(QtGui.QIcon("icons/help.png"))
        self._helpButton.setAutoRaise(True)
        self._helpButton.setToolTip("Help")
        self._helpButton.clicked.connect(self.helpButtonClicked)
        self.addRightToolButton(self._collapseRibbonButton)
        self.addRightToolButton(self._helpButton)

        # category tab bar
        self._tabBar = TabBar(self)
        font = self._tabBar.font()
        font.setPointSize(font.pointSize() + 3)
        self._tabBar.setFont(font)
        self._tabBar.setShape(QtWidgets.QTabBar.RoundedNorth)
        self._tabBar.setDocumentMode(True)

        self._tabsLayout.addLayout(self._quickAccessToolBarLayout)
        self._tabsLayout.addWidget(self._tabBar)
        self._tabsLayout.addSpacerItem(
            QtWidgets.QSpacerItem(
                10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
            )
        )
        self._tabsLayout.addWidget(self._rightToolBar)

        # stacked widget
        self._stackedWidget = QtWidgets.QStackedWidget(self)

        # Main layout
        self._mainLayout = QtWidgets.QVBoxLayout(self)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(5)
        self._mainLayout.addWidget(self._tabsWidget, 0)
        self._mainLayout.addWidget(self._stackedWidget, 1)

        # Connect signals
        self._collapseRibbonButton.clicked.connect(self._collapseButtonClicked)
        self._tabBar.currentChanged.connect(
            lambda index: self._stackedWidget.setCurrentIndex(index)
        )

    def setFileTitle(self, title: str):
        """Set the title of the file menu.

        :param title: The title to set.
        """
        self._tabBar.setTabText(0, title)

    def setFileMenu(self, menu: QtWidgets.QMenu):
        """Set the file menu of the ribbon.

        :param menu: The menu to set.
        """
        self._fileMenu = menu
        self._applicationButton.setMenu(menu)

    def tabBar(self) -> QtWidgets.QTabBar:
        """Return the tab bar of the ribbon.

        :return: The tab bar of the ribbon.
        """
        return self._tabBar

    def categories(self) -> typing.List[Category]:
        """Return the list of categories of the ribbon.

        :return: The list of categories of the ribbon.
        """
        return self._categories

    def addCategory(
        self,
        title: str,
        style=CategoryStyle.Normal,
        color: QtGui.QColor = None,
    ) -> typing.Union[NormalCategory, ContextCategory]:
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
        category = (ContextCategory(title, color, self) if style == CategoryStyle.Context else
                    NormalCategory(title, self))
        category.setFixedHeight(self._ribbonHeight -
                                self._tabsWidget.sizeHint().height() -
                                self._mainLayout.spacing() -
                                self._mainLayout.contentsMargins().top() -
                                self._mainLayout.contentsMargins().bottom() - 12)
        category.displayOptionsButtonClicked.connect(self.displayOptionsButtonClicked)
        if style == CategoryStyle.Normal:
            self._categories.append(category)
            self._tabBar.addTab(title, color)
            self._stackedWidget.addWidget(category)
        elif style == CategoryStyle.Context:
            category.hide()
        return category

    def addNormalCategory(self, title: str) -> NormalCategory:
        """Add a new category to the ribbon.

        :param title: The title of the category.
        :return: The newly created category.
        """
        return self.addCategory(title, CategoryStyle.Normal)

    def addContextCategory(self, title: str, color: QtGui.QColor = None) -> ContextCategory:
        """Add a new context category to the ribbon.

        :param title: The title of the category.
        :param color: The color of the context category, if None, the default color will be used.
        :return: The newly created category.
        """
        return self.addCategory(title, CategoryStyle.Context, color)

    def showContextCategory(self, category: ContextCategory):
        """Show the given category, if it is not a context category, nothing happens.

        :param category: The category to show.
        """
        self._categories.append(category)
        self._tabBar.addTab(category.title(), category.color())
        self._tabBar.setCurrentIndex(self._tabBar.count() - 1)
        self._stackedWidget.addWidget(category)
        self._stackedWidget.setCurrentIndex(self._tabBar.count() - 1)

    def hideContextCategory(self, category: ContextCategory):
        """Hide the given category, if it is not a context category, nothing happens.

        :param category: The category to hide.
        """
        self._categories.remove(category)
        self._tabBar.removeTab(self._tabBar.indexOf(category.title()))
        self._stackedWidget.removeWidget(category)

    def tabRect(self, category: Category) -> QtCore.QRect:
        """Get the rectangle of the tab of the given category.

        :param category: The category to get the tab rectangle of.
        :return: The rectangle of the tab.
        """
        return self._tabBar.tabRect(self._categories.index(category))

    def removeCategory(self, category: Category):
        """Remove a category from the ribbon.

        :param category: The category to remove.
        """
        index = self._categories.index(category)
        self._tabBar.removeTab(index)
        self._stackedWidget.removeWidget(self._stackedWidget.widget(index))

    def setCurrentCategory(self, category: Category):
        """Set the current category.

        :param category: The category to set.
        """
        index = self._categories.index(category)
        self._tabBar.setCurrentIndex(index)
        self._stackedWidget.setCurrentIndex(index)

    def addQuickAccessButton(self, button: QtWidgets.QToolButton):
        """Add a widget to the quick access bar.

        :param button: The button to add.
        """
        button.setIconSize(QtCore.QSize(self._quickAccessButtonHeight, self._quickAccessButtonHeight))
        self._quickAccessButtons.append(button)
        self._quickAccessToolBarLayout.addWidget(button, 0, QtCore.Qt.AlignBottom)

    def setQuickAccessButtonHeight(self, height: int):
        """Set the height of the quick access buttons.

        :param height: The height to set.
        """
        self._quickAccessButtonHeight = height
        self._applicationButton.setIconSize(QtCore.QSize(height, height))
        for button in self._quickAccessButtons:
            button.setIconSize(QtCore.QSize(height, height))

    def setCollapseButtonIcon(self, icon: QtGui.QIcon):
        """Set the icon of the min button.

        :param icon: The icon to set.
        """
        self._collapseRibbonButton.setIcon(icon)

    def removeCollapseButton(self):
        """Remove the min button from the ribbon."""
        self._collapseRibbonButton.setVisible(False)

    def setHelpButtonIcon(self, icon: QtGui.QIcon):
        """Set the icon of the help button.

        :param icon: The icon to set.
        """
        self._helpButton.setIcon(icon)

    def removeHelpButton(self):
        """Remove the help button from the ribbon."""
        self._helpButton.setVisible(False)

    def addRightToolButton(self, button: QtWidgets.QToolButton):
        """Add a widget to the right button bar.

        :param button: The button to add.
        """
        button.setIconSize(QtCore.QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._rightToolButtons.append(button)
        self._rightToolBar.addWidget(button)

    def setRightButtonHeight(self, height: int):
        """Set the height of the right buttons.

        :param height: The height to set.
        """
        self._rightButtonHeight = height
        for button in self._rightToolButtons:
            button.setIconSize(QtCore.QSize(height, height))

    def setRibbonHeight(self, height: int):
        """Set the total height of the ribbon.

        :param height: The height to set.
        """
        self._ribbonHeight = height
        self.setFixedHeight(height)

    def ribbonHeight(self) -> int:
        """Get the total height of the ribbon.

        :return: The height of the ribbon.
        """
        return self._ribbonHeight

    def setFileIcon(self, icon: QtGui.QIcon):
        """Set the icon of the file menu.

        :param icon: The icon to set.
        """
        self._applicationButton.setIcon(icon)

    def minimumSizeHint(self) -> QtCore.QSize:
        """Return the minimum size hint of the widget.

        :return: The minimum size hint.
        """
        return QtCore.QSize(super().minimumSizeHint().width(), self._ribbonHeight)

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(self.width(), self._ribbonHeight)

    def _collapseButtonClicked(self):
        if self._stackedWidget.isVisible():
            self._collapseRibbonButton.setToolTip("Expand Ribbon")
            self._collapseRibbonButton.setIcon(QtGui.QIcon('icons/expand-arrow.png'))
            self._stackedWidget.setVisible(False)
            self.setFixedSize(self.sizeHint().width(), self._tabsWidget.height())
        else:
            self._collapseRibbonButton.setToolTip("Collapse Ribbon")
            self._collapseRibbonButton.setIcon(QtGui.QIcon('icons/collapse-arrow.png'))
            self._stackedWidget.setVisible(True)
            self.setFixedSize(self.sizeHint())
