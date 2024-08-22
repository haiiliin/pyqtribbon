//
// Created by hailin on 8/21/2024.
//

#ifndef QTRIBBON_SEPARATOR_HPP
#define QTRIBBON_SEPARATOR_HPP

#include <QFrame>
#include <QPainter>
#include <QPen>
#include <QSizePolicy>

namespace qtribbon {

class RibbonSeparator : public QFrame {
    Q_OBJECT

   private:
    int _topMargins = 4;
    int _bottomMargins = 4;
    int _leftMargins = 4;
    int _rightMargins = 4;
    Qt::Orientation _orientation;
    int _width;

   public:
    explicit RibbonSeparator(QWidget *parent = nullptr) : RibbonSeparator(Qt::Vertical, 6, parent) {}
    explicit RibbonSeparator(Qt::Orientation orientation = Qt::Vertical, int width = 6, QWidget *parent = nullptr)
        : QFrame(parent), _orientation(orientation), _width(width) {
        if (orientation == Qt::Horizontal) {
            this->setFixedHeight(width);
            this->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Expanding);
        } else {
            this->setFixedWidth(width);
            this->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Preferred);
        }
    }
    ~RibbonSeparator() override = default;

    void setTopBottomMargins(int top, int bottom) {
        _topMargins = top;
        _bottomMargins = bottom;
    }

    void paintEvent(QPaintEvent *event) override {
        QPainter painter(this);
        QPen pen;
        pen.setColor(Qt::gray);
        painter.setPen(pen);
        if (_orientation == Qt::Vertical) {
            int x1 = this->rect().center().x();
            painter.drawLine(QPoint(x1, this->rect().top() + _topMargins),
                             QPoint(x1, this->rect().bottom() - _bottomMargins));
        } else {
            int y1 = this->rect().center().y();
            painter.drawLine(QPoint(this->rect().left() + _leftMargins, y1),
                             QPoint(this->rect().right() - _rightMargins, y1));
        }
    }
};

class RibbonHorizontalSeparator : public RibbonSeparator {
    Q_OBJECT

   public:
    explicit RibbonHorizontalSeparator(int width = 6, QWidget *parent = nullptr)
        : RibbonSeparator(Qt::Horizontal, width, parent) {}
    ~RibbonHorizontalSeparator() override = default;
};

class RibbonVerticalSeparator : public RibbonSeparator {
    Q_OBJECT

   public:
    explicit RibbonVerticalSeparator(int width = 6, QWidget *parent = nullptr)
        : RibbonSeparator(Qt::Vertical, width, parent) {}
    ~RibbonVerticalSeparator() override = default;
};
}  // namespace qtribbon

#endif  // QTRIBBON_SEPARATOR_HPP
