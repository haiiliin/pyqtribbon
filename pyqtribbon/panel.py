import typing
from enum import IntEnum

import numpy as np
from qtpy import QtWidgets, QtGui, QtCore

from .gallery import RibbonGallery
from .separator import RibbonHorizontalSeparator, RibbonVerticalSeparator
from .toolbutton import RibbonToolButton, RibbonButtonStyle, Large, Small, Medium
from .utils import DataFile


class RibbonPanelTitle(QtWidgets.QLabel):
    """Widget to display the title of a panel."""

    pass


class RibbonSpaceFindMode(IntEnum):
    """Mode to find available space in a grid layout, ColumnWise or RowWise."""

    ColumnWise = 0
    RowWise = 1


ColumnWise = RibbonSpaceFindMode.ColumnWise
RowWise = RibbonSpaceFindMode.RowWise


class RibbonGridLayoutManager(object):
    """Grid Layout Manager."""

    def __init__(self, rows: int):
        """Create a new grid layout manager.

        :param rows: The number of rows in the grid layout.
        """
        self.rows = rows
        self.cells = np.ones((rows, 1), dtype=bool)

    def request_cells(self, rowSpan: int = 1, colSpan: int = 1, mode=RibbonSpaceFindMode.ColumnWise):
        """Request a number of available cells from the grid.

        :param rowSpan: The number of rows the cell should span.
        :param colSpan: The number of columns the cell should span.
        :param mode: The mode of the grid.
        :return: row, col, the row and column of the requested cell.
        """
        if rowSpan > self.rows:
            raise ValueError("RowSpan is too large")
        if mode == RibbonSpaceFindMode.ColumnWise:
            for row in range(self.cells.shape[0] - rowSpan + 1):
                for col in range(self.cells.shape[1] - colSpan + 1):
                    if self.cells[row : row + rowSpan, col : col + colSpan].all():
                        self.cells[row : row + rowSpan, col : col + colSpan] = False
                        return row, col
        else:
            for col in range(self.cells.shape[1]):
                if self.cells[0, col:].all():
                    if self.cells.shape[1] - col < colSpan:
                        self.cells = np.append(
                            self.cells, np.ones((self.rows, colSpan - (self.cells.shape[1] - col)), dtype=bool), axis=1
                        )
                    self.cells[0, col:] = False
                    return 0, col
        cols = self.cells.shape[1]
        colSpan1 = colSpan
        if self.cells[:, -1].all():
            cols -= 1
            colSpan1 -= 1
        self.cells = np.append(self.cells, np.ones((self.rows, colSpan1), dtype=bool), axis=1)
        self.cells[:rowSpan, cols : cols + colSpan] = False
        return 0, cols


class RibbonPanelItemWidget(QtWidgets.QFrame):
    """Widget to display a panel item."""

    def __init__(self, parent=None):
        """Create a new panel item.

        :param parent: The parent widget.
        """
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.layout().setAlignment(QtCore.Qt.AlignCenter)
        self.layout().setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)  # type: ignore

    def addWidget(self, widget):
        """Add a widget to the panel item.

        :param widget: The widget to add.
        """
        self.layout().addWidget(widget)


class RibbonPanelOptionButton(QtWidgets.QToolButton):
    """Button to display the options of a panel."""

    pass


