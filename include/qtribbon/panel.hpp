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
#include "gallery.hpp"
#include "separator.hpp"
#include "toolbutton.hpp"

namespace qtribbon {

class RibbonPanelTitle : public QLabel {
   public:
    explicit RibbonPanelTitle(QWidget *parent = nullptr) : QLabel(parent) {}
    ~RibbonPanelTitle() {}
};

class RibbonGridLayoutManager {
   public:
    int rows;
    QVector<QVector<bool>> cells;

   public:
    explicit RibbonGridLayoutManager(int rows) : rows(rows) {
        cells.resize(rows);
        for (auto &row : cells) {
            row.fill(true);
        }
    }
    ~RibbonGridLayoutManager() {}

    std::pair<int, int> request_cells(int rowSpan = 1, int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise) {
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
    explicit RibbonPanelItemWidget(QWidget *parent = nullptr) : QFrame(parent) {
        QVBoxLayout *layout = new QVBoxLayout(this);
        layout->setContentsMargins(0, 0, 0, 0);
        layout->setSpacing(0);
        setLayout(layout);
    }
    ~RibbonPanelItemWidget() {}

    void addWidget(QWidget *widget) { layout()->addWidget(widget); }
};

class RibbonPanelOptionButton : public QToolButton {
   public:
    explicit RibbonPanelOptionButton(QWidget *parent = nullptr) : QToolButton(parent) {}
    ~RibbonPanelOptionButton() {}
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
    QList<QWidget *> _widgets = {};

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
            connect(_panelOption, SIGNAL(clicked(bool)), this, SIGNAL(panelOptionClicked(bool)));
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

    void setTitle(const QString &title) { _titleLabel->setText(title); }

    QString title() const { return _titleLabel->text(); }

    void setTitleHeight(int height) {
        _titleHeight = height;
        _titleWidget->setFixedHeight(height);
        _panelOption->setIconSize(QSize(height, height));
    }

    int titleHeight() const { return _titleHeight; }

    template <RibbonButtonStyle rowSpan = Small, int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise,
              Qt::AlignmentFlag alignment = Qt::AlignCenter, bool fixedHeight = false>
    QWidget *addWidget(QWidget *widget) {
        int rowSpan1 = defaultRowSpan(rowSpan);
        _widgets.append(widget);
        int row, col;
        std::tie(row, col) = _gridLayoutManager->request_cells(rowSpan1, colSpan, mode);
        int maximumHeight = rowHeight() * rowSpan1 + _actionsLayout->verticalSpacing() * (rowSpan1 - 2);
        widget->setMaximumHeight(maximumHeight);
        if (fixedHeight) widget->setFixedHeight(std::max(int(fixedHeight * maximumHeight), int(0.4 * maximumHeight)));
        RibbonPanelItemWidget *item = new RibbonPanelItemWidget(this);
        item->addWidget(widget);
        _actionsLayout->addWidget(item, row, col, rowSpan1, colSpan, alignment);
        return widget;
    }
    template <int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise, Qt::AlignmentFlag alignment = Qt::AlignCenter,
              bool fixedHeight = false>
    QWidget *addSmallWidget(QWidget *widget) {
        return addWidget<Small, colSpan, mode, alignment, fixedHeight>(widget);
    }
    template <int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise, Qt::AlignmentFlag alignment = Qt::AlignCenter,
              bool fixedHeight = false>
    QWidget *addMediumWidget(QWidget *widget) {
        return addWidget<Medium, colSpan, mode, alignment, fixedHeight>(widget);
    }
    template <int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise, Qt::AlignmentFlag alignment = Qt::AlignCenter,
              bool fixedHeight = false>
    QWidget *addLargeWidget(QWidget *widget) {
        return addWidget<Large, colSpan, mode, alignment, fixedHeight>(widget);
    }

    void removeWidget(QWidget *widget) { _actionsLayout->removeWidget(widget); }

    QWidget *widget(int index) { return _widgets.at(index); }

    QList<QWidget *> widgets() { return _widgets; }

