import typing

from PyQt5.QtCore import QEvent, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QActionEvent, QIcon
from PyQt5.QtWidgets import (
    QAction,
    QFrame,
    QHBoxLayout,
    QMenu,
    QSizePolicy,
    QToolButton,
    QWidget,
    QWidgetAction,
)

from .toolbutton import ToolButton, ButtonStyle
from .separator import Separator


class ButtonGroupWidgetItem:
    action: QWidgetAction
    button: ToolButton
    customWidget: bool

    @typing.overload
    def __init__(self) -> None:
        pass

    @typing.overload
    def __init__(
        self, action: QWidgetAction, button: ToolButton, customWidget: bool
    ) -> None:
        pass

    def __init__(self, *args) -> None:
        if len(args) == 3:
            self.action, self.button, self.customWidget = args
        else:
            self.action = QWidgetAction(None)
            self.button = ToolButton()
            self.customWidget = False

    @typing.overload
    def __eq__(self, action: QWidgetAction) -> bool:
        pass

    @typing.overload
    def __eq__(self, widget: "ButtonGroupWidgetItem") -> bool:
        pass

    def __eq__(self, arg: typing.Union[QWidgetAction, "ButtonGroupWidgetItem"]) -> bool:
        if type(arg) == QWidgetAction:
            return self.action == arg
        else:
            return self.button == arg


class ButtonGroupWidgetPrivate:
    Parent: "ButtonGroupWidget"
    mItems: list[ButtonGroupWidgetItem] = []  # 用于记录所有管理的item

    def __init__(self, parent: "ButtonGroupWidget") -> None:
        self.Parent = parent

    def init(self):
        layout = QHBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.Parent.setLayout(layout)
        self.Parent.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)


class ButtonGroupWidget(QFrame):
    """
    用于管理一组Action,类似于 QToolBar
    """

    actionTriggered = pyqtSignal(QAction)
    m_d: ButtonGroupWidgetPrivate

    def __init__(self, parent=None) -> None:
        super(ButtonGroupWidget, self).__init__(parent=parent)
        self.m_d = ButtonGroupWidgetPrivate(self)
        self.m_d.init()

    def __del__(self) -> None:
        for item in self.m_d.mItems:
            if item.customWidget is True:
                item.action.releaseWidget(item.button)
        del self.m_d
        pass

    def addAction(self, action: QAction) -> None:
        super(ButtonGroupWidget, self).addAction(action)

    def addNewAction(
        self, text: str, icon: QIcon, popMode: QToolButton.ToolButtonPopupMode
    ) -> QAction:
        """生成 action, action 的所有权归 ButtonGroupWidget

        Args:
            text (str): Text
            icon (QIcon): Icon
            popMode (QToolButton.ToolButtonPopupMode): ToolButtonPopupMode

        Returns:
            QAction: Action
        """
        action = QAction(icon, text)
        # btn: ToolButton = sip.cast(self.m_d.mItems[-1].widget, ToolButton)
        if self.m_d.mItems[-1].button:
            self.m_d.mItems[-1].button.setPopupMode(popMode)
        return action

    def addMenu(self, menu: QMenu, popMode: QToolButton.ToolButtonPopupMode) -> None:
        action = menu.menuAction()
        super(ButtonGroupWidget, self).addAction(action)
        # btn: ToolButton = sip.cast(self.m_d.mItems[-1].widget, ToolButton)
        self.m_d.mItems[-1].button.setPopupMode(popMode)

    def addSeparator(self) -> QAction:
        action = QAction(self)
        action.setSeparator(True)
        self.addAction(action)
        return action

    def addWidget(self, w: QWidget) -> QAction:
        action = QWidgetAction(self)

        action.setDefaultWidget(w)
        w.setAttribute(Qt.WA_Hover)
        self.addAction(action)
        return action

    def sizeHint(self) -> QSize:
        return self.layout().sizeHint()

    def minimumSizeHint(self) -> QSize:
        return self.layout().minimumSize()

    def actionEvent(self, event: QActionEvent) -> None:
        item = ButtonGroupWidgetItem()
        item.action = event.action()

        if event.type() == QEvent.ActionAdded:
            if item.action is not None:
                if not item.action.parent() == self:
                    item.action.setParent(self)
                item.widget = item.action.associatedWidgets()[0]
                if item.widget is not None:
                    item.widget.setAttribute(Qt.WA_LayoutUsesWidgetRect)
                    item.customWidget = True
            elif item.action.isSeparator():
                sp: Separator = Separator(self)
                sp.setTopBottomMargins(3, 3)
                item.widget = sp
            # 不是widget，自动生成SARibbonToolButton
            if not item.widget:
                button: ToolButton = ToolButton(self)
                button.setAutoRaise(True)
                button.setFocusPolicy(Qt.NoFocus)
                button.setButtonStyle(ButtonStyle.Small)
                button.setToolButtonStyle(Qt.ToolButtonIconOnly)
                button.setDefaultAction(item.action)
                # 根据QAction的属性设置按钮的大小
                button.triggered.connect(self.actionTriggered)
                item.widget = button
            self.layout().addWidget(item.widget)
            self.m_d.mItems.append(item)

        elif event.type() == QEvent.ActionChanged:
            # 让布局重新绘制
            self.layout().invalidate()
        elif event.type() == QEvent.ActionRemoved:
            item.action.disconnect()
            for item in self.m_d.mItems:
                # widgetAction: QWidgetAction = sip.cast(item.action, QWidgetAction)
                if item.action and item.customWidget:
                    item.action.releaseWidget(item.widget)
                else:
                    # destroy the QToolButton/QToolBarSeparator
                    item.widget.hide()
                    item.widget.deleteLater()
                self.m_d.mItems.remove(item)
            self.layout().invalidate()
        return super().actionEvent(event)