class RibbonPanel(QtWidgets.QFrame):
    """Panel in the ribbon category."""

    #: maximal number of rows
    _maxRows: int = 6
    #: rows for large widgets
    _largeRows: int = 6
    #: rows for medium widgets
    _mediumRows: int = 3
    #: rows for small widgets
    _smallRows: int = 2
    #: GridLayout manager to request available cells.
    _gridLayoutManager: RibbonGridLayoutManager
    #: whether to show the panel option button
    _showPanelOptionButton: bool

    #: widgets that are added to the panel
    _widgets: typing.List[QtWidgets.QWidget] = []

    # height of the title widget
    _titleHeight: int = 20

    # Panel options signal
    panelOptionClicked = QtCore.Signal(bool)

    @typing.overload
    def __init__(self, title: str = "", maxRows: int = 6, showPanelOptionButton=True, parent=None):
        pass

    @typing.overload
    def __init__(self, parent=None):
        pass

    def __init__(self, *args, **kwargs):
        """Create a new panel.

        :param title: The title of the panel.
        :param maxRows: The maximal number of rows in the panel.
        :param showPanelOptionButton: Whether to show the panel option button.
        :param parent: The parent widget.
        """
        if (args and not isinstance(args[0], QtWidgets.QWidget)) or ("title" in kwargs or "maxRows" in kwargs):
            title = args[0] if len(args) > 0 else kwargs.get("title", "")
            maxRows = args[1] if len(args) > 1 else kwargs.get("maxRows", 6)
            showPanelOptionButton = args[2] if len(args) > 2 else kwargs.get("showPanelOptionButton", True)
            parent = args[3] if len(args) > 3 else kwargs.get("parent", None)
        else:
            title = ""
            maxRows = 6
            showPanelOptionButton = True
            parent = args[0] if len(args) > 0 else kwargs.get("parent", None)
        super().__init__(parent)
        self._maxRows = maxRows
        self._largeRows = maxRows
        self._mediumRows = max(round(maxRows / 2), 1)
        self._smallRows = max(round(maxRows / 3), 1)
        self._gridLayoutManager = RibbonGridLayoutManager(self._maxRows)
        self._widgets = []
        self._showPanelOptionButton = showPanelOptionButton

        # Main layout
        self._mainLayout = QtWidgets.QVBoxLayout(self)
        self._mainLayout.setContentsMargins(5, 2, 5, 2)
        self._mainLayout.setSpacing(5)

        # Actions layout
        self._actionsLayout = QtWidgets.QGridLayout()
        self._actionsLayout.setContentsMargins(5, 0, 5, 0)
        self._actionsLayout.setSpacing(0)
        self._mainLayout.addLayout(self._actionsLayout, 1)

        # Title layout
        self._titleWidget = QtWidgets.QWidget()
        self._titleWidget.setFixedHeight(self._titleHeight)
        self._titleLayout = QtWidgets.QHBoxLayout(self._titleWidget)
        self._titleLayout.setContentsMargins(0, 0, 0, 0)
        self._titleLayout.setSpacing(5)
        self._titleLabel = RibbonPanelTitle()  # type: ignore
        self._titleLabel.setText(title)
        self._titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self._titleLayout.addWidget(self._titleLabel, 1)

        # Panel option button
        if showPanelOptionButton:
            self._panelOption = RibbonPanelOptionButton()  # type: ignore
            self._panelOption.setAutoRaise(True)
            self._panelOption.setIcon(QtGui.QIcon(DataFile("icons/linking.png")))
            self._panelOption.setIconSize(QtCore.QSize(16, 16))
            self._panelOption.setToolTip("Panel options")
            self._panelOption.clicked.connect(self.panelOptionClicked)  # type: ignore
            self._titleLayout.addWidget(self._panelOption, 0)

        self._mainLayout.addWidget(self._titleWidget, 0)

    def maximumRows(self) -> int:
        """Return the maximal number of rows in the panel.

        :return: The maximal number of rows in the panel.
        """
        return self._maxRows

    def largeRows(self) -> int:
        """Return the number of span rows for large widgets.

        :return: The number of span rows for large widgets.
        """
        return self._largeRows

    def mediumRows(self) -> int:
        """Return the number of span rows for medium widgets.

        :return: The number of span rows for medium widgets.
        """
        return self._mediumRows

    def smallRows(self) -> int:
        """Return the number of span rows for small widgets.

        :return: The number of span rows for small widgets.
        """
        return self._smallRows

    def setMaximumRows(self, maxRows: int):
        """Set the maximal number of rows in the panel.

        :param maxRows: The maximal number of rows in the panel.
        """
        self._maxRows = maxRows
        self._largeRows = maxRows
        self._mediumRows = max(round(maxRows / 2), 1)
        self._smallRows = max(round(maxRows / 3), 1)

    def setLargeRows(self, rows: int):
        """Set the number of span rows for large widgets.

        :param rows: The number of span rows for large widgets.
        """
        if not (0 < rows <= self._maxRows):
            raise ValueError("Invalid number of rows")
        self._largeRows = rows

    def setMediumRows(self, rows: int):
        """Set the number of span rows for medium widgets.

        :param rows: The number of span rows for medium widgets.
        """
        if not (0 < rows <= self._maxRows):
            raise ValueError("Invalid number of rows")
        self._mediumRows = rows

    def setSmallRows(self, rows: int):
        """Set the number of span rows for small widgets.

        :param rows: The number of span rows for small widgets.
        """
        if not (0 < rows <= self._maxRows):
            raise ValueError("Invalid number of rows")
        self._smallRows = rows

    def defaultRowSpan(self, rowSpan: typing.Union[int, RibbonButtonStyle]):
        """Return the number of span rows for the given widget type.

        :param rowSpan: row span or type.
        :return: The number of span rows for the given widget type.
        """
        if not isinstance(rowSpan, RibbonButtonStyle):
            return rowSpan
        if rowSpan == Large:
            return self._largeRows
        elif rowSpan == Medium:
            return self._mediumRows
        elif rowSpan == Small:
            return self._smallRows
        else:
            raise ValueError("Invalid row span")

    def panelOptionButton(self) -> RibbonPanelOptionButton:
        """Return the panel option button.

        :return: The panel option button.
        """
        return self._panelOption

    def setPanelOptionToolTip(self, text: str):
        """Set the tooltip of the panel option button.

        :param text: The tooltip text.
        """
        self._panelOption.setToolTip(text)

    def rowHeight(self) -> int:
        """Return the height of a row."""
        return int(
            (
                self.size().height()
                - self._mainLayout.contentsMargins().top()
                - self._mainLayout.contentsMargins().bottom()
                - self._mainLayout.spacing()
                - self._titleWidget.height()
                - self._actionsLayout.contentsMargins().top()
                - self._actionsLayout.contentsMargins().bottom()
                - self._actionsLayout.verticalSpacing() * (self._gridLayoutManager.rows - 1)
            )
            / self._gridLayoutManager.rows
        )

    def addWidgetsBy(
        self,
        data: typing.Dict[
            str,  # type of the widget
            typing.Dict,  # data of the widget
        ],
    ) -> typing.Dict[str, QtWidgets.QWidget]:
        """Add widgets to the panel.

        :param data: The data to add. The dict is of the form:

            .. code-block:: python

                {
                    "widget-name": {
                        "type": "Button",
                        "arguments": {
                            "key1": "value1",
                            "key2": "value2"
                        }
                    },
                }

            Possible types are: Button, SmallButton, MediumButton, LargeButton,
            ToggleButton, SmallToggleButton, MediumToggleButton, LargeToggleButton, ComboBox, FontComboBox,
            LineEdit, TextEdit, PlainTextEdit, Label, ProgressBar, SpinBox, DoubleSpinBox, DataEdit, TimeEdit,
            DateTimeEdit, TableWidget, TreeWidget, ListWidget, CalendarWidget, Separator, HorizontalSeparator,
            VerticalSeparator, Gallery.
        :return: A dictionary of the added widgets.
        """
        widgets = {}  # type: typing.Dict[str, QtWidgets.QWidget]
        for key, widget_data in data.items():
            type = widget_data.pop("type", "").capitalize()
            if hasattr(self, "add" + type):
                method = getattr(self, "add" + type)  # type: typing.Callable
                if method is not None:
                    widgets[key] = method(**widget_data.get("arguments", {}))
        return widgets

    def addWidget(
        self,
        widget: QtWidgets.QWidget,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ):
        """Add a widget to the panel.

        :param widget: The widget to add.
        :param rowSpan: The number of rows the widget should span, 2: small, 3: medium, 6: large.
        :param colSpan: The number of columns the widget should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the widget.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        self._widgets.append(widget)
        row, col = self._gridLayoutManager.request_cells(rowSpan, colSpan, mode)
        maximumHeight = self.rowHeight() * rowSpan + self._actionsLayout.verticalSpacing() * (rowSpan - 2)
        widget.setMaximumHeight(maximumHeight)
        if fixedHeight is True or fixedHeight > 0:
            fixedHeight = (
                int(fixedHeight * maximumHeight)
                if 0 < fixedHeight <= 1
                else fixedHeight
                if 1 < fixedHeight < maximumHeight
                else maximumHeight
            )
            fixedHeight = max(fixedHeight, 0.4 * maximumHeight)  # minimum height is 40% of the maximum height
            widget.setFixedHeight(fixedHeight)
        item = RibbonPanelItemWidget(self)
        item.addWidget(widget)
        self._actionsLayout.addWidget(item, row, col, rowSpan, colSpan, alignment)  # type: ignore

    def addSmallWidget(
        self,
        widget: QtWidgets.QWidget,
        *,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ):
        """Add a small widget to the panel.

        :param widget: The widget to add.
        :param colSpan: The number of columns the widget should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the widget.
        :return: The widget that was added.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.
        """
        return self.addWidget(
            widget, rowSpan=self.smallRows(), colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )

    def addMediumWidget(
        self,
        widget: QtWidgets.QWidget,
        *,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ):
        """Add a medium widget to the panel.

        :param widget: The widget to add.
        :param colSpan: The number of columns the widget should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the widget.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.
        """
        return self.addWidget(
            widget, rowSpan=self.mediumRows(), colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )

    def addLargeWidget(
        self,
        widget: QtWidgets.QWidget,
        *,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ):
        """Add a large widget to the panel.

        :param widget: The widget to add.
        :param colSpan: The number of columns the widget should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the widget.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.
        """
        return self.addWidget(
            widget, rowSpan=self.largeRows(), colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )

    def removeWidget(self, widget: QtWidgets.QWidget):
        """Remove a widget from the panel."""
        self._actionsLayout.removeWidget(widget)

    def widget(self, index: int) -> QtWidgets.QWidget:
        """Get the widget at the given index.

        :param index: The index of the widget, starting from 0.
        :return: The widget at the given index.
        """
        return self._widgets[index]

    def widgets(self) -> typing.List[QtWidgets.QWidget]:
        """Get all the widgets in the panel.

        :return: A list of all the widgets in the panel.
        """
        return self._widgets

    def addButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        style: RibbonButtonStyle = RibbonButtonStyle.Large,
        showText: bool = True,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        *,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> RibbonToolButton:
        """Add a button to the panel.

        :param text: The text of the button.
        :param icon: The icon of the button.
        :param style: The style of the button.
        :param showText: Whether to show the text of the button.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param colSpan: The number of columns the button should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the button.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The button that was added.
        """
        button = RibbonToolButton(self)
        button.setButtonStyle(style)
        if text:
            button.setText(text)
        if icon:
            button.setIcon(icon)
        if slot:
            button.clicked.connect(slot)  # type: ignore
        if shortcut:
            button.setShortcut(shortcut)
        if tooltip:
            button.setToolTip(tooltip)
        if statusTip:
            button.setStatusTip(statusTip)
        maximumHeight = (
            self.height()
            - self._titleLabel.sizeHint().height()
            - self._mainLayout.spacing()
            - self._mainLayout.contentsMargins().top()
            - self._mainLayout.contentsMargins().bottom()
        )
        button.setMaximumHeight(maximumHeight)
        if style == RibbonButtonStyle.Large:
            fontSize = max(button.font().pointSize() * 4 / 3, button.font().pixelSize())
            arrowSize = fontSize
            maximumIconSize = max(maximumHeight - fontSize * 2 - arrowSize, 48)
            button.setMaximumIconSize(int(maximumIconSize))
        if not showText:
            button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.addWidget(
            button,
            rowSpan=(
                self.defaultRowSpan(Small)
                if style == Small
                else self.defaultRowSpan(Medium)
                if style == Medium
                else self.defaultRowSpan(Large)
            ),
            colSpan=colSpan,
            mode=mode,
            alignment=alignment,
            fixedHeight=fixedHeight,
        )
        return button

    def addSmallButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        *,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> RibbonToolButton:
        """Add a small button to the panel.

        :param text: The text of the button.
        :param icon: The icon of the button.
        :param showText: Whether to show the text of the button.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param colSpan: The number of columns the button should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the button.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The button that was added.
        """
        return self.addButton(
            text,
            icon,
            RibbonButtonStyle.Small,
            showText,
            slot,
            shortcut,
            tooltip,
            statusTip,
            colSpan=colSpan,
            mode=mode,
            alignment=alignment,
            fixedHeight=fixedHeight,
        )

    def addMediumButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        *,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> RibbonToolButton:
        """Add a medium button to the panel.

        :param text: The text of the button.
        :param icon: The icon of the button.
        :param showText: Whether to show the text of the button.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param colSpan: The number of columns the button should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the button.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The button that was added.
        """
        return self.addButton(
            text,
            icon,
            RibbonButtonStyle.Medium,
            showText,
            slot,
            shortcut,
            tooltip,
            statusTip,
            colSpan=colSpan,
            mode=mode,
            alignment=alignment,
            fixedHeight=fixedHeight,
        )

    def addLargeButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        *,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> RibbonToolButton:
        """Add a large button to the panel.

        :param text: The text of the button.
        :param icon: The icon of the button.
        :param showText: Whether to show the text of the button.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param colSpan: The number of columns the button should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the button.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The button that was added.
        """
        return self.addButton(
            text,
            icon,
            RibbonButtonStyle.Large,
            showText,
            slot,
            shortcut,
            tooltip,
            statusTip,
            colSpan=colSpan,
            mode=mode,
            alignment=alignment,
            fixedHeight=fixedHeight,
        )

    def addToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        style: RibbonButtonStyle = RibbonButtonStyle.Large,
        showText: bool = True,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        *,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> RibbonToolButton:
        """Add a toggle button to the panel.

        :param text: The text of the button.
        :param icon: The icon of the button.
        :param style: The style of the button.
        :param showText: Whether to show the text of the button.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param colSpan: The number of columns the button should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the button.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The button that was added.
        """
        button = self.addButton(
            text,
            icon,
            style,
            showText,
            slot,
            shortcut,
            tooltip,
            statusTip,
            colSpan=colSpan,
            mode=mode,
            alignment=alignment,
            fixedHeight=fixedHeight,
        )
        button.setCheckable(True)
        return button

    def addSmallToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        *,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> RibbonToolButton:
        """Add a small toggle button to the panel.

        :param text: The text of the button.
        :param icon: The icon of the button.
        :param showText: Whether to show the text of the button.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param colSpan: The number of columns the button should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the button.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The button that was added.
        """
        return self.addToggleButton(
            text,
            icon,
            RibbonButtonStyle.Small,
            showText,
            slot,
            shortcut,
            tooltip,
            statusTip,
            colSpan=colSpan,
            mode=mode,
            alignment=alignment,
            fixedHeight=fixedHeight,
        )

    def addMediumToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        *,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> RibbonToolButton:
        """Add a medium toggle button to the panel.

        :param text: The text of the button.
        :param icon: The icon of the button.
        :param showText: Whether to show the text of the button.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param colSpan: The number of columns the button should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the button.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The button that was added.
        """
        return self.addToggleButton(
            text,
            icon,
            RibbonButtonStyle.Medium,
            showText,
            slot,
            shortcut,
            tooltip,
            statusTip,
            colSpan=colSpan,
            mode=mode,
            alignment=alignment,
            fixedHeight=fixedHeight,
        )

    def addLargeToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        *,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> RibbonToolButton:
        """Add a large toggle button to the panel.

        :param text: The text of the button.
        :param icon: The icon of the button.
        :param showText: Whether to show the text of the button.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param colSpan: The number of columns the button should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the button.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The button that was added.
        """
        return self.addToggleButton(
            text,
            icon,
            RibbonButtonStyle.Large,
            showText,
            slot,
            shortcut,
            tooltip,
            statusTip,
            colSpan=colSpan,
            mode=mode,
            alignment=alignment,
            fixedHeight=fixedHeight,
        )

    def addComboBox(
        self,
        items: typing.List[str],
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QComboBox:
        """Add a combo box to the panel.

        :param items: The items of the combo box.
        :param rowSpan: The number of rows the combo box should span.
        :param colSpan: The number of columns the combo box should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the combo box.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The combo box that was added.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        comboBox = QtWidgets.QComboBox(self)
        comboBox.addItems(items)
        self.addWidget(
            comboBox, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return comboBox

    def addFontComboBox(
        self,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QFontComboBox:
        """Add a font combo box to the panel.

        :param rowSpan: The number of rows the combo box should span.
        :param colSpan: The number of columns the combo box should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the combo box.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.
        :return: The combo box that was added.
        """
        comboBox = QtWidgets.QFontComboBox(self)
        self.addWidget(
            comboBox, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return comboBox

    def addLineEdit(
        self,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QLineEdit:
        """Add a line edit to the panel.

        :param rowSpan: The number of rows the line edit should span.
        :param colSpan: The number of columns the line edit should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the line edit.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The line edit that was added.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        lineEdit = QtWidgets.QLineEdit(self)
        self.addWidget(
            lineEdit, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return lineEdit

    def addTextEdit(
        self,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QTextEdit:
        """Add a text edit to the panel.

        :param rowSpan: The number of rows the text edit should span.
        :param colSpan: The number of columns the text edit should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the text edit.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The text edit that was added.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        textEdit = QtWidgets.QTextEdit(self)
        self.addWidget(
            textEdit, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return textEdit

    def addPlainTextEdit(
        self,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QPlainTextEdit:
        """Add a plain text edit to the panel.

        :param rowSpan: The number of rows the text edit should span.
        :param colSpan: The number of columns the text edit should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the text edit.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The text edit that was added.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        textEdit = QtWidgets.QPlainTextEdit(self)
        self.addWidget(
            textEdit, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return textEdit

    def addLabel(
        self,
        text: str,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QLabel:
        """Add a label to the panel.

        :param text: The text of the label.
        :param rowSpan: The number of rows the label should span.
        :param colSpan: The number of columns the label should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the label.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The label that was added.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        label = QtWidgets.QLabel(self)
        label.setText(text)
        self.addWidget(label, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight)
        return label

    def addProgressBar(
        self,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QProgressBar:
        """Add a progress bar to the panel.

        :param rowSpan: The number of rows the progress bar should span.
        :param colSpan: The number of columns the progress bar should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the progress bar.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The progress bar that was added.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        progressBar = QtWidgets.QProgressBar(self)
        self.addWidget(
            progressBar, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return progressBar

    def addSlider(
        self,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QSlider:
        """Add a slider to the panel.

        :param rowSpan: The number of rows the slider should span.
        :param colSpan: The number of columns the slider should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the slider.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The slider that was added.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        slider = QtWidgets.QSlider(self)
        slider.setOrientation(QtCore.Qt.Horizontal)
        self.addWidget(
            slider, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return slider

    def addSpinBox(
        self,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QSpinBox:
        """Add a spin box to the panel.

        :param rowSpan: The number of rows the spin box should span.
        :param colSpan: The number of columns the spin box should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the spin box.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The spin box that was added.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        spinBox = QtWidgets.QSpinBox(self)
        self.addWidget(
            spinBox, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return spinBox

    def addDoubleSpinBox(
        self,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QDoubleSpinBox:
        """Add a double spin box to the panel.

        :param rowSpan: The number of rows the double spin box should span.
        :param colSpan: The number of columns the double spin box should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the double spin box.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The double spin box that was added.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        doubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.addWidget(
            doubleSpinBox, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return doubleSpinBox

    def addDateEdit(
        self,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QDateEdit:
        """Add a date edit to the panel.

        :param rowSpan: The number of rows the date edit should span.
        :param colSpan: The number of columns the date edit should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the date edit.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The date edit that was added.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        dateEdit = QtWidgets.QDateEdit(self)
        self.addWidget(
            dateEdit, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return dateEdit

    def addTimeEdit(
        self,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QTimeEdit:
        """Add a time edit to the panel.

        :param rowSpan: The number of rows the time edit should span.
        :param colSpan: The number of columns the time edit should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the time edit.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The time edit that was added.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        timeEdit = QtWidgets.QTimeEdit(self)
        self.addWidget(
            timeEdit, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return timeEdit

    def addDateTimeEdit(
        self,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QDateTimeEdit:
        """Add a date time edit to the panel.

        :param rowSpan: The number of rows the date time edit should span.
        :param colSpan: The number of columns the date time edit should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the date time edit.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The date time edit that was added.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        dateTimeEdit = QtWidgets.QDateTimeEdit(self)
        self.addWidget(
            dateTimeEdit, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return dateTimeEdit

    def addTableWidget(
        self,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QTableWidget:
        """Add a table widget to the panel.

        :param rowSpan: The number of rows the table widget should span.
        :param colSpan: The number of columns the table widget should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the table widget.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The table widget that was added.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        tableWidget = QtWidgets.QTableWidget(self)
        self.addWidget(
            tableWidget, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return tableWidget

    def addTreeWidget(
        self,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QTreeWidget:
        """Add a tree widget to the panel.

        :param rowSpan: The number of rows the tree widget should span.
        :param colSpan: The number of columns the tree widget should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the tree widget.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The tree widget that was added.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        treeWidget = QtWidgets.QTreeWidget(self)
        self.addWidget(
            treeWidget, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return treeWidget

    def addListWidget(
        self,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QListWidget:
        """Add a list widget to the panel.

        :param rowSpan: The number of rows the list widget should span.
        :param colSpan: The number of columns the list widget should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the list widget.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The list widget that was added.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        listWidget = QtWidgets.QListWidget(self)
        self.addWidget(
            listWidget, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return listWidget

    def addCalendarWidget(
        self,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> QtWidgets.QCalendarWidget:
        """Add a calendar widget to the panel.

        :param rowSpan: The number of rows the calendar widget should span.
        :param colSpan: The number of columns the calendar widget should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the calendar widget.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The calendar widget that was added.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        calendarWidget = QtWidgets.QCalendarWidget(self)
        self.addWidget(
            calendarWidget, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return calendarWidget

    def addSeparator(
        self,
        orientation=QtCore.Qt.Vertical,
        width=6,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> typing.Union[RibbonHorizontalSeparator, RibbonVerticalSeparator]:
        """Add a separator to the panel.

        :param orientation: The orientation of the separator.
        :param width: The width of the separator.
        :param rowSpan: The number of rows the separator spans.
        :param colSpan: The number of columns the separator spans.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the separator.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The separator.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        separator = (
            RibbonHorizontalSeparator(width) if orientation == QtCore.Qt.Horizontal else RibbonVerticalSeparator(width)
        )
        self.addWidget(
            separator, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return separator

    def addHorizontalSeparator(
        self,
        width=6,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 2,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> RibbonHorizontalSeparator:
        """Add a horizontal separator to the panel.

        :param width: The width of the separator.
        :param rowSpan: The number of rows the separator spans.
        :param colSpan: The number of columns the separator spans.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the separator.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The separator.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        return self.addSeparator(
            QtCore.Qt.Horizontal,
            width,
            rowSpan=rowSpan,
            colSpan=colSpan,
            mode=mode,
            alignment=alignment,
            fixedHeight=fixedHeight,
        )

    def addVerticalSeparator(
        self,
        width=6,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> RibbonVerticalSeparator:
        """Add a vertical separator to the panel.

        :param width: The width of the separator.
        :param rowSpan: The number of rows the separator spans.
        :param colSpan: The number of columns the separator spans.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the separator.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The separator.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        return self.addSeparator(
            QtCore.Qt.Vertical,
            width,
            rowSpan=rowSpan,
            colSpan=colSpan,
            mode=mode,
            alignment=alignment,
            fixedHeight=fixedHeight,
        )

    def addGallery(
        self,
        minimumWidth=800,
        popupHideOnClick=False,
        *,
        rowSpan: typing.Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=RibbonSpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: typing.Union[bool, float] = False,
    ) -> RibbonGallery:
        """Add a gallery to the panel.

        :param minimumWidth: The minimum width of the gallery.
        :param popupHideOnClick: Whether the gallery popup should be hidden when a user clicks on it.
        :param rowSpan: The number of rows the gallery spans.
        :param colSpan: The number of columns the gallery spans.
        :param mode: The mode of the gallery.
        :param alignment: The alignment of the gallery.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.

        :return: The gallery.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        gallery = RibbonGallery(minimumWidth, popupHideOnClick, self)
        maximumHeight = self.rowHeight() * rowSpan + self._actionsLayout.verticalSpacing() * (rowSpan - 2)
        gallery.setFixedHeight(maximumHeight)
        self.addWidget(
            gallery, rowSpan=rowSpan, colSpan=colSpan, mode=mode, alignment=alignment, fixedHeight=fixedHeight
        )
        return gallery

    def setTitle(self, title: str):
        """Set the title of the panel.

        :param title: The title to set.
        """
        self._titleLabel.setText(title)

    def title(self):
        """Get the title of the panel.

        :return: The title.
        """
        return self._titleLabel.text()