    template <RibbonButtonStyle rowSpan = Small, int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise,
              Qt::AlignmentFlag alignment = Qt::AlignCenter, bool fixedHeight = false>
    RibbonToolButton *addButton(QString text = "", QIcon icon = QIcon(), bool showText = true,
                                QKeySequence shortcut = QKeySequence(), QString tooltip = "", QString statusTip = "",
                                bool checkable = false) {
        RibbonToolButton *button = new RibbonToolButton(this);
        button->setButtonStyle(rowSpan);
        if (!text.isEmpty()) button->setText(text);
        if (!icon.isNull()) button->setIcon(icon);
        if (!shortcut.isEmpty()) button->setShortcut(shortcut);
        if (!tooltip.isEmpty()) button->setToolTip(tooltip);
        if (!statusTip.isEmpty()) button->setStatusTip(statusTip);
        if (!showText) button->setToolButtonStyle(Qt::ToolButtonIconOnly);
        button->setCheckable(checkable);
        addWidget<rowSpan, colSpan, mode, alignment, fixedHeight>(button);
        return button;
    }
    template <int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise, Qt::AlignmentFlag alignment = Qt::AlignCenter,
              bool fixedHeight = false>
    RibbonToolButton *addSmallButton(QString text = "", QIcon icon = QIcon(), bool showText = true,
                                     QKeySequence shortcut = QKeySequence(), QString tooltip = "",
                                     QString statusTip = "", bool checkable = false) {
        return addButton<Small, colSpan, mode, alignment, fixedHeight>(text, icon, showText, shortcut, tooltip,
                                                                       statusTip, checkable);
    }
    template <int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise, Qt::AlignmentFlag alignment = Qt::AlignCenter,
              bool fixedHeight = false>
    RibbonToolButton *addMediumButton(QString text = "", QIcon icon = QIcon(), bool showText = true,
                                      QKeySequence shortcut = QKeySequence(), QString tooltip = "",
                                      QString statusTip = "", bool checkable = false) {
        return addButton<Medium, colSpan, mode, alignment, fixedHeight>(text, icon, showText, shortcut, tooltip,
                                                                        statusTip, checkable);
    }
    template <int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise, Qt::AlignmentFlag alignment = Qt::AlignCenter,
              bool fixedHeight = false>
    RibbonToolButton *addLargeButton(QString text = "", QIcon icon = QIcon(), bool showText = true,
                                     QKeySequence shortcut = QKeySequence(), QString tooltip = "",
                                     QString statusTip = "", bool checkable = false) {
        return addButton<Large, colSpan, mode, alignment, fixedHeight>(text, icon, showText, shortcut, tooltip,
                                                                       statusTip, checkable);
    }

    template <RibbonButtonStyle rowSpan = Small, int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise,
              Qt::AlignmentFlag alignment = Qt::AlignCenter, bool fixedHeight = false>
    RibbonToolButton *addToggleButton(QString text = "", QIcon icon = QIcon(), bool showText = true,
                                      QKeySequence shortcut = QKeySequence(), QString tooltip = "",
                                      QString statusTip = "") {
        return addButton<rowSpan, colSpan, mode, alignment, fixedHeight>(text, icon, showText, shortcut, tooltip,
                                                                         statusTip, true);
    }
    template <int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise, Qt::AlignmentFlag alignment = Qt::AlignCenter,
              bool fixedHeight = false>
    RibbonToolButton *addSmallToggleButton(QString text = "", QIcon icon = QIcon(), bool showText = true,
                                           QKeySequence shortcut = QKeySequence(), QString tooltip = "",
                                           QString statusTip = "") {
        return addToggleButton<Small, colSpan, mode, alignment, fixedHeight>(text, icon, showText, shortcut, tooltip,
                                                                             statusTip);
    }
    template <int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise, Qt::AlignmentFlag alignment = Qt::AlignCenter,
              bool fixedHeight = false>
    RibbonToolButton *addMediumToggleButton(QString text = "", QIcon icon = QIcon(), bool showText = true,
                                            QKeySequence shortcut = QKeySequence(), QString tooltip = "",
                                            QString statusTip = "") {
        return addToggleButton<Medium, colSpan, mode, alignment, fixedHeight>(text, icon, showText, shortcut, tooltip,
                                                                              statusTip);
    }
    template <int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise, Qt::AlignmentFlag alignment = Qt::AlignCenter,
              bool fixedHeight = false>
    RibbonToolButton *addLargeToggleButton(QString text = "", QIcon icon = QIcon(), bool showText = true,
                                           QKeySequence shortcut = QKeySequence(), QString tooltip = "",
                                           QString statusTip = "") {
        return addToggleButton<Large, colSpan, mode, alignment, fixedHeight>(text, icon, showText, shortcut, tooltip,
                                                                             statusTip);
    }

