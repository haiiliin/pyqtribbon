//
// Created by hailin on 8/21/2024.
//

#ifndef PYQTRIBBON_CONSTANTS_HPP
#define PYQTRIBBON_CONSTANTS_HPP

#include <QColor>
#include <vector>

namespace qtribbon {

enum class RibbonCategoryStyle { Normal = 0, Context = 1 };

const RibbonCategoryStyle Normal = RibbonCategoryStyle::Normal;
const RibbonCategoryStyle Context = RibbonCategoryStyle::Context;

inline std::vector<QColor> contextColors = {
    QColor(201, 89, 156),  // 玫红
    QColor(242, 203, 29),  // 黄
    QColor(255, 157, 0),   // 橙
    QColor(14, 81, 167),   // 蓝
    QColor(228, 0, 69),    // 红
    QColor(67, 148, 0)     // 绿
};

enum class RibbonSpaceFindMode { ColumnWise = 0, RowWise = 1 };
const RibbonSpaceFindMode ColumnWise = RibbonSpaceFindMode::ColumnWise;
const RibbonSpaceFindMode RowWise = RibbonSpaceFindMode::RowWise;

enum class RibbonStyle { Default = 0, Debug = 1 };

const RibbonStyle Debug = RibbonStyle::Debug;
const RibbonStyle Default = RibbonStyle::Default;

enum class RibbonButtonStyle { Small = 0, Medium = 1, Large = 2 };

const RibbonButtonStyle Small = RibbonButtonStyle::Small;
const RibbonButtonStyle Medium = RibbonButtonStyle::Medium;
const RibbonButtonStyle Large = RibbonButtonStyle::Large;
}  // namespace qtribbon

#endif  // PYQTRIBBON_CONSTANTS_HPP
