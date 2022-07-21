import typing
from enum import IntEnum

import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore

from .toolbutton import RibbonToolButton, ButtonStyle
from .separator import RibbonHorizontalSeparator, RibbonVerticalSeparator


class RibbonPanelTitle(QtWidgets.QLabel):
    pass


class SpaceFindMode(IntEnum):
    """
    SpaceFindMode
    """
    ColumnWise = 0
    RowWise = 1


class GridLayoutManager(object):

    def __init__(self, rows: int):
        self.rows = rows
        self.cells = np.ones((rows, 1), dtype=bool)

    def request_cells(self, rowSpan: int = 1, colSpan: int = 1, mode=SpaceFindMode.ColumnWise):
        """Request a number of available cells from the grid.

        :param rowSpan: The number of rows the cell should span.
        :param colSpan: The number of columns the cell should span.
        :param mode: The mode of the grid.
        :return: row, col, the row and column of the requested cell.
        """
        if rowSpan > self.rows:
            raise ValueError("RowSpan is too large")
        if mode == SpaceFindMode.ColumnWise:
            for row in range(self.cells.shape[0] - rowSpan + 1):
                for col in range(self.cells.shape[1] - colSpan + 1):
                    if self.cells[row: row + rowSpan, col: col + colSpan].all():
                        self.cells[row: row + rowSpan, col: col + colSpan] = False
                        return row, col
        else:
            for col in range(self.cells.shape[1]):
                if self.cells[0, col:].all():
                    if self.cells.shape[1] - col < colSpan:
                        self.cells = np.append(
                            self.cells, np.ones((self.rows, colSpan - (self.cells.shape[1] - col)),
                                                dtype=bool),
                            axis=1)
                    self.cells[0, col:] = False
                    return 0, col
        cols = self.cells.shape[1]
        colSpan1 = colSpan
        if self.cells[:, -1].all():
            cols -= 1
            colSpan1 -= 1
        self.cells = np.append(
            self.cells, np.ones((self.rows, colSpan1), dtype=bool), axis=1
        )
        self.cells[:rowSpan, cols: cols + colSpan] = False
        return 0, cols


