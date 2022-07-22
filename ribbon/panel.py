import typing
from enum import IntEnum

import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore

from .gallery import RibbonGallery
from .separator import RibbonHorizontalSeparator, RibbonVerticalSeparator
from .toolbutton import RibbonToolButton, ButtonStyle
from .utils import package_source_dir


class RibbonPanelTitle(QtWidgets.QLabel):
    """Widget to display the title of a panel."""
    pass


class SpaceFindMode(IntEnum):
    """Mode to find available space in a grid layout, ColumnWise or RowWise."""
    ColumnWise = 0
    RowWise = 1


class GridLayoutManager(object):
    """Grid Layout Manager."""

    def __init__(self, rows: int):
        """Create a new grid layout manager.

        :param rows: The number of rows in the grid layout.
        """
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
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

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
        """Create a new panel.

        :param title: The title of the panel.
        :param maxRows: The maximal number of rows in the panel.
        :param parent: The parent widget.
        """
        super().__init__(parent)
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
        self._panelOption = RibbonPanelOptionButton()
        self._panelOption.setAutoRaise(True)
        self._panelOption.setIcon(QtGui.QIcon(package_source_dir() + "/icons/linking.png"))
        self._panelOption.setIconSize(QtCore.QSize(16, 16))
        self._panelOption.clicked.connect(self.panelOptionClicked)
        self._titleLayout.addWidget(self._panelOption, 0)

        self._mainLayout.addWidget(self._titleWidget, 0)

    def rowHeight(self) -> int:
        """Return the height of a row."""
        return int((
            self.size().height() -
            self._mainLayout.contentsMargins().top() -
            self._mainLayout.contentsMargins().bottom() -
            self._mainLayout.spacing() -
            self._titleWidget.height() -
            self._actionsLayout.contentsMargins().top() -
            self._actionsLayout.contentsMargins().bottom() -
            self._actionsLayout.verticalSpacing() * (self._gridLayoutManager.rows - 1)
        ) / self._gridLayoutManager.rows)

    def addWidget(
        self,
        widget: QtWidgets.QWidget,
        rowSpan: int = 2,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ):
        """Add a widget to the panel.

        :param widget: The widget to add.
        :param rowSpan: The number of rows the widget should span, 2: small, 3: medium, 6: large.
        :param colSpan: The number of columns the widget should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the widget.
        """
        self._widgets.append(widget)
        row, col = self._gridLayoutManager.request_cells(rowSpan, colSpan, mode)
        maximumHeight = self.rowHeight() * rowSpan + self._actionsLayout.verticalSpacing() * (rowSpan - 2)
        widget.setMaximumHeight(maximumHeight)
        item = RibbonPanelItemWidget(self)
        item.setFixedHeight(maximumHeight)
        item.addWidget(widget)
        self._actionsLayout.addWidget(
            item, row, col, rowSpan, colSpan, alignment
        )

    def addSmallWidget(
        self,
        widget: QtWidgets.QWidget,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ):
        """Add a small widget to the panel.

        :param widget: The widget to add.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the widget.
        :return: The widget that was added.
        """
        return self.addWidget(widget, 2, 1, mode, alignment)

    def addMediumWidget(
        self,
        widget: QtWidgets.QWidget,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ):
        """Add a medium widget to the panel.

        :param widget: The widget to add.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the widget.
        """
        return self.addWidget(widget, 3, 1, mode, alignment)

    def addLargeWidget(
        self,
        widget: QtWidgets.QWidget,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ):
        """Add a large widget to the panel.

        :param widget: The widget to add.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the widget.
        """
        return self.addWidget(widget, 6, 1, mode, alignment)

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
        alignment=QtCore.Qt.AlignCenter,
    ) -> RibbonToolButton:
        """Add a button to the panel.
        
        :param text: The text of the button.
        :param icon: The icon of the button.
        :param style: The style of the button.
        :param showText: Whether to show the text of the button.
        :param colSpan: The number of columns the button should span.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the button.
        
        :return: The button that was added.
        """
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
            alignment=alignment
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
        alignment=QtCore.Qt.AlignCenter,
    ) -> RibbonToolButton:
        """Add a small button to the panel.
            
        :param text: The text of the button.
        :param icon: The icon of the button.
        :param showText: Whether to show the text of the button.
        :param colSpan: The number of columns the button should span.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the button.
        """
        return self.addButton(text, icon, ButtonStyle.Small, showText, colSpan,
                              slot, shortcut, tooltip, statusTip, mode, alignment)

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
        alignment=QtCore.Qt.AlignCenter,
    ) -> RibbonToolButton:
        """Add a medium button to the panel.

        :param text: The text of the button.
        :param icon: The icon of the button.
        :param showText: Whether to show the text of the button.
        :param colSpan: The number of columns the button should span.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the button.
        """
        return self.addButton(text, icon, ButtonStyle.Medium, showText, colSpan,
                              slot, shortcut, tooltip, statusTip, mode, alignment)

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
        alignment=QtCore.Qt.AlignCenter,
    ) -> RibbonToolButton:
        """Add a large button to the panel.

        :param text: The text of the button.
        :param icon: The icon of the button.
        :param showText: Whether to show the text of the button.
        :param colSpan: The number of columns the button should span.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the button.
        """
        return self.addButton(text, icon, ButtonStyle.Large, showText, colSpan,
                              slot, shortcut, tooltip, statusTip, mode, alignment)

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
        alignment=QtCore.Qt.AlignCenter,
    ) -> RibbonToolButton:
        """Add a toggle button to the panel.

        :param text: The text of the button.
        :param icon: The icon of the button.
        :param style: The style of the button.
        :param showText: Whether to show the text of the button.
        :param colSpan: The number of columns the button should span.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the button.
        """
        button = self.addButton(text, icon, style, showText, colSpan,
                                slot, shortcut, tooltip, statusTip, mode, alignment)
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
        alignment=QtCore.Qt.AlignCenter,
    ) -> RibbonToolButton:
        """Add a small toggle button to the panel.

        :param text: The text of the button.
        :param icon: The icon of the button.
        :param showText: Whether to show the text of the button.
        :param colSpan: The number of columns the button should span.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the button.
        """
        return self.addToggleButton(
            text, icon, ButtonStyle.Small, showText, colSpan, slot, shortcut, tooltip, statusTip, mode, alignment
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
        alignment=QtCore.Qt.AlignCenter,
    ) -> RibbonToolButton:
        """Add a medium toggle button to the panel.

        :param text: The text of the button.
        :param icon: The icon of the button.
        :param showText: Whether to show the text of the button.
        :param colSpan: The number of columns the button should span.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the button.
        """
        return self.addToggleButton(
            text, icon, ButtonStyle.Medium, showText, colSpan, slot, shortcut, tooltip, statusTip, mode, alignment
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
        alignment=QtCore.Qt.AlignCenter,
    ) -> RibbonToolButton:
        """Add a large toggle button to the panel.

        :param text: The text of the button.
        :param icon: The icon of the button.
        :param showText: Whether to show the text of the button.
        :param colSpan: The number of columns the button should span.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the button.
        """
        return self.addToggleButton(
            text, icon, ButtonStyle.Large, showText, colSpan, slot, shortcut, tooltip, statusTip, mode, alignment
        )

    def addComboBox(
        self,
        items: typing.List[str],
        rowSpan: int = 2,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QComboBox:
        """Add a combo box to the panel.

        :param items: The items of the combo box.
        :param rowSpan: The number of rows the combo box should span.
        :param colSpan: The number of columns the combo box should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the combo box.
        """
        comboBox = QtWidgets.QComboBox(self)
        comboBox.addItems(items)
        self.addWidget(comboBox, rowSpan, colSpan, mode, alignment)
        return comboBox

    def addFontComboBox(
        self,
        rowSpan: int = 2,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QFontComboBox:
        """Add a font combo box to the panel.

        :param rowSpan: The number of rows the combo box should span.
        :param colSpan: The number of columns the combo box should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the combo box.
        """
        comboBox = QtWidgets.QFontComboBox(self)
        self.addWidget(comboBox, rowSpan, colSpan, mode, alignment)
        return comboBox

    def addLineEdit(
        self,
        rowSpan: int = 2,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QLineEdit:
        """Add a line edit to the panel.

        :param rowSpan: The number of rows the line edit should span.
        :param colSpan: The number of columns the line edit should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the line edit.
        """
        lineEdit = QtWidgets.QLineEdit(self)
        self.addWidget(lineEdit, rowSpan, colSpan, mode, alignment)
        return lineEdit

    def addTextEdit(
        self,
        rowSpan: int = 2,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QTextEdit:
        """Add a text edit to the panel.

        :param rowSpan: The number of rows the text edit should span.
        :param colSpan: The number of columns the text edit should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the text edit.
        """
        textEdit = QtWidgets.QTextEdit(self)
        self.addWidget(textEdit, rowSpan, colSpan, mode, alignment)
        return textEdit

    def addPlainTextEdit(
        self,
        rowSpan: int = 2,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QPlainTextEdit:
        """Add a plain text edit to the panel.

        :param rowSpan: The number of rows the text edit should span.
        :param colSpan: The number of columns the text edit should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the text edit.
        """
        textEdit = QtWidgets.QPlainTextEdit(self)
        self.addWidget(textEdit, rowSpan, colSpan, mode, alignment)
        return textEdit

    def addLabel(
        self,
        text: str,
        rowSpan: int = 2,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QLabel:
        """Add a label to the panel.

        :param text: The text of the label.
        :param rowSpan: The number of rows the label should span.
        :param colSpan: The number of columns the label should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the label.
        """
        label = QtWidgets.QLabel(self)
        label.setText(text)
        self.addWidget(label, rowSpan, colSpan, mode, alignment)
        return label

    def addProgressBar(
        self,
        rowSpan: int = 2,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QProgressBar:
        """Add a progress bar to the panel.

        :param rowSpan: The number of rows the progress bar should span.
        :param colSpan: The number of columns the progress bar should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the progress bar.
        """
        progressBar = QtWidgets.QProgressBar(self)
        self.addWidget(progressBar, rowSpan, colSpan, mode, alignment)
        return progressBar

    def addSlider(
        self,
        rowSpan: int = 2,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QSlider:
        """Add a slider to the panel.

        :param rowSpan: The number of rows the slider should span.
        :param colSpan: The number of columns the slider should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the slider.
        """
        slider = QtWidgets.QSlider(self)
        slider.setOrientation(QtCore.Qt.Horizontal)
        self.addWidget(slider, rowSpan, colSpan, mode, alignment)
        return slider

    def addSpinBox(
        self,
        rowSpan: int = 2,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QSpinBox:
        """Add a spin box to the panel.

        :param rowSpan: The number of rows the spin box should span.
        :param colSpan: The number of columns the spin box should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the spin box.
        """
        spinBox = QtWidgets.QSpinBox(self)
        self.addWidget(spinBox, rowSpan, colSpan, mode, alignment)
        return spinBox

    def addDoubleSpinBox(
        self,
        rowSpan: int = 2,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QDoubleSpinBox:
        """Add a double spin box to the panel.

        :param rowSpan: The number of rows the double spin box should span.
        :param colSpan: The number of columns the double spin box should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the double spin box.
        """
        doubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.addWidget(doubleSpinBox, rowSpan, colSpan, mode, alignment)
        return doubleSpinBox

    def addDateEdit(
        self,
        rowSpan: int = 2,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QDateEdit:
        """Add a date edit to the panel.

        :param rowSpan: The number of rows the date edit should span.
        :param colSpan: The number of columns the date edit should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the date edit.
        """
        dateEdit = QtWidgets.QDateEdit(self)
        self.addWidget(dateEdit, rowSpan, colSpan, mode, alignment)
        return dateEdit

    def addTimeEdit(
        self,
        rowSpan: int = 2,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QTimeEdit:
        """Add a time edit to the panel.

        :param rowSpan: The number of rows the time edit should span.
        :param colSpan: The number of columns the time edit should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the time edit.
        """
        timeEdit = QtWidgets.QTimeEdit(self)
        self.addWidget(timeEdit, rowSpan, colSpan, mode, alignment)
        return timeEdit

    def addDateTimeEdit(
        self,
        rowSpan: int = 2,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QDateTimeEdit:
        """Add a date time edit to the panel.

        :param rowSpan: The number of rows the date time edit should span.
        :param colSpan: The number of columns the date time edit should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the date time edit.
        """
        dateTimeEdit = QtWidgets.QDateTimeEdit(self)
        self.addWidget(dateTimeEdit, rowSpan, colSpan, mode, alignment)
        return dateTimeEdit

    def addTableWidget(
        self,
        rowSpan: int = 6,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QTableWidget:
        """Add a table widget to the panel.

        :param rowSpan: The number of rows the table widget should span.
        :param colSpan: The number of columns the table widget should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the table widget.
        """
        tableWidget = QtWidgets.QTableWidget(self)
        self.addWidget(tableWidget, rowSpan, colSpan, mode, alignment)
        return tableWidget

    def addTreeWidget(
        self,
        rowSpan: int = 6,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QTreeWidget:
        """Add a tree widget to the panel.

        :param rowSpan: The number of rows the tree widget should span.
        :param colSpan: The number of columns the tree widget should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the tree widget.
        """
        treeWidget = QtWidgets.QTreeWidget(self)
        self.addWidget(treeWidget, rowSpan, colSpan, mode, alignment)
        return treeWidget

    def addListWidget(
        self,
        rowSpan: int = 6,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QListWidget:
        """Add a list widget to the panel.

        :param rowSpan: The number of rows the list widget should span.
        :param colSpan: The number of columns the list widget should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the list widget.
        """
        listWidget = QtWidgets.QListWidget(self)
        self.addWidget(listWidget, rowSpan, colSpan, mode, alignment)
        return listWidget

    def addCalendarWidget(
        self,
        rowSpan: int = 6,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> QtWidgets.QCalendarWidget:
        """Add a calendar widget to the panel.

        :param rowSpan: The number of rows the calendar widget should span.
        :param colSpan: The number of columns the calendar widget should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the calendar widget.
        """
        calendarWidget = QtWidgets.QCalendarWidget(self)
        self.addWidget(calendarWidget, rowSpan, colSpan, mode, alignment)
        return calendarWidget

    def addSeparator(
        self,
        orientation=QtCore.Qt.Vertical,
        width=6,
        rowSpan: int = 6,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> typing.Union[RibbonHorizontalSeparator, RibbonVerticalSeparator]:
        """Add a separator to the panel.

        :param orientation: The orientation of the separator.
        :param width: The width of the separator.
        :param rowSpan: The number of rows the separator spans.
        :param colSpan: The number of columns the separator spans.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the separator.
        :return: The separator.
        """
        separator = (RibbonHorizontalSeparator(width) if orientation == QtCore.Qt.Horizontal else
                     RibbonVerticalSeparator(width))
        self.addWidget(separator, rowSpan, colSpan, mode, alignment)
        return separator

    def addHorizontalSeparator(
        self,
        linewidth=6,
        rowSpan: int = 1,
        colSpan: int = 2,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> RibbonHorizontalSeparator:
        """Add a horizontal separator to the panel.

        :param linewidth: The width of the separator.
        :param rowSpan: The number of rows the separator spans.
        :param colSpan: The number of columns the separator spans.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the separator.
        :return: The separator.
        """
        return self.addSeparator(QtCore.Qt.Horizontal, linewidth, rowSpan, colSpan, mode, alignment)

    def addVerticalSeparator(
        self,
        linewidth=6,
        rowSpan: int = 6,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
    ) -> RibbonVerticalSeparator:
        """Add a vertical separator to the panel.

        :param linewidth: The width of the separator.
        :param rowSpan: The number of rows the separator spans.
        :param colSpan: The number of columns the separator spans.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the separator.
        :return: The separator.
        """
        return self.addSeparator(QtCore.Qt.Vertical, linewidth, rowSpan, colSpan, mode, alignment)

    def addGallery(
        self,
        minimumWidth=800,
        popupHideOnClick=False,
        rowSpan: int = 6,
        colSpan: int = 1,
        mode=SpaceFindMode.ColumnWise
    ) -> RibbonGallery:
        """Add a gallery to the panel.

        :param minimumWidth: The minimum width of the gallery.
        :param popupHideOnClick: Whether the gallery popup should be hidden when a user clicks on it.
        :param rowSpan: The number of rows the gallery spans.
        :param colSpan: The number of columns the gallery spans.
        :param mode: The mode of the gallery.
        :return: The gallery.
        """
        gallery = RibbonGallery(minimumWidth, popupHideOnClick, self)
        maximumHeight = self.rowHeight() * rowSpan + self._actionsLayout.verticalSpacing() * (rowSpan - 2)
        gallery.setFixedHeight(maximumHeight)
        self.addWidget(gallery, rowSpan, colSpan, mode)
        return gallery

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
