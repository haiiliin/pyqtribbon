import typing

from PyQt5 import QtGui
from qtpy import QtWidgets, QtCore


class RibbonMenu(QtWidgets.QMenu):

    @typing.overload
    def __init__(self, title: str = '', parent=None):
        pass

    @typing.overload
    def __init__(self, parent=None):
        pass

    def __init__(self, *args, **kwargs):
        """Create a new panel.

        :param title: The title of the menu.
        :param parent: The parent widget.
        """
        if (args and not isinstance(args[0], QtWidgets.QWidget)) or ('title' in kwargs):
            title = args[0] if len(args) > 0 else kwargs.get('title', '')
            parent = args[1] if len(args) > 1 else kwargs.get('parent', None)
        else:
            title = ''
            parent = args[0] if len(args) > 0 else kwargs.get('parent', None)
        super().__init__(title, parent)
        self.setFont(QtWidgets.QApplication.instance().font())

    def addWidget(self, widget: QtWidgets.QWidget):
        """Add a widget to the menu.

        :param widget: The widget to add.
        """
        widgetAction = QtWidgets.QWidgetAction(self)
        widgetAction.setDefaultWidget(widget)
        self.addAction(widgetAction)

    def addHorizontalLayoutWidget(self) -> QtWidgets.QHBoxLayout:
        """Add a horizontal layout widget to the menu.

        :return: The horizontal layout.
        """
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.addWidget(widget)
        return layout

    def addVerticalLayoutWidget(self) -> QtWidgets.QVBoxLayout:
        """Add a vertical layout widget to the menu.

        :return: The vertical layout.
        """
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.addWidget(widget)
        return layout

    def addGridLayoutWidget(self) -> QtWidgets.QGridLayout:
        """Add a grid layout widget to the menu.

        :return: The grid layout.
        """
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.addWidget(widget)
        return layout

    def addFormLayoutWidget(self) -> QtWidgets.QFormLayout:
        """Add a form layout widget to the menu.

        :return: The form layout.
        """
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.addWidget(widget)
        return layout

    def addSpacing(self, spacing: int = 5):
        """Add spacing to the menu.

        :param spacing: The spacing.
        """
        spacer = QtWidgets.QLabel()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        spacer.setFixedHeight(spacing)
        self.addWidget(spacer)

    def addLabel(self, text: str = '', alignment: QtCore.Qt.Alignment = QtCore.Qt.AlignLeft):
        """Add a label to the menu.

        :param text: The text of the label.
        :param alignment: The alignment of the label.
        """
        label = QtWidgets.QLabel(text)
        label.setAlignment(alignment)
        self.addWidget(label)


class RibbonPermanentMenu(RibbonMenu):
    """
    A permanent menu.
    """
    actionAdded = QtCore.Signal(QtWidgets.QAction)

    def hideEvent(self, a0: QtGui.QHideEvent) -> None:
        self.show()

    def actionEvent(self, a0: QtGui.QActionEvent) -> None:
        if a0.type() == QtGui.QActionEvent.ActionAdded:
            self.actionAdded.emit(a0.action())
        super().actionEvent(a0)