    template <RibbonButtonStyle rowSpan = Large, int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise,
              Qt::AlignmentFlag alignment = Qt::AlignCenter, bool fixedHeight = false>
    RibbonSeparator *addSeparator(Qt::Orientation orientation = Qt::Vertical, int width = 6) {
        RibbonSeparator *separator = new RibbonSeparator(orientation, width);
        addWidget<rowSpan, colSpan, mode, alignment, fixedHeight>(separator);
        return separator;
    }
    template <RibbonButtonStyle rowSpan = Large, int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise,
              Qt::AlignmentFlag alignment = Qt::AlignCenter, bool fixedHeight = false>
    RibbonSeparator *addHorizontalSeparator(int height = 6) {
        return addSeparator<rowSpan, colSpan, mode, alignment, fixedHeight>(Qt::Horizontal, height);
    }
    template <RibbonButtonStyle rowSpan = Large, int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise,
              Qt::AlignmentFlag alignment = Qt::AlignCenter, bool fixedHeight = false>
    RibbonSeparator *addVerticalSeparator(int width = 6) {
        return addSeparator<rowSpan, colSpan, mode, alignment, fixedHeight>(Qt::Vertical, width);
    }

    template <RibbonButtonStyle rowSpan = Small, int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise,
              Qt::AlignmentFlag alignment = Qt::AlignCenter, bool fixedHeight = false>
    RibbonGallery *addGallery(int minimumWidth = 800, bool popupHideOnClick = false) {
        RibbonGallery *gallery = new RibbonGallery(minimumWidth, popupHideOnClick, this);
        int rowSpan1 = defaultRowSpan(Large);
        int maximumHeight = rowHeight() * rowSpan1 + _actionsLayout->verticalSpacing() * (rowSpan1 - 2);
        gallery->setFixedHeight(maximumHeight);
        addWidget<rowSpan, colSpan, mode, alignment, fixedHeight>(gallery);
        return gallery;
    }
    template <int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise, Qt::AlignmentFlag alignment = Qt::AlignCenter,
              bool fixedHeight = false>
    RibbonGallery *addSmallGallery(int minimumWidth = 800, bool popupHideOnClick = false) {
        return addGallery<Small, colSpan, mode, alignment, fixedHeight>(minimumWidth, popupHideOnClick);
    }
    template <int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise, Qt::AlignmentFlag alignment = Qt::AlignCenter,
              bool fixedHeight = false>
    RibbonGallery *addMediumGallery(int minimumWidth = 800, bool popupHideOnClick = false) {
        return addGallery<Medium, colSpan, mode, alignment, fixedHeight>(minimumWidth, popupHideOnClick);
    }
    template <int colSpan = 1, RibbonSpaceFindMode mode = ColumnWise, Qt::AlignmentFlag alignment = Qt::AlignCenter,
              bool fixedHeight = false>
    RibbonGallery *addLargeGallery(int minimumWidth = 800, bool popupHideOnClick = false) {
        return addGallery<Large, colSpan, mode, alignment, fixedHeight>(minimumWidth, popupHideOnClick);
    }
};

}  // namespace qtribbon

#endif  // QTRIBBON_PANEL_HPP
