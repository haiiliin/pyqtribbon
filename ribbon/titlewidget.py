from PyQt5 import QtWidgets, QtCore, QtGui

from .tabbar import RibbonTabBar
from .utils import package_source_dir


class RibbonApplicationButton(QtWidgets.QToolButton):
    """Application button in the ribbon bar."""
    pass


class RibbonTitleLabel(QtWidgets.QLabel):
    """Title label in the ribbon bar."""
    pass


class RibbonTitleWidget(QtWidgets.QFrame):
    """The title widget of the ribbon."""
    #: Signal: The help button was clicked.
    helpButtonClicked = QtCore.pyqtSignal(bool)
    collapseRibbonButtonClicked = QtCore.pyqtSignal(bool)

    #: Buttons
    _quickAccessButtons = []
    _rightToolButtons = []

    _tabBarHeight = 60
    _quickAccessButtonHeight = 40
    _rightButtonHeight = 24

    def __init__(self, title='PyQtRibbon', parent=None):
        """Initialize the ribbon title widget.

        :param title: The title of the ribbon.
        :param parent: The parent widget.
        """
        super().__init__(parent)
        # Tab bar layout
        self.setFixedHeight(self._tabBarHeight)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self._mainLayout = QtWidgets.QHBoxLayout(self)
        self._mainLayout.setContentsMargins(5, 0, 5, 5)
        self._mainLayout.setSpacing(5)

        # Application
        self._applicationButton = RibbonApplicationButton()
        self._applicationButton.setIcon(QtGui.QIcon('icons/python.png'))
        self._applicationButton.setIconSize(QtCore.QSize(self._quickAccessButtonHeight, self._quickAccessButtonHeight))
        self._applicationButton.setText("PyQtRibbon")
        self._applicationButton.setToolTip("PyQtRibbon")
        self._applicationMenu = QtWidgets.QMenu(self)

        self._quickAccessToolBar = QtWidgets.QToolBar()
        self._quickAccessToolBar.setFixedHeight(self._quickAccessButtonHeight)
        self._quickAccessToolBar.setIconSize(QtCore.QSize(self._quickAccessButtonHeight, self._quickAccessButtonHeight))
        self._quickAccessToolBar.setOrientation(QtCore.Qt.Horizontal)
        self._quickAccessToolBar.setMovable(False)
        self._quickAccessToolBar.addWidget(self._applicationButton)
        self._quickAccessToolBarWidget = QtWidgets.QWidget()
        self._quickAccessToolBarLayout = QtWidgets.QHBoxLayout(self._quickAccessToolBarWidget)
        self._quickAccessToolBarLayout.setContentsMargins(0, 0, 0, 0)
        self._quickAccessToolBarLayout.setSpacing(0)
        self._quickAccessToolBarLayout.addWidget(self._quickAccessToolBar, 0, QtCore.Qt.AlignBottom)

        # right toolbar
        self._rightToolBar = QtWidgets.QToolBar()
        self._rightToolBar.setOrientation(QtCore.Qt.Horizontal)
        self._rightToolBar.setIconSize(QtCore.QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._collapseRibbonButton = QtWidgets.QToolButton(self)
        self._collapseRibbonButton.setIconSize(QtCore.QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._collapseRibbonButton.setIcon(QtGui.QIcon('icons/up.png'))
        self._collapseRibbonButton.setAutoRaise(True)
        self._collapseRibbonButton.setToolTip("Collapse Ribbon")
        self._helpButton = QtWidgets.QToolButton(self)
        self._helpButton.setIconSize(QtCore.QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._helpButton.setIcon(QtGui.QIcon(package_source_dir() + "/icons/help.png"))
        self._helpButton.setAutoRaise(True)
        self._helpButton.setToolTip("Help")
        self._helpButton.clicked.connect(self.helpButtonClicked)
        self.addRightToolButton(self._collapseRibbonButton)
        self.addRightToolButton(self._helpButton)

        # category tab bar
        self._tabBar = RibbonTabBar(self)
        self._tabBar.setExpanding(False)
        self._tabBar.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        font = self._tabBar.font()
        font.setPointSize(font.pointSize() + 3)
        self._tabBar.setFont(font)
        self._tabBar.setShape(QtWidgets.QTabBar.RoundedNorth)
        self._tabBar.setDocumentMode(True)

        # Title label
        self._titleLabel = RibbonTitleLabel(self)
        self._titleLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self._titleLabel.setFixedHeight(self._tabBarHeight -
                                        self._mainLayout.contentsMargins().top() -
                                        self._mainLayout.contentsMargins().bottom())
        self._titleLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self._titleLabel.setText(title)
        font = self._titleLabel.font()
        font.setPointSize(font.pointSize() + 3)
        self._titleLabel.setFont(font)

        self._mainLayout.addWidget(self._quickAccessToolBarWidget, 0, QtCore.Qt.AlignBottom)
        self._mainLayout.addWidget(self._tabBar, 1, QtCore.Qt.AlignBottom)
        self._mainLayout.addWidget(self._titleLabel, 1, QtCore.Qt.AlignBottom)
        self._mainLayout.addWidget(self._rightToolBar, 0, QtCore.Qt.AlignBottom)

        self._collapseRibbonButton.clicked.connect(self.collapseRibbonButtonClicked)

    def applicationButton(self):
        """Return the application button."""
        return self._applicationButton

    def applicationMenu(self) -> QtWidgets.QMenu:
        """Return the application menu.

        :return: The application menu.
        """
        return self._applicationMenu

    def setApplicationIcon(self, icon: QtGui.QIcon):
        """Set the application icon.

        :param icon: The icon to set.
        """
        self._applicationButton.setIcon(icon)

    def addApplicationOptionAction(self, action: QtWidgets.QAction):
        """Add a display option to the category.

        :param action: The action of the display option.
        """
        self._applicationMenu.addAction(action)
        self._applicationButton.setMenu(self._applicationMenu if self._applicationMenu.actions() else None)

    def tabBar(self) -> RibbonTabBar:
        """Return the tab bar of the ribbon.

        :return: The tab bar of the ribbon.
        """
        return self._tabBar

    def tabBarHeight(self) -> int:
        """Get the height of the tab bar.

        :return: The height of the tab bar.
        """
        return self._tabBarHeight

    def setTabBarHeight(self, height: int = 50):
        """Set the height of the tab bar.

        :param height: The height to set.
        """
        self._tabBarHeight = height
        self.setFixedHeight(height)

    def quickAccessToolBar(self) -> QtWidgets.QToolBar:
        """Return the quick access toolbar of the ribbon.

        :return: The quick access toolbar of the ribbon.
        """
        return self._quickAccessToolBar

    def quickAccessButtons(self) -> list[QtWidgets.QToolButton]:
        """Return the quick access buttons of the ribbon.

        :return: The quick access buttons of the ribbon.
        """
        return self._quickAccessButtons

    def addQuickAccessButton(self, button: QtWidgets.QToolButton):
        """Add a widget to the quick access bar.

        :param button: The button to add.
        """
        button.setIconSize(QtCore.QSize(self._quickAccessButtonHeight, self._quickAccessButtonHeight))
        self._quickAccessButtons.append(button)
        self._quickAccessToolBar.addWidget(button)

    def setQuickAccessButtonHeight(self, height: int = 40):
        """Set the height of the quick access buttons.

        :param height: The height to set.
        """
        self._quickAccessButtonHeight = height
        self._applicationButton.setIconSize(QtCore.QSize(height, height))
        for button in self._quickAccessButtons:
            button.setIconSize(QtCore.QSize(height, height))

    def title(self):
        """Return the title of the ribbon.

        :return: The title of the ribbon.
        """
        return self._titleLabel.text()

    def setTitle(self, title: str):
        """Set the title of the ribbon.

        :param title: The title to set.
        """
        self._titleLabel.setText(title)

    def rightToolBar(self) -> QtWidgets.QToolBar:
        """Return the right toolbar of the ribbon.

        :return: The right toolbar of the ribbon.
        """
        return self._rightToolBar

    def addRightToolButton(self, button: QtWidgets.QToolButton):
        """Add a widget to the right button bar.

        :param button: The button to add.
        """
        button.setIconSize(QtCore.QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._rightToolButtons.append(button)
        self._rightToolBar.addWidget(button)

    def setRightToolBarHeight(self, height: int = 24):
        """Set the height of the right buttons.

        :param height: The height to set.
        """
        self._rightButtonHeight = height
        for button in self._rightToolButtons:
            button.setIconSize(QtCore.QSize(height, height))

    def setHelpButtonIcon(self, icon: QtGui.QIcon):
        """Set the icon of the help button.

        :param icon: The icon to set.
        """
        self._helpButton.setIcon(icon)

    def removeHelpButton(self):
        """Remove the help button from the ribbon."""
        self._helpButton.setVisible(False)

    def setCollapseButtonIcon(self, icon: QtGui.QIcon):
        """Set the icon of the min button.

        :param icon: The icon to set.
        """
        self._collapseRibbonButton.setIcon(icon)

    def removeCollapseButton(self):
        """Remove the min button from the ribbon."""
        self._collapseRibbonButton.setVisible(False)

    def collapseRibbonButton(self) -> QtWidgets.QToolButton:
        """Return the collapse ribbon button.

        :return: The collapse ribbon button.
        """
        return self._collapseRibbonButton
    