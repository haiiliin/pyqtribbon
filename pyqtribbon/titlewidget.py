import sys
import typing

from qtpy import QtWidgets, QtCore, QtGui

from .menu import RibbonMenu
from .tabbar import RibbonTabBar
from .utils import data_file_path, startSystemMove


class RibbonApplicationButton(QtWidgets.QToolButton):
    """Application button in the ribbon bar."""

    def addFileMenu(self) -> RibbonMenu:
        """Add a new ribbon menu to the application button.

        :return: The new ribbon menu.
        """
        menu = RibbonMenu(self)
        self.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.setMenu(menu)
        return menu


class RibbonTitleLabel(QtWidgets.QLabel):
    """Title label in the ribbon bar."""
    pass


class TitleBarButton(QtWidgets.QToolButton):
    """ Title bar button """

    def __init__(self, style=None, parent=None):
        """
        Parameters
        ----------
        style: dict
            button style of `normal`,`hover`, and `pressed`. Each state has
            `color`, `background` and `icon`(close button only) attributes.

        parent:
            parent widget
        """
        super().__init__(parent=parent)
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.setFixedSize(46, 32)
        self._state = 'normal'
        self._style = {
            "normal": {
                "color": (0, 0, 0, 255),
                'background': (0, 0, 0, 0)
            },
            "hover": {
                "color": (255, 255, 255),
                'background': (0, 100, 182)
            },
            "pressed": {
                "color": (255, 255, 255),
                'background': (54, 57, 65)
            },
        }
        self.updateStyle(style)
        self.setStyleSheet("""
            QToolButton{
                background-color: transparent;
                border: none;
                margin: 0px;
            }
        """)

    def updateStyle(self, style):
        """ update the style of button

        Parameters
        ----------
        style: dict
            button style of `normal`,`hover`, and `pressed`. Each state has
            `color`, `background` and `icon`(close button only) attributes.
        """
        style = style or {}
        for k, v in style.items():
            self._style[k].update(v)

        self.update()

    def setState(self, state):
        """ set the state of button

        Parameters
        ----------
        state: str
            the state of button, can be `normal`,`hover`, or `pressed`
        """
        if state not in ('normal', 'hover', 'pressed'):
            raise ValueError('The state can only be `normal`,`hover`, or `pressed`')

        self._state = state
        self.update()

    def enterEvent(self, e):
        self.setState("hover")
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.setState("normal")
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() != QtCore.Qt.LeftButton:
            return

        self.setState("pressed")
        super().mousePressEvent(e)


class RibbonMinimizeButton(TitleBarButton):
    """ Minimize button """

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)

        # draw background
        style = self._style[self._state]
        painter.setBrush(QtGui.QColor(*style['background']))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(QtCore.Qt.NoBrush)
        pen = QtGui.QPen(QtGui.QColor(*style['color']), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)


class RibbonMaximizeButton(TitleBarButton):
    """ Maximize button """

    def __init__(self, style=None, parent=None):
        super().__init__(style, parent)
        self.__isMax = False

    def setMaxState(self, isMax):
        """ update the maximized state and icon """
        if self.__isMax == isMax:
            return

        self.__isMax = isMax
        self.setState("normal")

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)

        # draw background
        style = self._style[self._state]
        painter.setBrush(QtGui.QColor(*style['background']))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(QtCore.Qt.NoBrush)
        pen = QtGui.QPen(QtGui.QColor(*style['color']), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)

        r = self.devicePixelRatioF()
        painter.scale(1/r, 1/r)
        if not self.__isMax:
            painter.drawRect(int(18*r), int(11*r), int(10*r), int(10*r))
        else:
            painter.drawRect(int(18*r), int(13*r), int(8*r), int(8*r))
            x0 = int(18*r)+int(2*r)
            y0 = 13*r
            dw = int(2*r)
            path = QtGui.QPainterPath(QtCore.QPointF(x0, y0))
            path.lineTo(x0, y0-dw)
            path.lineTo(x0+8*r, y0-dw)
            path.lineTo(x0+8*r, y0-dw+8*r)
            path.lineTo(x0+8*r-dw, y0-dw+8*r)
            painter.drawPath(path)


