//
// Created by hailin on 8/21/2024.
//

#ifndef PYQTRIBBON_TOOLBUTTON_HPP
#define PYQTRIBBON_TOOLBUTTON_HPP

#include <QSize>
#include <QStyle>
#include <QToolButton>

#include "constants.hpp"

namespace qtribbon {

class RibbonToolButton : public QToolButton {
    Q_OBJECT

   private:
    RibbonButtonStyle _buttonStyle;
    int _largeButtonIconSize;
    int _mediumButtonIconSize;
    int _smallButtonIconSize;
    int _maximumIconSize;

   public:
    explicit RibbonToolButton(QWidget* parent = nullptr)
        : QToolButton(parent),
          _buttonStyle(Large),
          _largeButtonIconSize(64),
          _mediumButtonIconSize(48),
          _smallButtonIconSize(32),
          _maximumIconSize(64) {
        setButtonStyle(Large);
        setAutoRaise(true);
        setFocusPolicy(Qt::NoFocus);
    }
    ~RibbonToolButton() override = default;

    void setMaximumIconSize(int size) {
        _maximumIconSize = size;
        setButtonStyle(_buttonStyle);
    }

    int maximumIconSize() const { return _maximumIconSize; }

    void setButtonStyle(RibbonButtonStyle style) {
        _buttonStyle = style;
        int height;
        if (style == Small) {
            height = qMin(_smallButtonIconSize, _maximumIconSize);
            setIconSize(QSize(height, height));
            setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
            setStyleSheet(
                "RibbonToolButton::menu-indicator {"
                "subcontrol-origin: padding;"
                "subcontrol-position: right;"
                "right: -5px;"
                "}");
        } else if (style == Medium) {
            height = qMin(_mediumButtonIconSize, _maximumIconSize);
            setIconSize(QSize(height, height));
            setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
            setStyleSheet(
                "RibbonToolButton::menu-indicator {"
                "subcontrol-origin: padding;"
                "subcontrol-position: right;"
                "right: -5px;"
                "}");
        } else if (style == Large) {
            height = qMin(_largeButtonIconSize, _maximumIconSize);
            setIconSize(QSize(height, height));
            setToolButtonStyle(Qt::ToolButtonTextUnderIcon);
            setStyleSheet(
                "RibbonToolButton[popupMode=\"0\"]::menu-indicator {"
                "subcontrol-origin: padding;"
                "subcontrol-position: bottom;"
                "bottom: -5px;"
                "}"
                "RibbonToolButton[popupMode=\"2\"]::menu-indicator {"
                "subcontrol-origin: padding;"
                "subcontrol-position: bottom;"
                "bottom: -5px;"
                "}");
        }
    }

    RibbonButtonStyle buttonStyle() const { return _buttonStyle; }

    RibbonMenu* addRibbonMenu() {
        auto menu = new RibbonMenu();
        setMenu(menu);
        return menu;
    }
};
}  // namespace qtribbon

#endif  // PYQTRIBBON_TOOLBUTTON_HPP
