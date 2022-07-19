import copy
import typing
from enum import IntEnum

from PyQt5 import QtGui
from PyQt5.QtCore import QEvent, QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QCursor, QFocusEvent, QIcon, QMouseEvent, QPainter, QPaintEvent, QPalette, QPixmap, QResizeEvent
from PyQt5.QtWidgets import (QSizePolicy, QStyle, QStyleOption, QStyleOptionFocusRect, QStyleOptionToolButton,
                             QStylePainter, QToolButton, QWidget)


LITE_LARGE_BUTTON_ICON_HIGH_RATE = 0.52
ARROW_WIDTH = 10
LARGE_BUTTON_ICON_RATIO = 1/2


class ButtonStyle(IntEnum):
    Small = 0
    Medium = 1
    Large = 2


class ToolButton(QToolButton):
    """ToolButton, modified from `github.com/czyt1988/SARibbon <https://github.com/czyt1988/SARibbon>`_.
    """
    #: Button style
    buttonStyle: ButtonStyle

    mouseOnSubControl: bool = False  # /< 这个用于标记MenuButtonPopup模式下，鼠标在文本区域
    menuButtonPressed: bool = False
    iconRect: QRect = QRect()
    isWordWrap: bool = False  # /< 标记是否文字换行 @default False

    @typing.overload
    def __init__(self, icon: QtGui.QIcon, text: str, style=ButtonStyle.Large, parent=None):
        """Create a new action with an icon and text.

        :param icon: The icon of the action.
        :param text: The text of the action.
        :param style: The buttonStyle of the action.
        :param parent: The parent of the action.
        """
        pass

    @typing.overload
    def __init__(self, text: str, style=ButtonStyle.Large, parent=None):
        """Create a new action with text.

        :param text: The text of the action.
        :param style: The buttonStyle of the action.
        :param parent: The parent of the action.
        """
        pass

    @typing.overload
    def __init__(self, style=ButtonStyle.Large, parent=None):
        """Create a new action without an icon or text.

        :param style: The buttonStyle of the action.
        :param parent: The parent of the action.
        """
        pass

    @typing.overload
    def __init__(self, parent=None):
        """Create a new action without an icon or text.

        :param parent: The parent of the action.
        """
        pass

    def __init__(self, *args, **kwargs):
        if (args and isinstance(args[0], QtGui.QIcon)) or (kwargs and 'icon' in kwargs):
            self.buttonStyle = args[2] if len(args) > 2 else kwargs.get('buttonStyle', ButtonStyle.Large)
            super().__init__(args[3] if len(args) > 3 else kwargs.get('parent', None))
            self.setIcon(kwargs.get('icon', args[0]))
            self.setText(kwargs.get('text', args[1]))
        elif (args and isinstance(args[0], str)) or (kwargs and 'text' in kwargs):
            self.buttonStyle = args[1] if len(args) > 1 else kwargs.get('buttonStyle', ButtonStyle.Large)
            super().__init__(args[2] if len(args) > 2 else kwargs.get('parent', None))
            self.setText(kwargs.get('text', args[0]))
        elif (args and isinstance(args[0], ButtonStyle)) or (kwargs and 'buttonStyle' in kwargs):
            self.buttonStyle = args[0] if len(args) > 0 else kwargs.get('buttonStyle', ButtonStyle.Large)
            super().__init__(args[1] if len(args) > 1 else kwargs.get('parent', None))
        else:
            self.buttonStyle = ButtonStyle.Large
            super().__init__(args[0] if len(args) > 0 else kwargs.get('parent', None))

        # Styles
        self.setButtonStyle(self.buttonStyle)
        self.setAutoRaise(True)
        self.setFocusPolicy(Qt.NoFocus)
        # self.setStyleSheet("background-color: transparent;")

    def setButtonStyle(self, buttonStyle: ButtonStyle) -> None:
        """Set the buttonStyle of the button.

        :param buttonStyle: The button Style of the button.
        """
        self.buttonStyle = buttonStyle
        if buttonStyle in [ButtonStyle.Large, ButtonStyle.Medium]:
            self.setIconSize(QSize(48, 48) if buttonStyle == ButtonStyle.Large else QSize(32, 32))
            self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        else:
            self.setIconSize(QSize(24, 24))
            self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.setMouseTracking(True)

    def minimumSizeHint(self) -> QSize:
        return self.sizeHint()

    def event(self, e: QEvent) -> bool:
        if e.type() in [QEvent.WindowDeactivate,
                        QEvent.ActionChanged,
                        QEvent.ActionRemoved,
                        QEvent.ActionAdded]:
            self.mouseOnSubControl = False

        return super().event(e)

    def paintEvent(self, event: QPaintEvent) -> None:
        if self.buttonStyle in [ButtonStyle.Large, ButtonStyle.Medium]:
            self._paintLargeButton()
        elif self.buttonStyle == ButtonStyle.Small:
            self._paintSmallButton()

    def resizeEvent(self, e: QResizeEvent) -> None:
        super().resizeEvent(e)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if self.buttonStyle in (ButtonStyle.Large, ButtonStyle.Medium):
            isMouseOnSubControl = e.pos().y() > self.height() / 2
        else:
            isMouseOnSubControl = not self.iconRect.contains(e.pos())

        if not self.mouseOnSubControl == isMouseOnSubControl:
            self.mouseOnSubControl = isMouseOnSubControl
            self.update()

        super().mouseMoveEvent(e)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.LeftButton and self.popupMode() == QStyleOptionToolButton.MenuButtonPopup:
            if self.buttonStyle in [ButtonStyle.Large, ButtonStyle.Medium]:
                popup = self.rect().adjusted(0, self.height() / 2, 0, 0)
                if popup.isValid() and popup.contains(e.pos()):
                    self.menuButtonPressed = True
                    self.showMenu()
                    return
            else:
                if self.iconRect.isValid() and not self.iconRect.contains(e.pos()):
                    self.menuButtonPressed = True
                    self.showMenu()
                return

        self.menuButtonPressed = False
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        self.menuButtonPressed = False
        super().mouseReleaseEvent(e)

    def focusOutEvent(self, e: QFocusEvent) -> None:
        self.mouseOnSubControl = False
        super().focusOutEvent(e)

    def leaveEvent(self, e: QEvent) -> None:
        self.mouseOnSubControl = False
        super().leaveEvent(e)

    def hitButton(self, pos: QPoint) -> bool:
        if super().hitButton(pos):
            return not self.menuButtonPressed
        return False

    def sizeHint(self) -> QSize:
        size: QSize = super().sizeHint()
        opt = QStyleOptionToolButton()
        self.initStyleOption(opt)
        # QToolButton的sizeHint已经考虑了菜单箭头的位置
        if self.buttonStyle in [ButtonStyle.Large, ButtonStyle.Medium]:
            # 计算最佳大小
            if size.width() > size.height() * 1.4:
                # 文本对齐方式
                alignment = Qt.TextShowMnemonic | Qt.TextWordWrap
                # 如果宽度大于高度，就看看换行是否能满足
                fm = self.fontMetrics()
                # 计算默认的文本区域
                textRange = self._calcTextRect(QRect(0, 0, size.width() / 2, size.height()))
                textRange.moveTo(0, 0)
                # 计算换行后的最大文本区域
                textRange = fm.boundingRect(textRange, alignment, self.text())
                # 把区域设置给size
                size.setWidth(textRange.width() + 4)
                # 确认是否换行
                self.isWordWrap = (textRange.height() > fm.lineSpacing())
                if (opt.features & QStyleOptionToolButton.Menu) or (opt.features & QStyleOptionToolButton.HasMenu):
                    # 如果有菜单
                    if self.buttonStyle == ButtonStyle.Medium:
                        # lite模式下都要偏移
                        size.setWidth(size.width() + ARROW_WIDTH)
                    elif self.isWordWrap:
                        size.setWidth(size.width() + ARROW_WIDTH)

            else:
                self.isWordWrap = '\n' in self.text()
                opt = QStyleOptionToolButton()
                self.initStyleOption(opt)
                if (opt.features & QStyleOptionToolButton.Menu) or (opt.features & QStyleOptionToolButton.HasMenu):
                    # 如果有菜单
                    if self.buttonStyle == ButtonStyle.Large and self.isWordWrap:
                        size.setWidth(size.width() + ARROW_WIDTH)

        else:
            #  InstantPopup在QToolButton不会添加控件来放下箭头，这里处理的和MenuButtonPopup一致
            #  在仅有图标的小模式显示时，预留一个下拉箭头位置
            if Qt.ToolButtonIconOnly == self.toolButtonStyle():
                if (opt.features & QStyleOptionToolButton.Menu) or (opt.features & QStyleOptionToolButton.HasMenu):
                    # 如果有菜单
                    size.setWidth(size.width() + ARROW_WIDTH)
            else:
                if (opt.features & QStyleOptionToolButton.Menu) or (opt.features & QStyleOptionToolButton.HasMenu):
                    pass
                else:
                    size.setWidth(size.width() - 4)

        return size

    def _paintSmallButton(self) -> None:
        p = QStylePainter(self)
        option = QStyleOptionToolButton()
        self.initStyleOption(option)
        if option.features & QStyleOptionToolButton.MenuButtonPopup or option.features & QStyleOptionToolButton.HasMenu:
            if not self.rect().contains(self.mapFromGlobal(QCursor.pos())):
                option.state &= not QStyle.State_MouseOver

        autoRaise: bool = option.state & QStyle.State_AutoRaise
        bFlags = option.state & ~QStyle.State_Sunken
        mFlags = bFlags
        if autoRaise:
            if not (bFlags & QStyle.State_MouseOver) or not (bFlags & QStyle.State_Enabled):
                bFlags &= ~QStyle.State_Raised

        if option.state & QStyle.State_Sunken:
            if option.activeSubControls & QStyle.SC_ToolButton:
                bFlags |= QStyle.State_Sunken
                mFlags |= QStyle.State_MouseOver | QStyle.State_Sunken
            elif option.activeSubControls & QStyle.SC_ToolButtonMenu:
                mFlags |= QStyle.State_Sunken
                bFlags |= QStyle.State_MouseOver

        # 绘制背景
        tool = QStyleOption(0)
        tool.palette = option.palette
        if (option.subControls & QStyle.SC_ToolButton) and (option.features & QStyleOptionToolButton.MenuButtonPopup):
            tool.rect = option.rect
            tool.state = bFlags
            if option.activeSubControls & QStyle.SC_ToolButtonMenu:
                option.activeSubControls &= QStyle.SC_ToolButtonMenu
                # 菜单激活
                self.style().drawPrimitive(QStyle.PE_PanelButtonTool, tool, p, self)
                tool.rect = self.iconRect.adjusted(1, 1, -1, -1)
                tool.state = QStyle.State_Raised  # 把图标区域显示为正常
                if autoRaise:
                    self.style().drawPrimitive(QStyle.PE_PanelButtonTool, tool, p, self)
                else:
                    self.style().drawPrimitive(QStyle.PE_PanelButtonBevel, tool, p, self)

            else:
                self.style().drawPrimitive(QStyle.PE_PanelButtonTool, tool, p, self)
                if tool.state & QStyle.State_MouseOver:
                    if self.mouseOnSubControl:  # 此时鼠标在indicate那
                        # 鼠标在文字区，把图标显示为正常
                        tool.rect = self.iconRect.adjusted(1, 1, -1, -1)
                        tool.state = QStyle.State_Raised  # 把图标区域显示为正常
                        if autoRaise:
                            self.style().drawPrimitive(QStyle.PE_PanelButtonTool, tool, p, self)
                        else:
                            self.style().drawPrimitive(QStyle.PE_PanelButtonBevel, tool, p, self)

                    else:
                        # 鼠标在图标区，把文字显示为正常
                        tool.state = QStyle.State_Raised  # 把图标区域显示为正常
                        tool.rect = option.rect.adjusted(self.iconRect.width() + 1, 1, -1, -1)
                        if autoRaise:
                            self.style().drawPrimitive(QStyle.PE_PanelButtonTool, tool, p, self)
                        else:
                            self.style().drawPrimitive(QStyle.PE_PanelButtonBevel, tool, p, self)

        elif (option.subControls & QStyle.SC_ToolButton) & (option.features & QStyleOptionToolButton.HasMenu):
            tool.rect = option.rect
            tool.state = bFlags
            if autoRaise:
                self.style().drawPrimitive(QStyle.PE_PanelButtonTool, tool, p, self)
            else:
                self.style().drawPrimitive(QStyle.PE_PanelButtonBevel, tool, p, self)

        elif option.subControls & QStyle.SC_ToolButton:
            tool.rect = option.rect
            tool.state = bFlags
            if option.state & QStyle.State_Sunken:
                tool.state &= ~QStyle.State_MouseOver

            if autoRaise:
                self.style().drawPrimitive(QStyle.PE_PanelButtonTool, tool, p, self)
            else:
                self.style().drawPrimitive(QStyle.PE_PanelButtonBevel, tool, p, self)
        self._drawIconAndLabel(p, option)

    def _paintLargeButton(self) -> None:
        painter = QPainter(self)
        option = QStyleOptionToolButton()
        self.initStyleOption(option)
        if option.features & QStyleOptionToolButton.MenuButtonPopup or \
                option.features & QStyleOptionToolButton.HasMenu:
            if not self.rect().contains(self.mapFromGlobal(QCursor.pos())):
                option.state &= ~QStyle.State_MouseOver

        autoRaise = option.state & QStyle.State_AutoRaise
        bFlags = option.state & ~QStyle.State_Sunken
        if autoRaise:
            # 如果autoRaise，但鼠标不在按钮上或者按钮不是激活状态，去除raised状态
            if not (bFlags & QStyle.State_MouseOver) or not (bFlags & QStyle.State_Enabled):
                bFlags &= ~QStyle.State_Raised

        if option.state & QStyle.State_Sunken:
            if option.activeSubControls & QStyle.SC_ToolButton:
                bFlags |= QStyle.State_Sunken
            elif option.activeSubControls & QStyle.SC_ToolButtonMenu:
                bFlags |= QStyle.State_MouseOver

        # 绘制背景
        tool = QStyleOption(0)
        tool.palette = option.palette
        # MenuButtonPopup特殊处理
        if (option.subControls & QStyle.SC_ToolButton) and \
                (option.features & QStyleOptionToolButton.MenuButtonPopup):
            # 此时按钮的菜单弹出
            tool.rect = option.rect
            tool.state = bFlags
            option.activeSubControls &= QStyle.SC_ToolButtonMenu
            if option.activeSubControls & QStyle.SC_ToolButtonMenu:
                self.style().drawPrimitive(QStyle.PE_PanelButtonTool, tool, painter, self)
                # 菜单激活
                self.style().drawPrimitive(QStyle.PE_PanelButtonTool, tool, painter, self)
                tool.rect = self.iconRect.adjusted(1, 1, -1, -1)
                tool.state = QStyle.State_Raised  # 把图标区域显示为正常
                if autoRaise:
                    self.style().drawPrimitive(QStyle.PE_PanelButtonTool, tool, painter, self)
                else:
                    self.style().drawPrimitive(QStyle.PE_PanelButtonBevel, tool, painter, self)

            else:
                self.style().drawPrimitive(QStyle.PE_PanelButtonTool, tool, painter, self)
                if tool.state & QStyle.State_MouseOver:
                    if self.mouseOnSubControl:  # 此时鼠标在indicator那
                        # 鼠标在文字区，把图标显示为正常
                        tool.rect = self.iconRect.adjusted(1, 1, -1, -1)
                        tool.state = QStyle.State_Raised  # 把图标区域显示为正常
                        if autoRaise:
                            self.style().drawPrimitive(QStyle.PE_PanelButtonTool, tool, painter, self)
                        else:
                            self.style().drawPrimitive(QStyle.PE_PanelButtonBevel, tool, painter, self)

                    else:
                        # 鼠标在图标区，把文字显示为正常
                        tool.state = QStyle.State_Raised  # 把图标区域显示为正常
                        tool.rect = option.rect.adjusted(1, self.iconRect.height() + 1, -1, -1)
                        if autoRaise:
                            self.style().drawPrimitive(QStyle.PE_PanelButtonTool, tool, painter, self)
                        else:
                            self.style().drawPrimitive(QStyle.PE_PanelButtonBevel, tool, painter, self)
        elif option.subControls & QStyle.SC_ToolButton and option.features & QStyleOptionToolButton.HasMenu:
            # 按钮含有菜单
            tool.rect = option.rect
            tool.state = bFlags
            if autoRaise:
                self.style().drawPrimitive(QStyle.PE_PanelButtonTool, tool, painter, self)
            else:
                self.style().drawPrimitive(QStyle.PE_PanelButtonBevel, tool, painter, self)

        elif option.subControls & QStyle.SC_ToolButton:
            tool.rect = option.rect
            tool.state = bFlags
            if option.state & QStyle.State_Sunken:
                tool.state &= ~QStyle.State_MouseOver
            if autoRaise:
                self.style().drawPrimitive(QStyle.PE_PanelButtonTool, tool, painter, self)
            else:
                self.style().drawPrimitive(QStyle.PE_PanelButtonBevel, tool, painter, self)

        # 绘制Focus
        if option.state & QStyle.State_HasFocus:
            fr = QStyleOptionFocusRect()
            fr.rect.adjust(3, 3, -3, -3)
            if option.features & QStyleOptionToolButton.MenuButtonPopup:
                fr.rect.adjust(0, 0, -self.style().pixelMetric(QStyle.PM_MenuButtonIndicator, option, self), 0)

            self.style().drawPrimitive(QStyle.PE_FrameFocusRect, fr, painter, self)
        self._drawIconAndLabel(painter, option)

    def _drawIconAndLabel(self, painter: QPainter, option: QStyleOptionToolButton) -> None:
        """在LargeButtonType == Normal模式下，icon占大按钮的一半区域，在wps模式下，icon占大按钮的60%，文字占40%，且文字不换行 
        
        :param painter: 
        :param option: 
        """
        self.iconRect = self._calcIconRect(option)
        pm = self._createIconPixmap(option)
        if self.buttonStyle in [ButtonStyle.Large, ButtonStyle.Medium]:
            # 绘制图标和文字
            textRect = self._calcTextRect(option)
            hasArrow = bool(option.features & QStyleOptionToolButton.Arrow)
            if not hasArrow and option.icon.isNull() and not len(option.text) == 0 or \
                    option.toolButtonStyle == Qt.ToolButtonTextOnly:
                # 没有箭头 且 没图标 且 有文字 or 只有文字模式
                alignment = Qt.AlignCenter | Qt.TextShowMnemonic | Qt.TextWordWrap  # 纯文本下，居中对齐,换行
                if not self.style().styleHint(QStyle.SH_UnderlineShortcut, option, self):
                    alignment |= Qt.TextHideMnemonic

                painter.setFont(option.font)
                self.style().drawItemText(painter, textRect, alignment, option.palette,
                                          option.state & QStyle.State_Enabled,
                                          option.text, QPalette.ButtonText)
            else:
                # 非纯文本
                if not option.toolButtonStyle == Qt.ToolButtonIconOnly:
                    # 文本加图标情况
                    painter.setFont(option.font)
                    alignment = Qt.TextShowMnemonic | Qt.TextWordWrap  # 换行
                    if not self.style().styleHint(QStyle.SH_UnderlineShortcut, option, self):
                        alignment |= Qt.TextHideMnemonic

                    # 文字在icon下
                    # 先绘制图标
                    if not hasArrow:
                        # if SA_RIBBON_DEBUG_HELP_DRAW:
                        # HELP_DRAW_RECT(painter, self.m_iconRect)
                        # endif
                        self.style().drawItemPixmap(painter, self.iconRect, Qt.AlignCenter, pm)
                    else:
                        self._drawArrow(self.style(), option, self.iconRect, painter, self)

                    # if SA_RIBBON_DEBUG_HELP_DRAW:
                    # HELP_DRAW_RECT(painter, textRect)
                    # endif
                    if self.buttonStyle == ButtonStyle.Large:
                        alignment = alignment | Qt.AlignHCenter | Qt.AlignTop  # 文字是顶部对齐
                    else:
                        alignment = alignment | Qt.AlignCenter

                    # 再绘制文本，对于Normal模式下的LargeButton，如果有菜单，且m_isWordWrap是True，箭头将在文本旁边
                    self.style().drawItemText(painter, QStyle.visualRect(option.direction, option.rect, textRect),
                                              alignment, option.palette,
                                              option.state & QStyle.State_Enabled, option.text, QPalette.ButtonText)
                else:
                    # 只有图标情况
                    if hasArrow:
                        self._drawArrow(self.style(), option, option.rect, painter, self)
                    else:
                        self.style().drawItemPixmap(painter, self.iconRect, Qt.AlignCenter, pm)

                # 绘制sub control 的下拉箭头
                if option.features & QStyleOptionToolButton.HasMenu:
                    option.rect = self._calcIndicatorArrowDownRect(option)
                    self.style().drawPrimitive(QStyle.PE_IndicatorArrowDown, option, painter, self)
        else:
            # 小图标
            # pmSize = opt.iconSize
            if not option.icon.isNull():
                # pmSize = pm.size() / pm.devicePixelRatio()
                if not option.toolButtonStyle == Qt.ToolButtonIconOnly:
                    painter.save()
                    painter.setFont(option.font)
                    pr = self.iconRect  # 图标区域
                    tr = option.rect.adjusted(pr.width() + 2, 0, -1, 0)  # 文本区域
                    alignment = Qt.TextShowMnemonic
                    # 快捷键的下划线
                    if not self.style().styleHint(QStyle.SH_UnderlineShortcut, option, self):
                        alignment |= Qt.TextHideMnemonic

                    if option.toolButtonStyle == Qt.ToolButtonTextUnderIcon:
                        pass
                        # ribbonButton在小图标下，不支持ToolButtonTextUnderIcon
                    else:
                        self.style().drawItemPixmap(painter, QStyle.visualRect(option.direction, option.rect, pr),
                                                    Qt.AlignCenter, pm)
                        alignment = alignment | Qt.AlignLeft | Qt.AlignVCenter

                    self.style().drawItemText(painter, QStyle.visualRect(option.direction, option.rect, tr),
                                              alignment, option.palette,
                                              option.state & QStyle.State_Enabled, option.text,
                                              QPalette.ButtonText)
                    painter.restore()
                else:
                    self.style().drawItemPixmap(painter, self.iconRect, Qt.AlignCenter, pm)

            else:  # 只有文字
                alignment = Qt.TextShowMnemonic
                # 快捷键的下划线
                if not self.style().styleHint(QStyle.SH_UnderlineShortcut, option, self):
                    alignment |= Qt.TextHideMnemonic

                self.style().drawItemText(painter,
                                          QStyle.visualRect(option.direction, option.rect,
                                                            option.rect.adjusted(2, 1, -2, -1)),
                                          alignment, option.palette, option.state & QStyle.State_Enabled, option.text,
                                          QPalette.ButtonText)

            # 绘制sub control 的下拉箭头
            if option.features & QStyleOptionToolButton.HasMenu:
                tool = option
                tool.rect = self._calcIndicatorArrowDownRect(tool)
                self.style().drawPrimitive(QStyle.PE_IndicatorArrowDown, tool, painter, self)

    @staticmethod
    def _drawArrow(style: QStyle, toolButton: QStyleOptionToolButton, rect: QRect, painter: QPainter,
                   widget: QWidget) -> None:
        # pe = QStyle.PrimitiveElement()
        if toolButton.arrowType == Qt.LeftArrow:
            pe = QStyle.PE_IndicatorArrowLeft
        elif toolButton.arrowType == Qt.RightArrow:
            pe = QStyle.PE_IndicatorArrowRight
        elif toolButton.arrowType == Qt.UpArrow:
            pe = QStyle.PE_IndicatorArrowUp
        elif toolButton.arrowType == Qt.DownArrow:
            pe = QStyle.PE_IndicatorArrowDown
        else:
            return

        arrowOpt = toolButton
        arrowOpt.rect = rect
        style.drawPrimitive(pe, arrowOpt, painter, widget)

    @staticmethod
    def _liteLargeButtonIconHeight(buttonHeight: int) -> int:
        return int(buttonHeight * LITE_LARGE_BUTTON_ICON_HIGH_RATE)

    def _calcIconRect(self, opt: QStyleOptionToolButton) -> QRect:
        """根据设定计算图标的绘制区域

        :param opt: QStyleOptionToolButton
        :return: None
        """
        if self.buttonStyle in [ButtonStyle.Large, ButtonStyle.Medium]:
            iconRect = copy.deepcopy(opt.rect)
            if not opt.toolButtonStyle == Qt.ToolButtonIconOnly:
                if self.buttonStyle == ButtonStyle.Large:
                    iconRect.setHeight(opt.rect.height() * LARGE_BUTTON_ICON_RATIO)
                elif self.buttonStyle == ButtonStyle.Medium:
                    iconRect.setHeight(self._liteLargeButtonIconHeight(opt.rect.height()))
        else:
            if opt.toolButtonStyle == Qt.ToolButtonIconOnly:
                #  InstantPopup在QToolButton不会添加控件来放下箭头，这里处理的和MenuButtonPopup一致
                #  在仅有图标的小模式显示时，预留一个下拉箭头位置
                iconRect = self.rect()
                if opt.features & QStyleOptionToolButton.Menu or opt.features & QStyleOptionToolButton.HasMenu:
                    # 如果有菜单
                    iconRect.adjust(0, 0, -ARROW_WIDTH, 0)
            else:
                iconRect = QRect(0, 0, max(opt.rect.height(), opt.iconSize.width()), opt.rect.height())
        return iconRect

    @typing.overload
    def _calcTextRect(self, option: QStyleOptionToolButton) -> QRect:
        """根据设定计算文本显示区域

        :param option: QStyleOptionToolButton
        :return: QRect 文字区域
        """
        pass

    @typing.overload
    def _calcTextRect(self, buttonRect: QRect, hasMenu: bool = False) -> QRect:
        """根据按钮区域计算文字范围

        在大按钮模式下，有几种情况:

        - 第一种，文字没有菜单，此时文本矩形占满下半矩形

        - 第二种，文本带有菜单，但没换行，此时下拉箭头在底部预留的10像素区域

        - 第三种，文本带有菜单，且换行了，此时下拉箭头在旁边

        :param buttonRect: 按钮的几何区域
        :param hasMenu: 是否有菜单
        :return: 文字区域
        """
        pass

    def _calcTextRect(self, *args) -> QRect:
        if type(args[0]) == QStyleOptionToolButton:
            opt: QStyleOptionToolButton = args[0]
            shiftX: int = 0
            shiftY: int = 0
            if opt.state & (QStyle.State_Sunken | QStyle.State_On):
                shiftX = self.style().pixelMetric(QStyle.PM_ButtonShiftHorizontal, opt, self)
                shiftY = self.style().pixelMetric(QStyle.PM_ButtonShiftVertical, opt, self)
            rect = self._calcTextRect(opt.rect, opt.features & QStyleOptionToolButton.HasMenu or
                                      opt.features & QStyleOptionToolButton.Menu)
            rect.translate(shiftX, shiftY)
            return rect
        elif type(args[0]) == QRect:
            buttonRect: QRect = args[0]
            hasMenu = bool(args[1]) if len(args) == 2 else False
            rect = copy.deepcopy(buttonRect)
            if self.toolButtonStyle() == Qt.ToolButtonTextOnly or self.icon().isNull():
                return rect

            if self.buttonStyle == ButtonStyle.Large:
                if hasMenu:
                    if self.isWordWrap:
                        # 预留ARROW_WIDTH绘制箭头，1px的上下边界
                        rect.adjust(1, buttonRect.height() * LARGE_BUTTON_ICON_RATIO, -ARROW_WIDTH, -1)
                    else:
                        # 预留ARROW_WIDTH绘制箭头，1px的上下边界
                        rect.adjust(1, buttonRect.height() * LARGE_BUTTON_ICON_RATIO, -1, -ARROW_WIDTH)
                else:
                    # 没有菜单不用预留箭头，1px的上下边界
                    rect.adjust(1, buttonRect.height() * LARGE_BUTTON_ICON_RATIO, -1, -1)

            elif self.buttonStyle == ButtonStyle.Medium:
                if hasMenu:
                    rect.adjust(1, self._liteLargeButtonIconHeight(buttonRect.height()), -ARROW_WIDTH, -1)
                else:
                    rect.adjust(1, self._liteLargeButtonIconHeight(buttonRect.height()), -1, -1)
            else:
                if not self.toolButtonStyle() == Qt.ToolButtonIconOnly:
                    if hasMenu:
                        rect = buttonRect.adjusted(self.iconRect.width(), 0, - ARROW_WIDTH, 0)
                    else:
                        rect = buttonRect.adjusted(self.iconRect.width(), 0, -1, 0)
            return rect

    def _calcIndicatorArrowDownRect(self, opt: QStyleOptionToolButton) -> QRect:
        """sub control 的下拉箭头的位置

        :param opt: QStyleOptionToolButton
        :return: QRect
        """
        # 预留8px绘制箭头，1px的上下边界
        rect = opt.rect
        if self.buttonStyle == ButtonStyle.Large:
            if self.isWordWrap:
                rect.adjust(rect.width() - ARROW_WIDTH, rect.height() / 2, 1, 1)
            else:
                rect.adjust(1, rect.height() - ARROW_WIDTH, 1, 1)

        elif self.buttonStyle == ButtonStyle.Medium:
            rect.adjust(rect.width() - ARROW_WIDTH, self._liteLargeButtonIconHeight(opt.rect.height()), 1, 1)

        else:
            rect.adjust(rect.width() - ARROW_WIDTH, 1, 1, 1)

        return rect

    def _createIconPixmap(self, opt: QStyleOptionToolButton) -> QPixmap:
        if not opt.icon.isNull():  # 有图标
            state: QIcon.State = QIcon.On if opt.state & QStyle.State_On else QIcon.Off
            if not (opt.state & QStyle.State_Enabled):
                mode = QIcon.Disabled
            elif (opt.state & QStyle.State_MouseOver) and (opt.state & QStyle.State_AutoRaise):
                mode = QIcon.Active
            else:
                mode = QIcon.Normal
            return opt.icon.pixmap(self.window().windowHandle(), opt.rect.size().boundedTo(opt.iconSize), mode, state)
        else:
            return QPixmap()