class RibbonCloseButton(TitleBarButton):
    """ Close button """

    def __init__(self, style=None, parent=None):
        defaultStyle = {
            "normal": {
                'background': (0, 0, 0, 0),
                "icon": "icons/close_black.svg"
            },
            "hover": {
                'background': (232, 17, 35),
                "icon": "icons/close_white.svg"
            },
            "pressed": {
                'background': (241, 112, 122),
                "icon": "icons/close_white.svg"
            },
        }
        super().__init__(defaultStyle, parent)
        self.updateStyle(style)
        self.setIconSize(QtCore.QSize(46, 32))
        self.setIcon(QtGui.QIcon(self._style['normal']['icon']))

    def updateStyle(self, style):
        super().updateStyle(style)
        self.setIcon(QtGui.QIcon(self._style[self._state]['icon']))

    def enterEvent(self, e):
        self.setIcon(QtGui.QIcon(self._style['hover']['icon']))
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.setIcon(QtGui.QIcon(self._style['normal']['icon']))
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        self.setIcon(QtGui.QIcon(self._style['pressed']['icon']))
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.setIcon(QtGui.QIcon(self._style['normal']['icon']))
        super().mouseReleaseEvent(e)

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # draw background
        style = self._style[self._state]
        painter.setBrush(QtGui.QColor(*style['background']))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        super().paintEvent(e)


