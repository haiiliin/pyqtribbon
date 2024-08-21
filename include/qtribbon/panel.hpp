//
// Created by hailin on 8/21/2024.
//

#ifndef QTRIBBON_PANEL_HPP
#define QTRIBBON_PANEL_HPP

#include <QApplication>
#include <QDebug>
#include <QFrame>
#include <QGridLayout>
#include <QIcon>
#include <QLabel>
#include <QMap>
#include <QSignalMapper>
#include <QSize>
#include <QToolButton>
#include <QVBoxLayout>
#include <QVariant>
#include <QWidget>

#include "constants.hpp"

namespace qtribbon {

class RibbonPanelTitle : public QLabel {
   public:
    RibbonPanelTitle(QWidget *parent = nullptr) : QLabel(parent) {}
};

class RibbonGridLayoutManager {
   public:
    int rows;
    QVector<QVector<bool>> cells;

   public:
    RibbonGridLayoutManager(int rows) : rows(rows) {
        cells.resize(rows);
        for (auto &row : cells) {
            row.fill(true);
        }
    }

    std::pair<int, int> requestCells(int rowSpan = 1, int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise) {
        if (rowSpan > rows) {
            throw std::invalid_argument("RowSpan is too large");
        }
        if (mode == ColumnWise) {
            for (int row = 0; row < cells.size() - rowSpan + 1; ++row) {
                for (int col = 0; col < cells[0].size() - colSpan + 1; ++col) {
                    bool allTrue = true;
                    for (int i = row; i < row + rowSpan; ++i) {
                        for (int j = col; j < col + colSpan; ++j) {
                            if (!cells[i][j]) {
                                allTrue = false;
                                break;
                            }
                        }
                        if (!allTrue) break;
                    }
                    if (allTrue) {
                        for (int i = row; i < row + rowSpan; ++i) {
                            for (int j = col; j < col + colSpan; ++j) cells[i][j] = false;
                        }
                        return std::make_pair(row, col);
                    }
                }
            }
        } else {
            for (int col = 0; col < cells[0].size(); ++col) {
                bool allTrue = true;
                for (int i = 0; i < rows; ++i) {
                    if (!cells[i][col]) {
                        allTrue = false;
                        break;
                    }
                }
                if (allTrue) {
                    if (cells[0].size() - col < colSpan) {
                        for (int i = 0; i < rows; ++i) cells[i].resize(colSpan - (cells[0].size() - col), true);
                    }
                    for (int i = 0; i < rows; ++i) cells[i][col] = false;

                    return std::make_pair(0, col);
                }
            }
        }
        int cols = cells[0].size();
        int colSpan1 = colSpan;
        bool allTrue = true;
        for (int i = 0; i < rows; ++i) {
            if (!cells[i][cols - 1]) {
                allTrue = false;
                break;
            }
        }
        if (allTrue) {
            cols--;
            colSpan1--;
        }
        for (int i = 0; i < rows; ++i) {
            cells[i].resize(cols + colSpan1, true);
            for (int j = cols; j < cols + colSpan; ++j) cells[i][j] = false;
        }
        return std::make_pair(0, cols);
    }
};

class RibbonPanelItemWidget : public QFrame {
   public:
    RibbonPanelItemWidget(QWidget *parent = nullptr) : QFrame(parent) {
        QVBoxLayout *layout = new QVBoxLayout(this);
        layout->setContentsMargins(0, 0, 0, 0);
        layout->setSpacing(0);
        setLayout(layout);
    }

    void addWidget(QWidget *widget) { layout()->addWidget(widget); }
};

class RibbonPanelOptionButton : public QToolButton {
   public:
    RibbonPanelOptionButton(QWidget *parent = nullptr) : QToolButton(parent) {}
};

class RibbonPanel : public QFrame {
    Q_OBJECT

   private:
    QVBoxLayout *_mainLayout;
    RibbonGridLayoutManager *_gridLayoutManager;
    QWidget *_titleWidget;
    RibbonPanelTitle *_titleLabel;
    RibbonPanelOptionButton *_panelOption = nullptr;
    QGridLayout *_actionsLayout;

    int _maxRows = 6;
    int _largeRows = 6;
    int _mediumRows = 3;
    int _smallRows = 2;
    bool _showPanelOptionButton;
    int _titleHeight;

   signals:
    void panelOptionClicked(bool);