class RibbonPanelItemWidget(QtWidgets.QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.layout().setAlignment(QtCore.Qt.AlignCenter)
        self.layout().setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def addWidget(self, widget):
        self.layout().addWidget(widget)


class RibbonPanel(QtWidgets.QFrame):
    #: maximal number of rows
    _maxRows: int
    #: GridLayout manager to request available cells.
    _gridLayoutManager: GridLayoutManager

    #: widgets that are added to the panel
    _widgets: typing.List[QtWidgets.QWidget] = []

    # height of the title widget
    _titleHeight: int = 20

    # Panel options signal
    panelOptionClicked = QtCore.pyqtSignal(bool)

    def __init__(self, title: str, maxRows=6, parent=None):
        super().__init__(parent)
        self.setStyleSheet("Panel { background-color: white; }")
        self._maxRows = maxRows
        self._gridLayoutManager = GridLayoutManager(self._maxRows)
        self._widgets = []

        # Main layout
        self._mainLayout = QtWidgets.QVBoxLayout(self)
        self._mainLayout.setContentsMargins(5, 2, 5, 2)
        self._mainLayout.setSpacing(5)

        # Actions layout
        # self._actionsWidget = QtWidgets.QWidget(self)
        self._actionsLayout = QtWidgets.QGridLayout()
        self._actionsLayout.setContentsMargins(5, 0, 5, 0)
        self._actionsLayout.setSpacing(5)
        self._mainLayout.addLayout(self._actionsLayout, 1)

        # Title layout
        self._titleWidget = QtWidgets.QWidget()
        self._titleWidget.setFixedHeight(self._titleHeight)
        self._titleLayout = QtWidgets.QHBoxLayout(self._titleWidget)
        self._titleLayout.setContentsMargins(0, 0, 0, 0)
        self._titleLayout.setSpacing(5)
        self._titleLabel = RibbonPanelTitle()
        self._titleLabel.setText(title)
        self._titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self._titleLayout.addWidget(self._titleLabel, 1)
        self._panelOption = QtWidgets.QToolButton()
        self._panelOption.setAutoRaise(True)
        self._panelOption.setIcon(QtGui.QIcon("icons/linking.png"))
        self._panelOption.setIconSize(QtCore.QSize(16, 16))
        self._panelOption.clicked.connect(self.panelOptionClicked)
        self._titleLayout.addWidget(self._panelOption, 0)

        self._mainLayout.addWidget(self._titleWidget, 0)

    def rowHeight(self) -> int:
        """Return the height of a row."""
        return (
            self.size().height() -
            self._mainLayout.contentsMargins().top() -
            self._mainLayout.contentsMargins().bottom() -
            self._mainLayout.spacing() -
            self._titleWidget.height() -
            self._actionsLayout.contentsMargins().top() -
            self._actionsLayout.contentsMargins().bottom() -
            self._actionsLayout.verticalSpacing() * (self._gridLayoutManager.rows - 1)
        ) / self._gridLayoutManager.rows

    def addWidget(
        self, widget: QtWidgets.QWidget, rowSpan: int = 2, colSpan: int = 1, mode=SpaceFindMode.ColumnWise,
    ):
        """Add a widget to the panel.

        :param widget: The widget to add.
        :param rowSpan: The number of rows the widget should span, 2: small, 3: medium, 6: large.
        :param colSpan: The number of columns the widget should span.
        :param mode: The mode to find spaces.
        """
        self._widgets.append(widget)
        row, col = self._gridLayoutManager.request_cells(rowSpan, colSpan, mode)
        maximumHeight = self.rowHeight() * rowSpan + self._actionsLayout.verticalSpacing() * (rowSpan - 2)
        widget.setMaximumHeight(maximumHeight)
        item = RibbonPanelItemWidget(self)
        item.setFixedHeight(maximumHeight)
        item.addWidget(widget)
        self._actionsLayout.addWidget(
            item, row, col, rowSpan, colSpan, QtCore.Qt.AlignCenter
        )

    def addSmallWidget(self, widget: QtWidgets.QWidget, mode=SpaceFindMode.ColumnWise):
        """Add a small widget to the panel.

        :param widget: The widget to add.
        :param mode: The mode to find spaces.
        :return: The widget that was added.
        """
        return self.addWidget(widget, 2, 1, mode)

    def addMediumWidget(self, widget: QtWidgets.QWidget, mode=SpaceFindMode.ColumnWise):
        """Add a medium widget to the panel.

        :param widget: The widget to add.
        :param mode: The mode to find spaces.
        """
        return self.addWidget(widget, 3, 1, mode)

    def addLargeWidget(self, widget: QtWidgets.QWidget, mode=SpaceFindMode.ColumnWise):
        """Add a large widget to the panel.

        :param widget: The widget to add.
        :param mode: The mode to find spaces.
        """
        return self.addWidget(widget, 6, 1, mode)

    def removeWidget(self, widget: QtWidgets.QWidget):
        """Remove a widget from the panel."""
        self._actionsLayout.removeWidget(widget)

    def widget(self, index: int) -> QtWidgets.QWidget:
        """Get the widget at the given index.

        :param index: The index of the widget, starting from 0.
        :return: The widget at the given index.
        """
        return self._widgets[index]

    def addButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        style: ButtonStyle = ButtonStyle.Large,
        showText: bool = True,
        colSpan: int = 1,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        mode=SpaceFindMode.ColumnWise,
    ) -> RibbonToolButton:
        button = RibbonToolButton(self)
        button.setButtonStyle(style)
        if text:
            button.setText(text)
        if icon:
            button.setIcon(icon)
        if slot:
            button.clicked.connect(slot)
        if shortcut:
            button.setShortcut(shortcut)
        if tooltip:
            button.setToolTip(tooltip)
        if statusTip:
            button.setStatusTip(statusTip)
        button.setMaximumHeight(self.height() - self._titleLabel.sizeHint().height() -
                                self._mainLayout.spacing() -
                                self._mainLayout.contentsMargins().top() -
                                self._mainLayout.contentsMargins().bottom())
        if not showText:
            button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.addWidget(
            button,
            rowSpan=2 if style == ButtonStyle.Small else 3 if style == ButtonStyle.Medium else 6,
            colSpan=colSpan,
            mode=mode,
        )
        return button

    def addSmallButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        colSpan: int = 1,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        mode=SpaceFindMode.ColumnWise,
    ) -> RibbonToolButton:
        return self.addButton(text, icon, ButtonStyle.Small, showText, colSpan,
                              slot, shortcut, tooltip, statusTip, mode)

    def addMediumButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        colSpan: int = 1,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        mode=SpaceFindMode.ColumnWise,
    ) -> RibbonToolButton:
        return self.addButton(text, icon, ButtonStyle.Medium, showText, colSpan,
                              slot, shortcut, tooltip, statusTip, mode)

    def addLargeButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        colSpan: int = 1,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        mode=SpaceFindMode.ColumnWise,
    ) -> RibbonToolButton:
        return self.addButton(text, icon, ButtonStyle.Large, showText, colSpan,
                              slot, shortcut, tooltip, statusTip, mode)

    def addToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        style: ButtonStyle = ButtonStyle.Large,
        showText: bool = True,
        colSpan: int = 1,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        mode=SpaceFindMode.ColumnWise,
    ) -> RibbonToolButton:
        button = self.addButton(text, icon, style, showText, colSpan, slot, shortcut, tooltip, statusTip, mode)
        button.setCheckable(True)
        return button

    def addSmallToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        colSpan: int = 1,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        mode=SpaceFindMode.ColumnWise,
    ) -> RibbonToolButton:
        return self.addToggleButton(
            text, icon, ButtonStyle.Small, showText, colSpan, slot, shortcut, tooltip, statusTip, mode
        )

    def addMediumToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        colSpan: int = 1,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        mode=SpaceFindMode.ColumnWise,
    ) -> RibbonToolButton:
        return self.addToggleButton(
            text, icon, ButtonStyle.Medium, showText, colSpan, slot, shortcut, tooltip, statusTip, mode
        )

    def addLargeToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        colSpan: int = 1,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        mode=SpaceFindMode.ColumnWise,
    ) -> RibbonToolButton:
        return self.addToggleButton(
            text, icon, ButtonStyle.Large, showText, colSpan, slot, shortcut, tooltip, statusTip, mode
        )

    def addComboBox(
        self, items: typing.List[str], rowSpan: int = 2, colSpan: int = 1, mode=SpaceFindMode.ColumnWise
    ) -> QtWidgets.QComboBox:
        comboBox = QtWidgets.QComboBox(self)
        comboBox.addItems(items)
        self.addWidget(comboBox, rowSpan, colSpan, mode)
        return comboBox

    def addFontComboBox(
        self, rowSpan: int = 2, colSpan: int = 1, mode=SpaceFindMode.ColumnWise
    ) -> QtWidgets.QFontComboBox:
        comboBox = QtWidgets.QFontComboBox(self)
        self.addWidget(comboBox, rowSpan, colSpan, mode)
        return comboBox

    def addLineEdit(self, rowSpan: int = 2, colSpan: int = 1, mode=SpaceFindMode.ColumnWise) -> QtWidgets.QLineEdit:
        lineEdit = QtWidgets.QLineEdit(self)
        self.addWidget(lineEdit, rowSpan, colSpan, mode)
        return lineEdit

    def addTextEdit(self, rowSpan: int = 2, colSpan: int = 1, mode=SpaceFindMode.ColumnWise) -> QtWidgets.QTextEdit:
        textEdit = QtWidgets.QTextEdit(self)
        self.addWidget(textEdit, rowSpan, colSpan, mode)
        return textEdit

    def addPlainTextEdit(
        self, rowSpan: int = 2, colSpan: int = 1, mode=SpaceFindMode.ColumnWise
    ) -> QtWidgets.QPlainTextEdit:
        textEdit = QtWidgets.QPlainTextEdit(self)
        self.addWidget(textEdit, rowSpan, colSpan, mode)
        return textEdit

    def addLabel(
        self, text: str, rowSpan: int = 2, colSpan: int = 1, mode=SpaceFindMode.ColumnWise
    ) -> QtWidgets.QLabel:
        label = QtWidgets.QLabel(self)
        label.setText(text)
        self.addWidget(label, rowSpan, colSpan, mode)
        return label

    def addProgressBar(
        self, rowSpan: int = 2, colSpan: int = 1, mode=SpaceFindMode.ColumnWise
    ) -> QtWidgets.QProgressBar:
        progressBar = QtWidgets.QProgressBar(self)
        self.addWidget(progressBar, rowSpan, colSpan, mode)
        return progressBar

    def addSlider(self, rowSpan: int = 2, colSpan: int = 1, mode=SpaceFindMode.ColumnWise) -> QtWidgets.QSlider:
        slider = QtWidgets.QSlider(self)
        slider.setOrientation(QtCore.Qt.Horizontal)
        self.addWidget(slider, rowSpan, colSpan, mode)
        return slider

    def addSpinBox(self, rowSpan: int = 2, colSpan: int = 1, mode=SpaceFindMode.ColumnWise) -> QtWidgets.QSpinBox:
        spinBox = QtWidgets.QSpinBox(self)
        self.addWidget(spinBox, rowSpan, colSpan, mode)
        return spinBox

    def addDoubleSpinBox(
        self, rowSpan: int = 2, colSpan: int = 1, mode=SpaceFindMode.ColumnWise
    ) -> QtWidgets.QDoubleSpinBox:
        doubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.addWidget(doubleSpinBox, rowSpan, colSpan, mode)
        return doubleSpinBox

    def addDateEdit(self, rowSpan: int = 2, colSpan: int = 1, mode=SpaceFindMode.ColumnWise) -> QtWidgets.QDateEdit:
        dateEdit = QtWidgets.QDateEdit(self)
        self.addWidget(dateEdit, rowSpan, colSpan, mode)
        return dateEdit

    def addTimeEdit(self, rowSpan: int = 2, colSpan: int = 1, mode=SpaceFindMode.ColumnWise) -> QtWidgets.QTimeEdit:
        timeEdit = QtWidgets.QTimeEdit(self)
        self.addWidget(timeEdit, rowSpan, colSpan, mode)
        return timeEdit

    def addDateTimeEdit(
        self, rowSpan: int = 2, colSpan: int = 1, mode=SpaceFindMode.ColumnWise
    ) -> QtWidgets.QDateTimeEdit:
        dateTimeEdit = QtWidgets.QDateTimeEdit(self)
        self.addWidget(dateTimeEdit, rowSpan, colSpan, mode)
        return dateTimeEdit

    def addTableWidget(
        self, rowSpan: int = 6, colSpan: int = 1, mode=SpaceFindMode.ColumnWise
    ) -> QtWidgets.QTableWidget:
        tableWidget = QtWidgets.QTableWidget(self)
        self.addWidget(tableWidget, rowSpan, colSpan, mode)
        return tableWidget

    def addTreeWidget(
        self, rowSpan: int = 6, colSpan: int = 1, mode=SpaceFindMode.ColumnWise
    ) -> QtWidgets.QTreeWidget:
        treeWidget = QtWidgets.QTreeWidget(self)
        self.addWidget(treeWidget, rowSpan, colSpan, mode)
        return treeWidget

    def addListWidget(
        self, rowSpan: int = 6, colSpan: int = 1, mode=SpaceFindMode.ColumnWise
    ) -> QtWidgets.QListWidget:
        listWidget = QtWidgets.QListWidget(self)
        self.addWidget(listWidget, rowSpan, colSpan, mode)
        return listWidget

    def addCalendarWidget(
        self, rowSpan: int = 6, colSpan: int = 1, mode=SpaceFindMode.ColumnWise
    ) -> QtWidgets.QCalendarWidget:
        calendarWidget = QtWidgets.QCalendarWidget(self)
        self.addWidget(calendarWidget, rowSpan, colSpan, mode)
        return calendarWidget

    def addSeparator(
        self,
        orientation=QtCore.Qt.Vertical,
        linewidth=6,
        rowSpan: int = 6,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
    ) -> typing.Union[RibbonHorizontalSeparator, RibbonVerticalSeparator]:
        """Add a separator to the panel.

        :param orientation: The orientation of the separator.
        :param linewidth: The width of the separator.
        :param rowSpan: The number of rows the separator spans.
        :param colSpan: The number of columns the separator spans.
        :param mode: The mode of the separator.
        :return: The separator.
        """
        separator = (RibbonHorizontalSeparator(linewidth) if orientation == QtCore.Qt.Horizontal else
                     RibbonVerticalSeparator(linewidth))
        self.addWidget(separator, rowSpan, colSpan, mode)
        return separator

    def addHorizontalSeparator(
        self,
        linewidth=6,
        rowSpan: int = 1,
        colSpan: int = 2,
        mode=SpaceFindMode.ColumnWise
    ) -> RibbonHorizontalSeparator:
        """Add a horizontal separator to the panel.

        :param linewidth: The width of the separator.
        :param rowSpan: The number of rows the separator spans.
        :param colSpan: The number of columns the separator spans.
        :param mode: The mode of the separator.
        :return: The separator.
        """
        return self.addSeparator(QtCore.Qt.Horizontal, linewidth, rowSpan, colSpan, mode)

    def addVerticalSeparator(
        self,
        linewidth=6,
        rowSpan: int = 6,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise
    ) -> RibbonVerticalSeparator:
        """Add a vertical separator to the panel.

        :param linewidth: The width of the separator.
        :param rowSpan: The number of rows the separator spans.
        :param colSpan: The number of columns the separator spans.
        :param mode: The mode of the separator.
        :return: The separator.
        """
        return self.addSeparator(QtCore.Qt.Vertical, linewidth, rowSpan, colSpan, mode)

    def setTitleText(self, text: str):
        """Set the title text of the panel.

        :param text: The text to set.
        """
        self._titleLabel.setText(text)

    def titleText(self):
        """Get the title text of the panel.

        :return: The title text.
        """
        return self._titleLabel.text()