class RibbonTitleWidget(QtWidgets.QFrame):
    """The title widget of the ribbon."""
    #: Signal, the help button was clicked.
    helpButtonClicked = QtCore.Signal(bool)
    #: Signal, the collapse button wa clicked.
    collapseRibbonButtonClicked = QtCore.Signal(bool)

    #: Buttons
    _quickAccessButtons = []
    _rightToolButtons = []

    _quickAccessButtonHeight = 30
    _rightButtonHeight = 24

    @typing.overload
    def __init__(self, title='PyQtRibbon', parent=None):
        pass

    @typing.overload
    def __init__(self, parent=None):
        pass

    def __init__(self, *args, **kwargs):
        """Initialize the ribbon title widget.

        :param title: The title of the ribbon.
        :param parent: The parent widget.
        """
        if (args and not isinstance(args[0], QtWidgets.QWidget)) or ('title' in kwargs):
            title = args[0] if len(args) > 0 else kwargs.get('title', 'PyQtRibbon')
            parent = args[1] if len(args) > 1 else kwargs.get('parent', None)
        else:
            title = 'PyQtRibbon'
            parent = args[0] if len(args) > 0 else kwargs.get('parent', None)
        super().__init__(parent)
        # Tab bar layout
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        # main layout
        self._mainLayout = QtWidgets.QVBoxLayout(self)
        self._mainLayout.setContentsMargins(5, 0, 5, 5)
        self._mainLayout.setSpacing(5)
        self._titleLayout = QtWidgets.QHBoxLayout()
        self._titleLayout.setContentsMargins(0, 0, 0, 0)
        self._titleLayout.setSpacing(0)
        self._tabBarLayout = QtWidgets.QHBoxLayout()
        self._tabBarLayout.setContentsMargins(0, 0, 0, 0)
        self._tabBarLayout.setSpacing(0)
        self._mainLayout.addLayout(self._titleLayout)
        self._mainLayout.addLayout(self._tabBarLayout)

        # Application
        self._applicationButton = RibbonApplicationButton()
        self._applicationButton.setIcon(QtGui.QIcon(data_file_path('icons/python.png')))
        self._applicationButton.setIconSize(QtCore.QSize(self._quickAccessButtonHeight, self._quickAccessButtonHeight))
        self._applicationButton.setText("PyQtRibbon")
        self._applicationButton.setToolTip("PyQtRibbon")

        self._quickAccessToolBar = QtWidgets.QToolBar()
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
        self._collapseRibbonButton.setIcon(QtGui.QIcon(data_file_path('icons/up.png')))
        self._collapseRibbonButton.setAutoRaise(True)
        self._collapseRibbonButton.setToolTip("Collapse Ribbon")
        self._collapseRibbonButton.clicked.connect(self.collapseRibbonButtonClicked)
        self._helpButton = QtWidgets.QToolButton(self)
        self._helpButton.setIconSize(QtCore.QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._helpButton.setIcon(QtGui.QIcon(data_file_path("icons/help.png")))
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
        self._tabBar.addTab("File")

        # Title label
        self._titleLabel = RibbonTitleLabel(self)
        self._titleLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self._titleLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self._titleLabel.setText(title)
        font = self._titleLabel.font()
        font.setPointSize(font.pointSize() + 3)
        self._titleLabel.setFont(font)

        # Title bar
        self._minButton = RibbonMinimizeButton()
        self._maxButton = RibbonMaximizeButton()
        self._closeButton = RibbonCloseButton()
        self._minMaxButtonsLayout = QtWidgets.QHBoxLayout()
        self._minMaxButtonsLayout.setContentsMargins(0, 0, 0, 0)
        self._minMaxButtonsLayout.setSpacing(0)
        self._minMaxButtonsLayout.addWidget(self._minButton)
        self._minMaxButtonsLayout.addWidget(self._maxButton)
        self._minMaxButtonsLayout.addWidget(self._closeButton)

        # connect signal to slot
        self._minButton.clicked.connect(self.window().showMinimized)
        self._maxButton.clicked.connect(self.__toggleMaxState)
        self._closeButton.clicked.connect(self.window().close)

        self._titleLayout.addWidget(self._quickAccessToolBarWidget, 0)
        self._titleLayout.addWidget(self._titleLabel, 1)
        self._titleLayout.addLayout(self._minMaxButtonsLayout, 0)
        self._tabBarLayout.addWidget(self._tabBar, 1)
        self._tabBarLayout.addWidget(self._rightToolBar, 0)

        self.window().installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.window():
            if e.type() == QtCore.QEvent.WindowStateChange:
                self.maxBtn.setMaxState(self.window().isMaximized())
                return False

        return super().eventFilter(obj, e)

    def mouseDoubleClickEvent(self, event):
        """ Toggles the maximization state of the window """
        if event.button() != QtCore.Qt.LeftButton:
            return

        self.__toggleMaxState()

    def mouseMoveEvent(self, e):
        if sys.platform != "win32" or not self._isDragRegion(e.pos()):
            return

        startSystemMove(self.window(), e.globalPos())

    def mousePressEvent(self, e):
        if sys.platform == "win32" or e.button() != QtCore.Qt.LeftButton or not self._isDragRegion(e.pos()):
            return

        startSystemMove(self.window(), e.globalPos())

    def __toggleMaxState(self):
        """ Toggles the maximization state of the window and change icon """
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def _isDragRegion(self, pos):
        """ Check whether the pressed point belongs to the area where dragging is allowed """
        return 0 < pos.x() < self.width() - 46 * 3

    def applicationButton(self) -> RibbonApplicationButton:
        """Return the application button."""
        return self._applicationButton

    def setApplicationIcon(self, icon: QtGui.QIcon):
        """Set the application icon.

        :param icon: The icon to set.
        """
        self._applicationButton.setIcon(icon)

    def addTitleWidget(self, widget: QtWidgets.QWidget):
        """Add a widget to the title layout.

        :param widget: The widget to add.
        """
        self._titleLayout.addWidget(widget)

    def insertTitleWidget(self, index: int, widget: QtWidgets.QWidget):
        """Insert a widget to the title layout.

        :param index: The index to insert the widget.
        :param widget: The widget to insert.
        """
        self._titleLayout.insertWidget(index, widget)

    def removeTitleWidget(self, widget: QtWidgets.QWidget):
        """Remove a widget from the title layout.

        :param widget: The widget to remove.
        """
        self._titleLayout.removeWidget(widget)

    def tabBar(self) -> RibbonTabBar:
        """Return the tab bar of the ribbon.

        :return: The tab bar of the ribbon.
        """
        return self._tabBar

    def quickAccessToolBar(self) -> QtWidgets.QToolBar:
        """Return the quick access toolbar of the ribbon.

        :return: The quick access toolbar of the ribbon.
        """
        return self._quickAccessToolBar

    def quickAccessButtons(self) -> typing.List[QtWidgets.QToolButton]:
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

    def setQuickAccessButtonHeight(self, height: int = 30):
        """Set the height of the quick access buttons.

        :param height: The height to set.
        """
        self._quickAccessButtonHeight = height
        self._applicationButton.setIconSize(QtCore.QSize(height, height))
        for button in self._quickAccessButtons:
            button.setIconSize(QtCore.QSize(height, height))

    def title(self) -> str:
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
            
    def helpRibbonButton(self) -> QtWidgets.QToolButton:
        """Return the help ribbon button.

        :return: The help ribbon button.
        """
        return self._helpButton

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
    