   public:
    explicit RibbonPanel(QWidget *parent = nullptr) : RibbonPanel("", 6, true, parent) {}
    explicit RibbonPanel(const QString &title = "", int maxRows = 6, bool showPanelOptionButton = true,
                         QWidget *parent = nullptr)
        : QFrame(parent), _maxRows(maxRows), _showPanelOptionButton(showPanelOptionButton) {
        // Main Layout
        _mainLayout = new QVBoxLayout(this);
        _mainLayout->setContentsMargins(5, 2, 5, 2);
        _mainLayout->setSpacing(5);

        // Actions Layout
        _actionsLayout = new QGridLayout();
        _actionsLayout->setContentsMargins(5, 0, 5, 0);
        _actionsLayout->setSpacing(0);
        _mainLayout->addLayout(_actionsLayout, 1);

        // Title Layout
        _titleWidget = new QWidget(this);
        _titleWidget->setFixedHeight(_titleHeight);
        QHBoxLayout *_titleLayout = new QHBoxLayout(_titleWidget);
        _titleLayout->setContentsMargins(0, 0, 0, 0);
        _titleLayout->setSpacing(5);
        _titleLabel = new RibbonPanelTitle(this);
        _titleLabel->setText(title);
        _titleLabel->setAlignment(Qt::AlignCenter);
        _titleLayout->addWidget(_titleLabel, 1);

        // Panel Option Button
        if (showPanelOptionButton) {
            _panelOption = new RibbonPanelOptionButton(this);
            _panelOption->setAutoRaise(true);
            _panelOption->setIcon(QIcon("path/to/icon.png"));  // Update the path to your icon
            _panelOption->setIconSize(QSize(_titleHeight, _titleHeight));
            _panelOption->setToolTip("Panel options");
            connect(_panelOption, &QToolButton::clicked, [this]() { emit panelOptionClicked(true); });
            _titleLayout->addWidget(_panelOption, 0);
        }

        _mainLayout->addWidget(_titleWidget, 0);
    }

    ~RibbonPanel() {
        delete _gridLayoutManager;
        delete _mainLayout;
        delete _titleWidget;
        delete _titleLabel;
        if (_showPanelOptionButton) delete _panelOption;
        delete _actionsLayout;
    }

    int maximumRows() const { return _maxRows; }

    int largeRows() const { return _largeRows; }

    int mediumRows() const { return _mediumRows; }

    int smallRows() const { return _smallRows; }

    void setMaximumRows(int maxRows) {
        _maxRows = maxRows;
        _largeRows = maxRows;
        _mediumRows = std::max(static_cast<int>(round(maxRows / 2.0)), 1);
        _smallRows = std::max(static_cast<int>(round(maxRows / 3.0)), 1);
    }

    void setLargeRows(int rows) {
        assert(rows <= _maxRows && "Invalid number of rows");
        _largeRows = rows;
    }

    void setMediumRows(int rows) {
        assert(rows > 0 && rows <= _maxRows && "Invalid number of rows");
        _mediumRows = rows;
    }

    void setSmallRows(int rows) {
        assert(rows > 0 && rows <= _maxRows && "Invalid number of rows");
        _smallRows = rows;
    }

    int defaultRowSpan(RibbonButtonStyle rowSpan) const {
        switch (rowSpan) {
            case Large:
                return _largeRows;
            case Medium:
                return _mediumRows;
            case Small:
                return _smallRows;
            default:
                throw std::invalid_argument("Invalid row span");
        }
    }

    RibbonPanelOptionButton *panelOptionButton() const { return _panelOption; }

    void setPanelOptionToolTip(const QString &text) { _panelOption->setToolTip(text); }

    int rowHeight() const {
        return static_cast<int>((this->size().height() - _mainLayout->contentsMargins().top() -
                                 _mainLayout->contentsMargins().bottom() - _mainLayout->spacing() -
                                 _titleWidget->height() - _actionsLayout->contentsMargins().top() -
                                 _actionsLayout->contentsMargins().bottom() -
                                 _actionsLayout->verticalSpacing() * (_gridLayoutManager->rows - 1)) /
                                _gridLayoutManager->rows);
    }

    // The addWidget, removeWidget, widget, widgets, addButton, addSeparator, addGallery methods
    // are not included because they involve more complex logic and interactions with other classes.

    void setTitle(const QString &title) { _titleLabel->setText(title); }

    QString title() const { return _titleLabel->text(); }

    void setTitleHeight(int height) {
        _titleHeight = height;
        _titleWidget->setFixedHeight(height);
        _panelOption->setIconSize(QSize(height, height));
    }

    int titleHeight() const { return _titleHeight; }
};

}  // namespace qtribbon

#endif  // QTRIBBON_PANEL_HPP
