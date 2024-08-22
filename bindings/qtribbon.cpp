// File: qtribbon/constants.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <functional>
#include <qtribbon/constants.hpp>   // qtribbon::RibbonButtonStyle
#include <qtribbon/constants.hpp>   // qtribbon::RibbonCategoryStyle
#include <qtribbon/constants.hpp>   // qtribbon::RibbonSpaceFindMode
#include <qtribbon/constants.hpp>   // qtribbon::RibbonStyle
#include <qtribbon/gallery.hpp>     // qtribbon::RibbonGallery
#include <qtribbon/gallery.hpp>     // qtribbon::RibbonGalleryButton
#include <qtribbon/gallery.hpp>     // qtribbon::RibbonGalleryListWidget
#include <qtribbon/gallery.hpp>     // qtribbon::RibbonGalleryPopupListWidget
#include <qtribbon/gallery.hpp>     // qtribbon::RibbonPopupWidget
#include <qtribbon/menu.hpp>        // qtribbon::RibbonMenu
#include <qtribbon/menu.hpp>        // qtribbon::RibbonPermanentMenu
#include <qtribbon/panel.hpp>       // qtribbon::RibbonPanelTitle
#include <qtribbon/separator.hpp>   // qtribbon::RibbonHorizontalSeparator
#include <qtribbon/separator.hpp>   // qtribbon::RibbonSeparator
#include <qtribbon/separator.hpp>   // qtribbon::RibbonVerticalSeparator
#include <qtribbon/toolbutton.hpp>  // qtribbon::RibbonToolButton
#include <sstream>                  // __str__
#include <string>

#ifndef BINDER_PYBIND11_TYPE_CASTER
#define BINDER_PYBIND11_TYPE_CASTER
PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>, false)
PYBIND11_DECLARE_HOLDER_TYPE(T, T *, false)
PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>)
#endif

void bind_qtribbon_constants(std::function<pybind11::module &(std::string const &namespace_)> &M) {
    // qtribbon::RibbonCategoryStyle file:qtribbon/constants.hpp line:
    pybind11::enum_<qtribbon::RibbonCategoryStyle>(M("qtribbon"), "RibbonCategoryStyle", "")
        .value("Normal", qtribbon::RibbonCategoryStyle::Normal)
        .value("Context", qtribbon::RibbonCategoryStyle::Context);

    ;

    // qtribbon::RibbonSpaceFindMode file:qtribbon/constants.hpp line:
    pybind11::enum_<qtribbon::RibbonSpaceFindMode>(M("qtribbon"), "RibbonSpaceFindMode", "")
        .value("ColumnWise", qtribbon::RibbonSpaceFindMode::ColumnWise)
        .value("RowWise", qtribbon::RibbonSpaceFindMode::RowWise);

    ;

    // qtribbon::RibbonStyle file:qtribbon/constants.hpp line:
    pybind11::enum_<qtribbon::RibbonStyle>(M("qtribbon"), "RibbonStyle", "")
        .value("Default", qtribbon::RibbonStyle::Default)
        .value("Debug", qtribbon::RibbonStyle::Debug);

    ;

    // qtribbon::RibbonButtonStyle file:qtribbon/constants.hpp line:
    pybind11::enum_<qtribbon::RibbonButtonStyle>(M("qtribbon"), "RibbonButtonStyle", "")
        .value("Small", qtribbon::RibbonButtonStyle::Small)
        .value("Medium", qtribbon::RibbonButtonStyle::Medium)
        .value("Large", qtribbon::RibbonButtonStyle::Large);

    ;

    {  // qtribbon::RibbonMenu file:qtribbon/menu.hpp line:
        pybind11::class_<qtribbon::RibbonMenu, std::shared_ptr<qtribbon::RibbonMenu>> cl(M("qtribbon"), "RibbonMenu",
                                                                                         "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonMenu(); }));
        cl.def(pybind11::init([](qtribbon::RibbonMenu const &o) { return new qtribbon::RibbonMenu(o); }));
        cl.def(
            "assign",
            (class qtribbon::RibbonMenu & (qtribbon::RibbonMenu::*)(const class qtribbon::RibbonMenu &)) &
                qtribbon::RibbonMenu::operator=,
            "C++: qtribbon::RibbonMenu::operator=(const class qtribbon::RibbonMenu &) --> class qtribbon::RibbonMenu &",
            pybind11::return_value_policy::automatic, pybind11::arg(""));
    }
    {  // qtribbon::RibbonPermanentMenu file:qtribbon/menu.hpp line:
        pybind11::class_<qtribbon::RibbonPermanentMenu, std::shared_ptr<qtribbon::RibbonPermanentMenu>,
                         qtribbon::RibbonMenu>
            cl(M("qtribbon"), "RibbonPermanentMenu", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonPermanentMenu(); }), "doc");
        cl.def(pybind11::init<int *>(), pybind11::arg("parent"));

        cl.def(pybind11::init([](const int &a0) { return new qtribbon::RibbonPermanentMenu(a0); }), "doc",
               pybind11::arg("title"));
        cl.def(pybind11::init<const int &, int *>(), pybind11::arg("title"), pybind11::arg("parent"));

        cl.def(pybind11::init([]() { return new qtribbon::RibbonPermanentMenu(); }));
        cl.def(pybind11::init(
            [](qtribbon::RibbonPermanentMenu const &o) { return new qtribbon::RibbonPermanentMenu(o); }));
        cl.def("hideEvent", (void(qtribbon::RibbonPermanentMenu::*)(int *)) & qtribbon::RibbonPermanentMenu::hideEvent,
               "C++: qtribbon::RibbonPermanentMenu::hideEvent(int *) --> void", pybind11::arg("event"));
        cl.def("assign",
               (class qtribbon::RibbonPermanentMenu &
                (qtribbon::RibbonPermanentMenu::*)(const class qtribbon::RibbonPermanentMenu &)) &
                   qtribbon::RibbonPermanentMenu::operator=,
               "C++: qtribbon::RibbonPermanentMenu::operator=(const class qtribbon::RibbonPermanentMenu &) --> class "
               "qtribbon::RibbonPermanentMenu &",
               pybind11::return_value_policy::automatic, pybind11::arg(""));
    }
    {  // qtribbon::RibbonSeparator file:qtribbon/separator.hpp line:
        pybind11::class_<qtribbon::RibbonSeparator, std::shared_ptr<qtribbon::RibbonSeparator>> cl(
            M("qtribbon"), "RibbonSeparator", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonSeparator(); }), "doc");
        cl.def(pybind11::init<int *>(), pybind11::arg("parent"));

        cl.def(pybind11::init([]() { return new qtribbon::RibbonSeparator(); }), "doc");
        cl.def(pybind11::init([](int const &a0) { return new qtribbon::RibbonSeparator(a0); }), "doc",
               pybind11::arg("orientation"));
        cl.def(pybind11::init([](int const &a0, int const &a1) { return new qtribbon::RibbonSeparator(a0, a1); }),
               "doc", pybind11::arg("orientation"), pybind11::arg("width"));
        cl.def(pybind11::init<int, int, int *>(), pybind11::arg("orientation"), pybind11::arg("width"),
               pybind11::arg("parent"));

        cl.def(pybind11::init([]() { return new qtribbon::RibbonSeparator(); }));
        cl.def(pybind11::init([](qtribbon::RibbonSeparator const &o) { return new qtribbon::RibbonSeparator(o); }));
        cl.def("setTopBottomMargins",
               (void(qtribbon::RibbonSeparator::*)(int, int)) & qtribbon::RibbonSeparator::setTopBottomMargins,
               "C++: qtribbon::RibbonSeparator::setTopBottomMargins(int, int) --> void", pybind11::arg("top"),
               pybind11::arg("bottom"));
        cl.def("paintEvent", (void(qtribbon::RibbonSeparator::*)(int *)) & qtribbon::RibbonSeparator::paintEvent,
               "C++: qtribbon::RibbonSeparator::paintEvent(int *) --> void", pybind11::arg("event"));
        cl.def("assign",
               (class qtribbon::RibbonSeparator &
                (qtribbon::RibbonSeparator::*)(const class qtribbon::RibbonSeparator &)) &
                   qtribbon::RibbonSeparator::operator=,
               "C++: qtribbon::RibbonSeparator::operator=(const class qtribbon::RibbonSeparator &) --> class "
               "qtribbon::RibbonSeparator &",
               pybind11::return_value_policy::automatic, pybind11::arg(""));
    }
    {  // qtribbon::RibbonHorizontalSeparator file:qtribbon/separator.hpp line:
        pybind11::class_<qtribbon::RibbonHorizontalSeparator, std::shared_ptr<qtribbon::RibbonHorizontalSeparator>,
                         qtribbon::RibbonSeparator>
            cl(M("qtribbon"), "RibbonHorizontalSeparator", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonHorizontalSeparator(); }));
        cl.def(pybind11::init(
            [](qtribbon::RibbonHorizontalSeparator const &o) { return new qtribbon::RibbonHorizontalSeparator(o); }));
    }
    {  // qtribbon::RibbonVerticalSeparator file:qtribbon/separator.hpp line:
        pybind11::class_<qtribbon::RibbonVerticalSeparator, std::shared_ptr<qtribbon::RibbonVerticalSeparator>,
                         qtribbon::RibbonSeparator>
            cl(M("qtribbon"), "RibbonVerticalSeparator", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonVerticalSeparator(); }));
    }
    {  // qtribbon::RibbonToolButton file:qtribbon/toolbutton.hpp line:
        pybind11::class_<qtribbon::RibbonToolButton, std::shared_ptr<qtribbon::RibbonToolButton>> cl(
            M("qtribbon"), "RibbonToolButton", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonToolButton(); }), "doc");
        cl.def(pybind11::init<int *>(), pybind11::arg("parent"));

        cl.def(pybind11::init([]() { return new qtribbon::RibbonToolButton(); }));
        cl.def(pybind11::init([](qtribbon::RibbonToolButton const &o) { return new qtribbon::RibbonToolButton(o); }));
        cl.def("setMaximumIconSize",
               (void(qtribbon::RibbonToolButton::*)(int)) & qtribbon::RibbonToolButton::setMaximumIconSize,
               "C++: qtribbon::RibbonToolButton::setMaximumIconSize(int) --> void", pybind11::arg("size"));
        cl.def("maximumIconSize",
               (int(qtribbon::RibbonToolButton::*)() const) & qtribbon::RibbonToolButton::maximumIconSize,
               "C++: qtribbon::RibbonToolButton::maximumIconSize() const --> int");
        cl.def("setButtonStyle",
               (void(qtribbon::RibbonToolButton::*)(enum qtribbon::RibbonButtonStyle)) &
                   qtribbon::RibbonToolButton::setButtonStyle,
               "C++: qtribbon::RibbonToolButton::setButtonStyle(enum qtribbon::RibbonButtonStyle) --> void",
               pybind11::arg("style"));
        cl.def("buttonStyle",
               (enum qtribbon::RibbonButtonStyle(qtribbon::RibbonToolButton::*)() const) &
                   qtribbon::RibbonToolButton::buttonStyle,
               "C++: qtribbon::RibbonToolButton::buttonStyle() const --> enum qtribbon::RibbonButtonStyle");
        cl.def("addRibbonMenu",
               (class qtribbon::RibbonMenu * (qtribbon::RibbonToolButton::*)()) &
                   qtribbon::RibbonToolButton::addRibbonMenu,
               "C++: qtribbon::RibbonToolButton::addRibbonMenu() --> class qtribbon::RibbonMenu *",
               pybind11::return_value_policy::automatic);
    }
    {  // qtribbon::RibbonPopupWidget file:qtribbon/gallery.hpp line:
        pybind11::class_<qtribbon::RibbonPopupWidget, std::shared_ptr<qtribbon::RibbonPopupWidget>> cl(
            M("qtribbon"), "RibbonPopupWidget", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonPopupWidget(); }));
        cl.def(pybind11::init([](qtribbon::RibbonPopupWidget const &o) { return new qtribbon::RibbonPopupWidget(o); }));
    }
    {  // qtribbon::RibbonGalleryListWidget file:qtribbon/gallery.hpp line:
        pybind11::class_<qtribbon::RibbonGalleryListWidget, std::shared_ptr<qtribbon::RibbonGalleryListWidget>> cl(
            M("qtribbon"), "RibbonGalleryListWidget", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonGalleryListWidget(); }));
        cl.def(pybind11::init(
            [](qtribbon::RibbonGalleryListWidget const &o) { return new qtribbon::RibbonGalleryListWidget(o); }));
    }
    {  // qtribbon::RibbonGalleryButton file:qtribbon/gallery.hpp line:
        pybind11::class_<qtribbon::RibbonGalleryButton, std::shared_ptr<qtribbon::RibbonGalleryButton>> cl(
            M("qtribbon"), "RibbonGalleryButton", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonGalleryButton(); }));
        cl.def(pybind11::init(
            [](qtribbon::RibbonGalleryButton const &o) { return new qtribbon::RibbonGalleryButton(o); }));
    }
    {  // qtribbon::RibbonGalleryPopupListWidget file:qtribbon/gallery.hpp line:
        pybind11::class_<qtribbon::RibbonGalleryPopupListWidget,
                         std::shared_ptr<qtribbon::RibbonGalleryPopupListWidget>, qtribbon::RibbonGalleryListWidget>
            cl(M("qtribbon"), "RibbonGalleryPopupListWidget", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonGalleryPopupListWidget(); }));
        cl.def(pybind11::init([](qtribbon::RibbonGalleryPopupListWidget const &o) {
            return new qtribbon::RibbonGalleryPopupListWidget(o);
        }));
    }
    {  // qtribbon::RibbonGallery file:qtribbon/gallery.hpp line:
        pybind11::class_<qtribbon::RibbonGallery, std::shared_ptr<qtribbon::RibbonGallery>> cl(M("qtribbon"),
                                                                                               "RibbonGallery", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonGallery(); }), "doc");
        cl.def(pybind11::init<int *>(), pybind11::arg("parent"));

        cl.def(pybind11::init([]() { return new qtribbon::RibbonGallery(); }), "doc");
        cl.def(pybind11::init([](int const &a0) { return new qtribbon::RibbonGallery(a0); }), "doc",
               pybind11::arg("minimumWidth"));
        cl.def(pybind11::init([](int const &a0, bool const &a1) { return new qtribbon::RibbonGallery(a0, a1); }), "doc",
               pybind11::arg("minimumWidth"), pybind11::arg("popupHideOnClick"));
        cl.def(pybind11::init<int, bool, int *>(), pybind11::arg("minimumWidth"), pybind11::arg("popupHideOnClick"),
               pybind11::arg("parent"));

        cl.def(pybind11::init([]() { return new qtribbon::RibbonGallery(); }));
        cl.def(pybind11::init([](qtribbon::RibbonGallery const &o) { return new qtribbon::RibbonGallery(o); }));
        cl.def("_handlePopupAction",
               (void(qtribbon::RibbonGallery::*)(int *) const) & qtribbon::RibbonGallery::_handlePopupAction,
               "C++: qtribbon::RibbonGallery::_handlePopupAction(int *) const --> void", pybind11::arg("action"));
        cl.def("resizeEvent", (void(qtribbon::RibbonGallery::*)(int *)) & qtribbon::RibbonGallery::resizeEvent,
               "C++: qtribbon::RibbonGallery::resizeEvent(int *) --> void", pybind11::arg("event"));
        cl.def(
            "popupMenu",
            (class qtribbon::RibbonPermanentMenu * (qtribbon::RibbonGallery::*)()) & qtribbon::RibbonGallery::popupMenu,
            "C++: qtribbon::RibbonGallery::popupMenu() --> class qtribbon::RibbonPermanentMenu *",
            pybind11::return_value_policy::automatic);
        cl.def("showPopup", (void(qtribbon::RibbonGallery::*)()) & qtribbon::RibbonGallery::showPopup,
               "C++: qtribbon::RibbonGallery::showPopup() --> void");
        cl.def("hidePopupWidget", (void(qtribbon::RibbonGallery::*)()) & qtribbon::RibbonGallery::hidePopupWidget,
               "C++: qtribbon::RibbonGallery::hidePopupWidget() --> void");
        cl.def("popupWindowSize", (int(qtribbon::RibbonGallery::*)()) & qtribbon::RibbonGallery::popupWindowSize,
               "C++: qtribbon::RibbonGallery::popupWindowSize() --> int");
        cl.def("setPopupWindowSize",
               (void(qtribbon::RibbonGallery::*)(int)) & qtribbon::RibbonGallery::setPopupWindowSize,
               "C++: qtribbon::RibbonGallery::setPopupWindowSize(int) --> void", pybind11::arg("size"));
        cl.def("setSelectedButton", (void(qtribbon::RibbonGallery::*)()) & qtribbon::RibbonGallery::setSelectedButton,
               "C++: qtribbon::RibbonGallery::setSelectedButton() --> void");
        cl.def("_addWidget", (void(qtribbon::RibbonGallery::*)(int *)) & qtribbon::RibbonGallery::_addWidget,
               "C++: qtribbon::RibbonGallery::_addWidget(int *) --> void", pybind11::arg("widget"));
        cl.def("_addPopupWidget", (void(qtribbon::RibbonGallery::*)(int *)) & qtribbon::RibbonGallery::_addPopupWidget,
               "C++: qtribbon::RibbonGallery::_addPopupWidget(int *) --> void", pybind11::arg("widget"));
        cl.def("setPopupHideOnClick",
               (void(qtribbon::RibbonGallery::*)(bool)) & qtribbon::RibbonGallery::setPopupHideOnClick,
               "C++: qtribbon::RibbonGallery::setPopupHideOnClick(bool) --> void", pybind11::arg("popupHideOnClick"));
        cl.def(
            "addButton",
            [](qtribbon::RibbonGallery &o, const int &a0) -> qtribbon::RibbonToolButton * { return o.addButton(a0); },
            "", pybind11::return_value_policy::automatic, pybind11::arg("text"));
        cl.def(
            "addButton",
            [](qtribbon::RibbonGallery &o, const int &a0, const int &a1) -> qtribbon::RibbonToolButton * {
                return o.addButton(a0, a1);
            },
            "", pybind11::return_value_policy::automatic, pybind11::arg("text"), pybind11::arg("icon"));
        cl.def(
            "addButton",
            [](qtribbon::RibbonGallery &o, const int &a0, const int &a1,
               const int &a2) -> qtribbon::RibbonToolButton * { return o.addButton(a0, a1, a2); },
            "", pybind11::return_value_policy::automatic, pybind11::arg("text"), pybind11::arg("icon"),
            pybind11::arg("shortcut"));
        cl.def(
            "addButton",
            [](qtribbon::RibbonGallery &o, const int &a0, const int &a1, const int &a2,
               const int &a3) -> qtribbon::RibbonToolButton * { return o.addButton(a0, a1, a2, a3); },
            "", pybind11::return_value_policy::automatic, pybind11::arg("text"), pybind11::arg("icon"),
            pybind11::arg("shortcut"), pybind11::arg("tooltip"));
        cl.def(
            "addButton",
            [](qtribbon::RibbonGallery &o, const int &a0, const int &a1, const int &a2, const int &a3,
               const int &a4) -> qtribbon::RibbonToolButton * { return o.addButton(a0, a1, a2, a3, a4); },
            "", pybind11::return_value_policy::automatic, pybind11::arg("text"), pybind11::arg("icon"),
            pybind11::arg("shortcut"), pybind11::arg("tooltip"), pybind11::arg("statusTip"));
        cl.def("addButton",
               (class qtribbon::RibbonToolButton *
                (qtribbon::RibbonGallery::*)(const int &, const int &, const int &, const int &, const int &, bool)) &
                   qtribbon::RibbonGallery::addButton,
               "C++: qtribbon::RibbonGallery::addButton(const int &, const int &, const int &, const int &, const int "
               "&, bool) --> class qtribbon::RibbonToolButton *",
               pybind11::return_value_policy::automatic, pybind11::arg("text"), pybind11::arg("icon"),
               pybind11::arg("shortcut"), pybind11::arg("tooltip"), pybind11::arg("statusTip"),
               pybind11::arg("checkable"));
        cl.def(
            "addToggleButton",
            [](qtribbon::RibbonGallery &o, const int &a0) -> qtribbon::RibbonToolButton * {
                return o.addToggleButton(a0);
            },
            "", pybind11::return_value_policy::automatic, pybind11::arg("text"));
        cl.def(
            "addToggleButton",
            [](qtribbon::RibbonGallery &o, const int &a0, const int &a1) -> qtribbon::RibbonToolButton * {
                return o.addToggleButton(a0, a1);
            },
            "", pybind11::return_value_policy::automatic, pybind11::arg("text"), pybind11::arg("icon"));
        cl.def(
            "addToggleButton",
            [](qtribbon::RibbonGallery &o, const int &a0, const int &a1,
               const int &a2) -> qtribbon::RibbonToolButton * { return o.addToggleButton(a0, a1, a2); },
            "", pybind11::return_value_policy::automatic, pybind11::arg("text"), pybind11::arg("icon"),
            pybind11::arg("shortcut"));
        cl.def(
            "addToggleButton",
            [](qtribbon::RibbonGallery &o, const int &a0, const int &a1, const int &a2,
               const int &a3) -> qtribbon::RibbonToolButton * { return o.addToggleButton(a0, a1, a2, a3); },
            "", pybind11::return_value_policy::automatic, pybind11::arg("text"), pybind11::arg("icon"),
            pybind11::arg("shortcut"), pybind11::arg("tooltip"));
        cl.def("addToggleButton",
               (class qtribbon::RibbonToolButton *
                (qtribbon::RibbonGallery::*)(const int &, const int &, const int &, const int &, const int &)) &
                   qtribbon::RibbonGallery::addToggleButton,
               "C++: qtribbon::RibbonGallery::addToggleButton(const int &, const int &, const int &, const int &, "
               "const int &) --> class qtribbon::RibbonToolButton *",
               pybind11::return_value_policy::automatic, pybind11::arg("text"), pybind11::arg("icon"),
               pybind11::arg("shortcut"), pybind11::arg("tooltip"), pybind11::arg("statusTip"));
    }
    {  // qtribbon::RibbonPanelTitle file:qtribbon/panel.hpp line:
        pybind11::class_<qtribbon::RibbonPanelTitle, std::shared_ptr<qtribbon::RibbonPanelTitle>> cl(
            M("qtribbon"), "RibbonPanelTitle", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonPanelTitle(); }), "doc");
        cl.def(pybind11::init<int *>(), pybind11::arg("parent"));

        cl.def(pybind11::init([]() { return new qtribbon::RibbonPanelTitle(); }));
        cl.def(pybind11::init([](qtribbon::RibbonPanelTitle const &o) { return new qtribbon::RibbonPanelTitle(o); }));
    }
}

// File: qtribbon/panel.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <functional>
#include <qtribbon/category.hpp>   // qtribbon::RibbonCategory
#include <qtribbon/category.hpp>   // qtribbon::RibbonCategoryLayoutButton
#include <qtribbon/category.hpp>   // qtribbon::RibbonCategoryLayoutWidget
#include <qtribbon/category.hpp>   // qtribbon::RibbonCategoryScrollArea
#include <qtribbon/category.hpp>   // qtribbon::RibbonCategoryScrollAreaContents
#include <qtribbon/category.hpp>   // qtribbon::RibbonContextCategories
#include <qtribbon/category.hpp>   // qtribbon::RibbonContextCategory
#include <qtribbon/category.hpp>   // qtribbon::RibbonNormalCategory
#include <qtribbon/constants.hpp>  // qtribbon::RibbonButtonStyle
#include <qtribbon/constants.hpp>  // qtribbon::RibbonCategoryStyle
#include <qtribbon/constants.hpp>  // qtribbon::RibbonSpaceFindMode
#include <qtribbon/panel.hpp>      // qtribbon::RibbonGridLayoutManager
#include <qtribbon/panel.hpp>      // qtribbon::RibbonPanel
#include <qtribbon/panel.hpp>      // qtribbon::RibbonPanelItemWidget
#include <qtribbon/panel.hpp>      // qtribbon::RibbonPanelOptionButton
#include <sstream>                 // __str__
#include <string>
#include <utility>  // std::pair

#ifndef BINDER_PYBIND11_TYPE_CASTER
#define BINDER_PYBIND11_TYPE_CASTER
PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>, false)
PYBIND11_DECLARE_HOLDER_TYPE(T, T *, false)
PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>)
#endif

// qtribbon::RibbonCategory file:qtribbon/category.hpp line:
struct PyCallBack_qtribbon_RibbonCategory : public qtribbon::RibbonCategory {
    using qtribbon::RibbonCategory::RibbonCategory;

    void setCategoryStyle(enum qtribbon::RibbonCategoryStyle a0) override {
        pybind11::gil_scoped_acquire gil;
        pybind11::function overload =
            pybind11::get_overload(static_cast<const qtribbon::RibbonCategory *>(this), "setCategoryStyle");
        if (overload) {
            auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
            if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
                static pybind11::detail::override_caster_t<void> caster;
                return pybind11::detail::cast_ref<void>(std::move(o), caster);
            }
            return pybind11::detail::cast_safe<void>(std::move(o));
        }
        return RibbonCategory::setCategoryStyle(a0);
    }
};

// qtribbon::RibbonNormalCategory file:qtribbon/category.hpp line:
struct PyCallBack_qtribbon_RibbonNormalCategory : public qtribbon::RibbonNormalCategory {
    using qtribbon::RibbonNormalCategory::RibbonNormalCategory;

    void setCategoryStyle(enum qtribbon::RibbonCategoryStyle a0) override {
        pybind11::gil_scoped_acquire gil;
        pybind11::function overload =
            pybind11::get_overload(static_cast<const qtribbon::RibbonNormalCategory *>(this), "setCategoryStyle");
        if (overload) {
            auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
            if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
                static pybind11::detail::override_caster_t<void> caster;
                return pybind11::detail::cast_ref<void>(std::move(o), caster);
            }
            return pybind11::detail::cast_safe<void>(std::move(o));
        }
        return RibbonCategory::setCategoryStyle(a0);
    }
};

// qtribbon::RibbonContextCategory file:qtribbon/category.hpp line:
struct PyCallBack_qtribbon_RibbonContextCategory : public qtribbon::RibbonContextCategory {
    using qtribbon::RibbonContextCategory::RibbonContextCategory;

    void setCategoryStyle(enum qtribbon::RibbonCategoryStyle a0) override {
        pybind11::gil_scoped_acquire gil;
        pybind11::function overload =
            pybind11::get_overload(static_cast<const qtribbon::RibbonContextCategory *>(this), "setCategoryStyle");
        if (overload) {
            auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
            if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
                static pybind11::detail::override_caster_t<void> caster;
                return pybind11::detail::cast_ref<void>(std::move(o), caster);
            }
            return pybind11::detail::cast_safe<void>(std::move(o));
        }
        return RibbonCategory::setCategoryStyle(a0);
    }
};

void bind_qtribbon_panel(std::function<pybind11::module &(std::string const &namespace_)> &M) {
    {  // qtribbon::RibbonGridLayoutManager file:qtribbon/panel.hpp line:
        pybind11::class_<qtribbon::RibbonGridLayoutManager, std::shared_ptr<qtribbon::RibbonGridLayoutManager>> cl(
            M("qtribbon"), "RibbonGridLayoutManager", "");
        cl.def(pybind11::init<int>(), pybind11::arg("rows"));

        cl.def(pybind11::init(
            [](qtribbon::RibbonGridLayoutManager const &o) { return new qtribbon::RibbonGridLayoutManager(o); }));
        cl.def_readwrite("rows", &qtribbon::RibbonGridLayoutManager::rows);
        cl.def_readwrite("cells", &qtribbon::RibbonGridLayoutManager::cells);
        cl.def(
            "request_cells",
            [](qtribbon::RibbonGridLayoutManager &o) -> std::pair<int, int> { return o.request_cells(); }, "");
        cl.def(
            "request_cells",
            [](qtribbon::RibbonGridLayoutManager &o, int const &a0) -> std::pair<int, int> {
                return o.request_cells(a0);
            },
            "", pybind11::arg("rowSpan"));
        cl.def(
            "request_cells",
            [](qtribbon::RibbonGridLayoutManager &o, int const &a0, int const &a1) -> std::pair<int, int> {
                return o.request_cells(a0, a1);
            },
            "", pybind11::arg("rowSpan"), pybind11::arg("colSpan"));
        cl.def("request_cells",
               (struct std::pair<int, int>(qtribbon::RibbonGridLayoutManager::*)(int, int,
                                                                                 enum qtribbon::RibbonSpaceFindMode)) &
                   qtribbon::RibbonGridLayoutManager::request_cells,
               "C++: qtribbon::RibbonGridLayoutManager::request_cells(int, int, enum qtribbon::RibbonSpaceFindMode) "
               "--> struct std::pair<int, int>",
               pybind11::arg("rowSpan"), pybind11::arg("colSpan"), pybind11::arg("mode"));
    }
    {  // qtribbon::RibbonPanelItemWidget file:qtribbon/panel.hpp line:
        pybind11::class_<qtribbon::RibbonPanelItemWidget, std::shared_ptr<qtribbon::RibbonPanelItemWidget>> cl(
            M("qtribbon"), "RibbonPanelItemWidget", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonPanelItemWidget(); }), "doc");
        cl.def(pybind11::init<int *>(), pybind11::arg("parent"));

        cl.def(pybind11::init([]() { return new qtribbon::RibbonPanelItemWidget(); }));
        cl.def(pybind11::init(
            [](qtribbon::RibbonPanelItemWidget const &o) { return new qtribbon::RibbonPanelItemWidget(o); }));
        cl.def("addWidget",
               (void(qtribbon::RibbonPanelItemWidget::*)(int *)) & qtribbon::RibbonPanelItemWidget::addWidget,
               "C++: qtribbon::RibbonPanelItemWidget::addWidget(int *) --> void", pybind11::arg("widget"));
    }
    {  // qtribbon::RibbonPanelOptionButton file:qtribbon/panel.hpp line:
        pybind11::class_<qtribbon::RibbonPanelOptionButton, std::shared_ptr<qtribbon::RibbonPanelOptionButton>> cl(
            M("qtribbon"), "RibbonPanelOptionButton", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonPanelOptionButton(); }), "doc");
        cl.def(pybind11::init<int *>(), pybind11::arg("parent"));

        cl.def(pybind11::init([]() { return new qtribbon::RibbonPanelOptionButton(); }));
        cl.def(pybind11::init(
            [](qtribbon::RibbonPanelOptionButton const &o) { return new qtribbon::RibbonPanelOptionButton(o); }));
    }
    {  // qtribbon::RibbonPanel file:qtribbon/panel.hpp line:
        pybind11::class_<qtribbon::RibbonPanel, std::shared_ptr<qtribbon::RibbonPanel>> cl(M("qtribbon"), "RibbonPanel",
                                                                                           "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonPanel(); }), "doc");
        cl.def(pybind11::init<int *>(), pybind11::arg("parent"));

        cl.def(pybind11::init([](const int &a0) { return new qtribbon::RibbonPanel(a0); }), "doc",
               pybind11::arg("title"));
        cl.def(pybind11::init([](const int &a0, int const &a1) { return new qtribbon::RibbonPanel(a0, a1); }), "doc",
               pybind11::arg("title"), pybind11::arg("maxRows"));
        cl.def(pybind11::init(
                   [](const int &a0, int const &a1, bool const &a2) { return new qtribbon::RibbonPanel(a0, a1, a2); }),
               "doc", pybind11::arg("title"), pybind11::arg("maxRows"), pybind11::arg("showPanelOptionButton"));
        cl.def(pybind11::init<const int &, int, bool, int *>(), pybind11::arg("title"), pybind11::arg("maxRows"),
               pybind11::arg("showPanelOptionButton"), pybind11::arg("parent"));

        cl.def("maximumRows", (int(qtribbon::RibbonPanel::*)() const) & qtribbon::RibbonPanel::maximumRows,
               "C++: qtribbon::RibbonPanel::maximumRows() const --> int");
        cl.def("largeRows", (int(qtribbon::RibbonPanel::*)() const) & qtribbon::RibbonPanel::largeRows,
               "C++: qtribbon::RibbonPanel::largeRows() const --> int");
        cl.def("mediumRows", (int(qtribbon::RibbonPanel::*)() const) & qtribbon::RibbonPanel::mediumRows,
               "C++: qtribbon::RibbonPanel::mediumRows() const --> int");
        cl.def("smallRows", (int(qtribbon::RibbonPanel::*)() const) & qtribbon::RibbonPanel::smallRows,
               "C++: qtribbon::RibbonPanel::smallRows() const --> int");
        cl.def("setMaximumRows", (void(qtribbon::RibbonPanel::*)(int)) & qtribbon::RibbonPanel::setMaximumRows,
               "C++: qtribbon::RibbonPanel::setMaximumRows(int) --> void", pybind11::arg("maxRows"));
        cl.def("setLargeRows", (void(qtribbon::RibbonPanel::*)(int)) & qtribbon::RibbonPanel::setLargeRows,
               "C++: qtribbon::RibbonPanel::setLargeRows(int) --> void", pybind11::arg("rows"));
        cl.def("setMediumRows", (void(qtribbon::RibbonPanel::*)(int)) & qtribbon::RibbonPanel::setMediumRows,
               "C++: qtribbon::RibbonPanel::setMediumRows(int) --> void", pybind11::arg("rows"));
        cl.def("setSmallRows", (void(qtribbon::RibbonPanel::*)(int)) & qtribbon::RibbonPanel::setSmallRows,
               "C++: qtribbon::RibbonPanel::setSmallRows(int) --> void", pybind11::arg("rows"));
        cl.def("defaultRowSpan",
               (int(qtribbon::RibbonPanel::*)(enum qtribbon::RibbonButtonStyle) const) &
                   qtribbon::RibbonPanel::defaultRowSpan,
               "C++: qtribbon::RibbonPanel::defaultRowSpan(enum qtribbon::RibbonButtonStyle) const --> int",
               pybind11::arg("rowSpan"));
        cl.def("panelOptionButton",
               (class qtribbon::RibbonPanelOptionButton * (qtribbon::RibbonPanel::*)() const) &
                   qtribbon::RibbonPanel::panelOptionButton,
               "C++: qtribbon::RibbonPanel::panelOptionButton() const --> class qtribbon::RibbonPanelOptionButton *",
               pybind11::return_value_policy::automatic);
        cl.def("setPanelOptionToolTip",
               (void(qtribbon::RibbonPanel::*)(const int &)) & qtribbon::RibbonPanel::setPanelOptionToolTip,
               "C++: qtribbon::RibbonPanel::setPanelOptionToolTip(const int &) --> void", pybind11::arg("text"));
        cl.def("rowHeight", (int(qtribbon::RibbonPanel::*)() const) & qtribbon::RibbonPanel::rowHeight,
               "C++: qtribbon::RibbonPanel::rowHeight() const --> int");
        cl.def("setTitle", (void(qtribbon::RibbonPanel::*)(const int &)) & qtribbon::RibbonPanel::setTitle,
               "C++: qtribbon::RibbonPanel::setTitle(const int &) --> void", pybind11::arg("title"));
        cl.def("title", (int(qtribbon::RibbonPanel::*)() const) & qtribbon::RibbonPanel::title,
               "C++: qtribbon::RibbonPanel::title() const --> int");
        cl.def("setTitleHeight", (void(qtribbon::RibbonPanel::*)(int)) & qtribbon::RibbonPanel::setTitleHeight,
               "C++: qtribbon::RibbonPanel::setTitleHeight(int) --> void", pybind11::arg("height"));
        cl.def("titleHeight", (int(qtribbon::RibbonPanel::*)() const) & qtribbon::RibbonPanel::titleHeight,
               "C++: qtribbon::RibbonPanel::titleHeight() const --> int");
        cl.def("removeWidget", (void(qtribbon::RibbonPanel::*)(int *)) & qtribbon::RibbonPanel::removeWidget,
               "C++: qtribbon::RibbonPanel::removeWidget(int *) --> void", pybind11::arg("widget"));
        cl.def("widget", (int *(qtribbon::RibbonPanel::*)(int)) & qtribbon::RibbonPanel::widget,
               "C++: qtribbon::RibbonPanel::widget(int) --> int *", pybind11::return_value_policy::automatic,
               pybind11::arg("index"));
        cl.def("widgets", (int(qtribbon::RibbonPanel::*)()) & qtribbon::RibbonPanel::widgets,
               "C++: qtribbon::RibbonPanel::widgets() --> int");
    }
    {  // qtribbon::RibbonCategoryLayoutButton file:qtribbon/category.hpp line:
        pybind11::class_<qtribbon::RibbonCategoryLayoutButton, std::shared_ptr<qtribbon::RibbonCategoryLayoutButton>>
            cl(M("qtribbon"), "RibbonCategoryLayoutButton", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonCategoryLayoutButton(); }));
        cl.def(pybind11::init(
            [](qtribbon::RibbonCategoryLayoutButton const &o) { return new qtribbon::RibbonCategoryLayoutButton(o); }));
    }
    {  // qtribbon::RibbonCategoryScrollArea file:qtribbon/category.hpp line:
        pybind11::class_<qtribbon::RibbonCategoryScrollArea, std::shared_ptr<qtribbon::RibbonCategoryScrollArea>> cl(
            M("qtribbon"), "RibbonCategoryScrollArea", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonCategoryScrollArea(); }));
        cl.def(pybind11::init(
            [](qtribbon::RibbonCategoryScrollArea const &o) { return new qtribbon::RibbonCategoryScrollArea(o); }));
    }
    {  // qtribbon::RibbonCategoryScrollAreaContents file:qtribbon/category.hpp line:
        pybind11::class_<qtribbon::RibbonCategoryScrollAreaContents,
                         std::shared_ptr<qtribbon::RibbonCategoryScrollAreaContents>>
            cl(M("qtribbon"), "RibbonCategoryScrollAreaContents", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonCategoryScrollAreaContents(); }));
        cl.def(pybind11::init([](qtribbon::RibbonCategoryScrollAreaContents const &o) {
            return new qtribbon::RibbonCategoryScrollAreaContents(o);
        }));
    }
    {  // qtribbon::RibbonCategoryLayoutWidget file:qtribbon/category.hpp line:
        pybind11::class_<qtribbon::RibbonCategoryLayoutWidget, std::shared_ptr<qtribbon::RibbonCategoryLayoutWidget>>
            cl(M("qtribbon"), "RibbonCategoryLayoutWidget", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonCategoryLayoutWidget(); }), "doc");
        cl.def(pybind11::init<int *>(), pybind11::arg("parent"));

        cl.def(
            "paintEvent",
            (void(qtribbon::RibbonCategoryLayoutWidget::*)(int *)) & qtribbon::RibbonCategoryLayoutWidget::paintEvent,
            "C++: qtribbon::RibbonCategoryLayoutWidget::paintEvent(int *) --> void", pybind11::arg("event"));
        cl.def(
            "resizeEvent",
            (void(qtribbon::RibbonCategoryLayoutWidget::*)(int *)) & qtribbon::RibbonCategoryLayoutWidget::resizeEvent,
            "C++: qtribbon::RibbonCategoryLayoutWidget::resizeEvent(int *) --> void", pybind11::arg("event"));
        cl.def("autoSetScrollButtonsVisible",
               (void(qtribbon::RibbonCategoryLayoutWidget::*)()) &
                   qtribbon::RibbonCategoryLayoutWidget::autoSetScrollButtonsVisible,
               "C++: qtribbon::RibbonCategoryLayoutWidget::autoSetScrollButtonsVisible() --> void");
        cl.def("scrollPrevious",
               (void(qtribbon::RibbonCategoryLayoutWidget::*)()) & qtribbon::RibbonCategoryLayoutWidget::scrollPrevious,
               "C++: qtribbon::RibbonCategoryLayoutWidget::scrollPrevious() --> void");
        cl.def("scrollNext",
               (void(qtribbon::RibbonCategoryLayoutWidget::*)()) & qtribbon::RibbonCategoryLayoutWidget::scrollNext,
               "C++: qtribbon::RibbonCategoryLayoutWidget::scrollNext() --> void");
        cl.def("addWidget",
               (void(qtribbon::RibbonCategoryLayoutWidget::*)(int *)) & qtribbon::RibbonCategoryLayoutWidget::addWidget,
               "C++: qtribbon::RibbonCategoryLayoutWidget::addWidget(int *) --> void", pybind11::arg("widget"));
        cl.def(
            "removeWidget",
            (void(qtribbon::RibbonCategoryLayoutWidget::*)(int *)) & qtribbon::RibbonCategoryLayoutWidget::removeWidget,
            "C++: qtribbon::RibbonCategoryLayoutWidget::removeWidget(int *) --> void", pybind11::arg("widget"));
        cl.def(
            "takeWidget",
            (int *(qtribbon::RibbonCategoryLayoutWidget::*)(int *)) & qtribbon::RibbonCategoryLayoutWidget::takeWidget,
            "C++: qtribbon::RibbonCategoryLayoutWidget::takeWidget(int *) --> int *",
            pybind11::return_value_policy::automatic, pybind11::arg("widget"));
    }
    {  // qtribbon::RibbonCategory file:qtribbon/category.hpp line:
        pybind11::class_<qtribbon::RibbonCategory, std::shared_ptr<qtribbon::RibbonCategory>,
                         PyCallBack_qtribbon_RibbonCategory, qtribbon::RibbonCategoryLayoutWidget>
            cl(M("qtribbon"), "RibbonCategory", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonCategory(); },
                              []() { return new PyCallBack_qtribbon_RibbonCategory(); }),
               "doc");
        cl.def(pybind11::init<int *>(), pybind11::arg("parent"));

        cl.def(pybind11::init([](int const &a0) { return new qtribbon::RibbonCategory(a0); },
                              [](int const &a0) { return new PyCallBack_qtribbon_RibbonCategory(a0); }),
               "doc");
        cl.def(pybind11::init(
                   [](int const &a0, enum qtribbon::RibbonCategoryStyle const &a1) {
                       return new qtribbon::RibbonCategory(a0, a1);
                   },
                   [](int const &a0, enum qtribbon::RibbonCategoryStyle const &a1) {
                       return new PyCallBack_qtribbon_RibbonCategory(a0, a1);
                   }),
               "doc");
        cl.def(pybind11::init([](int const &a0, enum qtribbon::RibbonCategoryStyle const &a1,
                                 int const &a2) { return new qtribbon::RibbonCategory(a0, a1, a2); },
                              [](int const &a0, enum qtribbon::RibbonCategoryStyle const &a1, int const &a2) {
                                  return new PyCallBack_qtribbon_RibbonCategory(a0, a1, a2);
                              }),
               "doc");
        cl.def(pybind11::init<int, enum qtribbon::RibbonCategoryStyle, int, int *>(), pybind11::arg("title"),
               pybind11::arg("style"), pybind11::arg("color"), pybind11::arg("parent"));

        cl.def("setMaximumRows", (void(qtribbon::RibbonCategory::*)(int)) & qtribbon::RibbonCategory::setMaximumRows,
               "C++: qtribbon::RibbonCategory::setMaximumRows(int) --> void", pybind11::arg("rows"));
        cl.def("title", (int(qtribbon::RibbonCategory::*)() const) & qtribbon::RibbonCategory::title,
               "C++: qtribbon::RibbonCategory::title() const --> int");
        cl.def("setCategoryStyle",
               (void(qtribbon::RibbonCategory::*)(enum qtribbon::RibbonCategoryStyle)) &
                   qtribbon::RibbonCategory::setCategoryStyle,
               "C++: qtribbon::RibbonCategory::setCategoryStyle(enum qtribbon::RibbonCategoryStyle) --> void",
               pybind11::arg("style"));
        cl.def("categoryStyle",
               (enum qtribbon::RibbonCategoryStyle(qtribbon::RibbonCategory::*)() const) &
                   qtribbon::RibbonCategory::categoryStyle,
               "C++: qtribbon::RibbonCategory::categoryStyle() const --> enum qtribbon::RibbonCategoryStyle");
        cl.def("addPanel",
               (class qtribbon::RibbonPanel * (qtribbon::RibbonCategory::*)(const int &, bool)) &
                   qtribbon::RibbonCategory::addPanel,
               "C++: qtribbon::RibbonCategory::addPanel(const int &, bool) --> class qtribbon::RibbonPanel *",
               pybind11::return_value_policy::automatic, pybind11::arg("title"),
               pybind11::arg("showPanelOptionButton"));
        cl.def("removePanel", (void(qtribbon::RibbonCategory::*)(const int &)) & qtribbon::RibbonCategory::removePanel,
               "C++: qtribbon::RibbonCategory::removePanel(const int &) --> void", pybind11::arg("title"));
        cl.def("takePanel",
               (class qtribbon::RibbonPanel * (qtribbon::RibbonCategory::*)(const int &)) &
                   qtribbon::RibbonCategory::takePanel,
               "C++: qtribbon::RibbonCategory::takePanel(const int &) --> class qtribbon::RibbonPanel *",
               pybind11::return_value_policy::automatic, pybind11::arg("title"));
        cl.def("panel",
               (class qtribbon::RibbonPanel * (qtribbon::RibbonCategory::*)(const int &)) &
                   qtribbon::RibbonCategory::panel,
               "C++: qtribbon::RibbonCategory::panel(const int &) --> class qtribbon::RibbonPanel *",
               pybind11::return_value_policy::automatic, pybind11::arg("title"));
        cl.def("panels", (int(qtribbon::RibbonCategory::*)()) & qtribbon::RibbonCategory::panels,
               "C++: qtribbon::RibbonCategory::panels() --> int");
    }
    {  // qtribbon::RibbonNormalCategory file:qtribbon/category.hpp line:
        pybind11::class_<qtribbon::RibbonNormalCategory, std::shared_ptr<qtribbon::RibbonNormalCategory>,
                         PyCallBack_qtribbon_RibbonNormalCategory, qtribbon::RibbonCategory>
            cl(M("qtribbon"), "RibbonNormalCategory", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonNormalCategory(); },
                              []() { return new PyCallBack_qtribbon_RibbonNormalCategory(); }));
    }
    {  // qtribbon::RibbonContextCategory file:qtribbon/category.hpp line:
        pybind11::class_<qtribbon::RibbonContextCategory, std::shared_ptr<qtribbon::RibbonContextCategory>,
                         PyCallBack_qtribbon_RibbonContextCategory, qtribbon::RibbonCategory>
            cl(M("qtribbon"), "RibbonContextCategory", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonContextCategory(); },
                              []() { return new PyCallBack_qtribbon_RibbonContextCategory(); }));
    }
    {  // qtribbon::RibbonContextCategories file:qtribbon/category.hpp line:
        pybind11::class_<qtribbon::RibbonContextCategories, std::shared_ptr<qtribbon::RibbonContextCategories>> cl(
            M("qtribbon"), "RibbonContextCategories", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonContextCategories(); }));
        cl.def(pybind11::init<int, int, int>(), pybind11::arg("name"), pybind11::arg("color"),
               pybind11::arg("categories"));

        cl.def("name", (int(qtribbon::RibbonContextCategories::*)() const) & qtribbon::RibbonContextCategories::name,
               "C++: qtribbon::RibbonContextCategories::name() const --> int");
        cl.def("setName",
               (void(qtribbon::RibbonContextCategories::*)(int)) & qtribbon::RibbonContextCategories::setName,
               "C++: qtribbon::RibbonContextCategories::setName(int) --> void", pybind11::arg("name"));
        cl.def("color", (int(qtribbon::RibbonContextCategories::*)() const) & qtribbon::RibbonContextCategories::color,
               "C++: qtribbon::RibbonContextCategories::color() const --> int");
        cl.def("setColor",
               (void(qtribbon::RibbonContextCategories::*)(int)) & qtribbon::RibbonContextCategories::setColor,
               "C++: qtribbon::RibbonContextCategories::setColor(int) --> void", pybind11::arg("color"));
    }
}

// File: qtribbon/tabbar.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <functional>
#include <qtribbon/category.hpp>     // qtribbon::RibbonCategory
#include <qtribbon/category.hpp>     // qtribbon::RibbonContextCategories
#include <qtribbon/category.hpp>     // qtribbon::RibbonContextCategory
#include <qtribbon/category.hpp>     // qtribbon::RibbonNormalCategory
#include <qtribbon/constants.hpp>    // qtribbon::RibbonCategoryStyle
#include <qtribbon/constants.hpp>    // qtribbon::RibbonStyle
#include <qtribbon/menu.hpp>         // qtribbon::RibbonMenu
#include <qtribbon/panel.hpp>        // qtribbon::RibbonPanel
#include <qtribbon/ribbonbar.hpp>    // qtribbon::RibbonBar
#include <qtribbon/ribbonbar.hpp>    // qtribbon::RibbonStackedWidget
#include <qtribbon/tabbar.hpp>       // qtribbon::RibbonTabBar
#include <qtribbon/titlewidget.hpp>  // qtribbon::RibbonApplicationButton
#include <qtribbon/titlewidget.hpp>  // qtribbon::RibbonTitleLabel
#include <qtribbon/titlewidget.hpp>  // qtribbon::RibbonTitleWidget
#include <sstream>                   // __str__
#include <string>

#ifndef BINDER_PYBIND11_TYPE_CASTER
#define BINDER_PYBIND11_TYPE_CASTER
PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>, false)
PYBIND11_DECLARE_HOLDER_TYPE(T, T *, false)
PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>)
#endif

void bind_qtribbon_tabbar(std::function<pybind11::module &(std::string const &namespace_)> &M) {
    {  // qtribbon::RibbonTabBar file:qtribbon/tabbar.hpp line:
        pybind11::class_<qtribbon::RibbonTabBar, std::shared_ptr<qtribbon::RibbonTabBar>> cl(M("qtribbon"),
                                                                                             "RibbonTabBar", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonTabBar(); }), "doc");
        cl.def(pybind11::init<int *>(), pybind11::arg("parent"));

        cl.def(pybind11::init([]() { return new qtribbon::RibbonTabBar(); }));
        cl.def(pybind11::init([](qtribbon::RibbonTabBar const &o) { return new qtribbon::RibbonTabBar(o); }));
        cl.def("indexOf", (int(qtribbon::RibbonTabBar::*)(const int &)) & qtribbon::RibbonTabBar::indexOf,
               "C++: qtribbon::RibbonTabBar::indexOf(const int &) --> int", pybind11::arg("tabName"));
        cl.def("tabTitles", (int(qtribbon::RibbonTabBar::*)()) & qtribbon::RibbonTabBar::tabTitles,
               "C++: qtribbon::RibbonTabBar::tabTitles() --> int");
        cl.def(
            "addTab", [](qtribbon::RibbonTabBar &o, const int &a0) -> int { return o.addTab(a0); }, "",
            pybind11::arg("text"));
        cl.def("addTab", (int(qtribbon::RibbonTabBar::*)(const int &, const int &)) & qtribbon::RibbonTabBar::addTab,
               "C++: qtribbon::RibbonTabBar::addTab(const int &, const int &) --> int", pybind11::arg("text"),
               pybind11::arg("color"));
        cl.def("addAssociatedTabs",
               (int(qtribbon::RibbonTabBar::*)(const int &, const int &, const int &)) &
                   qtribbon::RibbonTabBar::addAssociatedTabs,
               "C++: qtribbon::RibbonTabBar::addAssociatedTabs(const int &, const int &, const int &) --> int",
               pybind11::arg("name"), pybind11::arg("texts"), pybind11::arg("color"));
        cl.def("removeAssociatedTabs",
               (void(qtribbon::RibbonTabBar::*)(const int &)) & qtribbon::RibbonTabBar::removeAssociatedTabs,
               "C++: qtribbon::RibbonTabBar::removeAssociatedTabs(const int &) --> void", pybind11::arg("titles"));
        cl.def("currentTabColor", (int(qtribbon::RibbonTabBar::*)()) & qtribbon::RibbonTabBar::currentTabColor,
               "C++: qtribbon::RibbonTabBar::currentTabColor() --> int");
        cl.def("changeColor", (void(qtribbon::RibbonTabBar::*)(int)) & qtribbon::RibbonTabBar::changeColor,
               "C++: qtribbon::RibbonTabBar::changeColor(int) --> void", pybind11::arg("inx"));
    }
    {  // qtribbon::RibbonApplicationButton file:qtribbon/titlewidget.hpp line:
        pybind11::class_<qtribbon::RibbonApplicationButton, std::shared_ptr<qtribbon::RibbonApplicationButton>> cl(
            M("qtribbon"), "RibbonApplicationButton", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonApplicationButton(); }));
        cl.def(pybind11::init(
            [](qtribbon::RibbonApplicationButton const &o) { return new qtribbon::RibbonApplicationButton(o); }));
    }
    {  // qtribbon::RibbonTitleLabel file:qtribbon/titlewidget.hpp line:
        pybind11::class_<qtribbon::RibbonTitleLabel, std::shared_ptr<qtribbon::RibbonTitleLabel>> cl(
            M("qtribbon"), "RibbonTitleLabel", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonTitleLabel(); }));
        cl.def(pybind11::init([](qtribbon::RibbonTitleLabel const &o) { return new qtribbon::RibbonTitleLabel(o); }));
    }
    {  // qtribbon::RibbonTitleWidget file:qtribbon/titlewidget.hpp line:
        pybind11::class_<qtribbon::RibbonTitleWidget, std::shared_ptr<qtribbon::RibbonTitleWidget>> cl(
            M("qtribbon"), "RibbonTitleWidget", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonTitleWidget(); }), "doc");
        cl.def(pybind11::init<int *>(), pybind11::arg("parent"));

        cl.def(pybind11::init([](const int &a0) { return new qtribbon::RibbonTitleWidget(a0); }), "doc",
               pybind11::arg("title"));
        cl.def(pybind11::init<const int &, int *>(), pybind11::arg("title"), pybind11::arg("parent"));

        cl.def("applicationButton",
               (class qtribbon::RibbonApplicationButton * (qtribbon::RibbonTitleWidget::*)()) &
                   qtribbon::RibbonTitleWidget::applicationButton,
               "C++: qtribbon::RibbonTitleWidget::applicationButton() --> class qtribbon::RibbonApplicationButton *",
               pybind11::return_value_policy::automatic);
        cl.def("setApplicationIcon",
               (void(qtribbon::RibbonTitleWidget::*)(const int &)) & qtribbon::RibbonTitleWidget::setApplicationIcon,
               "C++: qtribbon::RibbonTitleWidget::setApplicationIcon(const int &) --> void", pybind11::arg("icon"));
        cl.def("addTitleWidget",
               (void(qtribbon::RibbonTitleWidget::*)(int *)) & qtribbon::RibbonTitleWidget::addTitleWidget,
               "C++: qtribbon::RibbonTitleWidget::addTitleWidget(int *) --> void", pybind11::arg("widget"));
        cl.def("insertTitleWidget",
               (void(qtribbon::RibbonTitleWidget::*)(int, int *)) & qtribbon::RibbonTitleWidget::insertTitleWidget,
               "C++: qtribbon::RibbonTitleWidget::insertTitleWidget(int, int *) --> void", pybind11::arg("index"),
               pybind11::arg("widget"));
        cl.def("removeTitleWidget",
               (void(qtribbon::RibbonTitleWidget::*)(int *)) & qtribbon::RibbonTitleWidget::removeTitleWidget,
               "C++: qtribbon::RibbonTitleWidget::removeTitleWidget(int *) --> void", pybind11::arg("widget"));
        cl.def(
            "tabBar",
            (class qtribbon::RibbonTabBar * (qtribbon::RibbonTitleWidget::*)()) & qtribbon::RibbonTitleWidget::tabBar,
            "C++: qtribbon::RibbonTitleWidget::tabBar() --> class qtribbon::RibbonTabBar *",
            pybind11::return_value_policy::automatic);
        cl.def("quickAccessToolBar",
               (int *(qtribbon::RibbonTitleWidget::*)()) & qtribbon::RibbonTitleWidget::quickAccessToolBar,
               "C++: qtribbon::RibbonTitleWidget::quickAccessToolBar() --> int *",
               pybind11::return_value_policy::automatic);
        cl.def("quickAccessButtons",
               (int(qtribbon::RibbonTitleWidget::*)()) & qtribbon::RibbonTitleWidget::quickAccessButtons,
               "C++: qtribbon::RibbonTitleWidget::quickAccessButtons() --> int");
        cl.def("addQuickAccessButton",
               (void(qtribbon::RibbonTitleWidget::*)(int *)) & qtribbon::RibbonTitleWidget::addQuickAccessButton,
               "C++: qtribbon::RibbonTitleWidget::addQuickAccessButton(int *) --> void", pybind11::arg("button"));
        cl.def("setQuickAccessButtonHeight",
               (void(qtribbon::RibbonTitleWidget::*)(int)) & qtribbon::RibbonTitleWidget::setQuickAccessButtonHeight,
               "C++: qtribbon::RibbonTitleWidget::setQuickAccessButtonHeight(int) --> void", pybind11::arg("height"));
        cl.def("title", (int(qtribbon::RibbonTitleWidget::*)()) & qtribbon::RibbonTitleWidget::title,
               "C++: qtribbon::RibbonTitleWidget::title() --> int");
        cl.def("setTitle", (void(qtribbon::RibbonTitleWidget::*)(const int &)) & qtribbon::RibbonTitleWidget::setTitle,
               "C++: qtribbon::RibbonTitleWidget::setTitle(const int &) --> void", pybind11::arg("title"));
        cl.def("rightToolBar", (int *(qtribbon::RibbonTitleWidget::*)()) & qtribbon::RibbonTitleWidget::rightToolBar,
               "C++: qtribbon::RibbonTitleWidget::rightToolBar() --> int *", pybind11::return_value_policy::automatic);
        cl.def("addRightToolButton",
               (void(qtribbon::RibbonTitleWidget::*)(int *)) & qtribbon::RibbonTitleWidget::addRightToolButton,
               "C++: qtribbon::RibbonTitleWidget::addRightToolButton(int *) --> void", pybind11::arg("button"));
        cl.def("setRightToolBarHeight",
               (void(qtribbon::RibbonTitleWidget::*)(int)) & qtribbon::RibbonTitleWidget::setRightToolBarHeight,
               "C++: qtribbon::RibbonTitleWidget::setRightToolBarHeight(int) --> void", pybind11::arg("height"));
        cl.def("helpRibbonButton",
               (int *(qtribbon::RibbonTitleWidget::*)()) & qtribbon::RibbonTitleWidget::helpRibbonButton,
               "C++: qtribbon::RibbonTitleWidget::helpRibbonButton() --> int *",
               pybind11::return_value_policy::automatic);
        cl.def("setHelpButtonIcon",
               (void(qtribbon::RibbonTitleWidget::*)(const int &)) & qtribbon::RibbonTitleWidget::setHelpButtonIcon,
               "C++: qtribbon::RibbonTitleWidget::setHelpButtonIcon(const int &) --> void", pybind11::arg("icon"));
        cl.def("removeHelpButton",
               (void(qtribbon::RibbonTitleWidget::*)()) & qtribbon::RibbonTitleWidget::removeHelpButton,
               "C++: qtribbon::RibbonTitleWidget::removeHelpButton() --> void");
        cl.def("setCollapseButtonIcon",
               (void(qtribbon::RibbonTitleWidget::*)(const int &)) & qtribbon::RibbonTitleWidget::setCollapseButtonIcon,
               "C++: qtribbon::RibbonTitleWidget::setCollapseButtonIcon(const int &) --> void", pybind11::arg("icon"));
        cl.def("removeCollapseButton",
               (void(qtribbon::RibbonTitleWidget::*)()) & qtribbon::RibbonTitleWidget::removeCollapseButton,
               "C++: qtribbon::RibbonTitleWidget::removeCollapseButton() --> void");
        cl.def("collapseRibbonButton",
               (int *(qtribbon::RibbonTitleWidget::*)()) & qtribbon::RibbonTitleWidget::collapseRibbonButton,
               "C++: qtribbon::RibbonTitleWidget::collapseRibbonButton() --> int *",
               pybind11::return_value_policy::automatic);
        cl.def("setTitleWidgetHeight",
               (void(qtribbon::RibbonTitleWidget::*)(int)) & qtribbon::RibbonTitleWidget::setTitleWidgetHeight,
               "C++: qtribbon::RibbonTitleWidget::setTitleWidgetHeight(int) --> void", pybind11::arg("height"));
        cl.def(
            "topLevelWidget", (int *(qtribbon::RibbonTitleWidget::*)()) & qtribbon::RibbonTitleWidget::topLevelWidget,
            "C++: qtribbon::RibbonTitleWidget::topLevelWidget() --> int *", pybind11::return_value_policy::automatic);
        cl.def("mousePressEvent",
               (void(qtribbon::RibbonTitleWidget::*)(int *)) & qtribbon::RibbonTitleWidget::mousePressEvent,
               "C++: qtribbon::RibbonTitleWidget::mousePressEvent(int *) --> void", pybind11::arg("event"));
        cl.def("mouseMoveEvent",
               (void(qtribbon::RibbonTitleWidget::*)(int *)) & qtribbon::RibbonTitleWidget::mouseMoveEvent,
               "C++: qtribbon::RibbonTitleWidget::mouseMoveEvent(int *) --> void", pybind11::arg("event"));
        cl.def("mouseDoubleClickEvent",
               (void(qtribbon::RibbonTitleWidget::*)(int *)) & qtribbon::RibbonTitleWidget::mouseDoubleClickEvent,
               "C++: qtribbon::RibbonTitleWidget::mouseDoubleClickEvent(int *) --> void", pybind11::arg("event"));
    }
    {  // qtribbon::RibbonStackedWidget file:qtribbon/ribbonbar.hpp line:
        pybind11::class_<qtribbon::RibbonStackedWidget, std::shared_ptr<qtribbon::RibbonStackedWidget>> cl(
            M("qtribbon"), "RibbonStackedWidget", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonStackedWidget(); }));
        cl.def(pybind11::init(
            [](qtribbon::RibbonStackedWidget const &o) { return new qtribbon::RibbonStackedWidget(o); }));
    }
    {  // qtribbon::RibbonBar file:qtribbon/ribbonbar.hpp line:
        pybind11::class_<qtribbon::RibbonBar, std::shared_ptr<qtribbon::RibbonBar>> cl(M("qtribbon"), "RibbonBar", "");
        cl.def(pybind11::init([]() { return new qtribbon::RibbonBar(); }), "doc");
        cl.def(pybind11::init<int *>(), pybind11::arg("parent"));

        cl.def(pybind11::init([](const int &a0) { return new qtribbon::RibbonBar(a0); }), "doc",
               pybind11::arg("title"));
        cl.def(pybind11::init([](const int &a0, int const &a1) { return new qtribbon::RibbonBar(a0, a1); }), "doc",
               pybind11::arg("title"), pybind11::arg("maxRows"));
        cl.def(pybind11::init<const int &, int, int *>(), pybind11::arg("title"), pybind11::arg("maxRows"),
               pybind11::arg("parent"));

        cl.def("autoHideRibbon", (bool(qtribbon::RibbonBar::*)() const) & qtribbon::RibbonBar::autoHideRibbon,
               "C++: qtribbon::RibbonBar::autoHideRibbon() const --> bool");
        cl.def("setAutoHideRibbon", (void(qtribbon::RibbonBar::*)(bool)) & qtribbon::RibbonBar::setAutoHideRibbon,
               "C++: qtribbon::RibbonBar::setAutoHideRibbon(bool) --> void", pybind11::arg("autoHide"));
        cl.def("eventFilter", (bool(qtribbon::RibbonBar::*)(int *, int *)) & qtribbon::RibbonBar::eventFilter,
               "C++: qtribbon::RibbonBar::eventFilter(int *, int *) --> bool", pybind11::arg("object"),
               pybind11::arg("event"));
        cl.def("setRibbonStyle",
               (void(qtribbon::RibbonBar::*)(enum qtribbon::RibbonStyle)) & qtribbon::RibbonBar::setRibbonStyle,
               "C++: qtribbon::RibbonBar::setRibbonStyle(enum qtribbon::RibbonStyle) --> void", pybind11::arg("style"));
        cl.def(
            "applicationOptionButton",
            (class qtribbon::RibbonApplicationButton * (qtribbon::RibbonBar::*)() const) &
                qtribbon::RibbonBar::applicationOptionButton,
            "C++: qtribbon::RibbonBar::applicationOptionButton() const --> class qtribbon::RibbonApplicationButton *",
            pybind11::return_value_policy::automatic);
        cl.def("setApplicationIcon",
               (void(qtribbon::RibbonBar::*)(const int &)) & qtribbon::RibbonBar::setApplicationIcon,
               "C++: qtribbon::RibbonBar::setApplicationIcon(const int &) --> void", pybind11::arg("icon"));
        cl.def("addTitleWidget", (void(qtribbon::RibbonBar::*)(int *)) & qtribbon::RibbonBar::addTitleWidget,
               "C++: qtribbon::RibbonBar::addTitleWidget(int *) --> void", pybind11::arg("widget"));
        cl.def("removeTitleWidget", (void(qtribbon::RibbonBar::*)(int *)) & qtribbon::RibbonBar::removeTitleWidget,
               "C++: qtribbon::RibbonBar::removeTitleWidget(int *) --> void", pybind11::arg("widget"));
        cl.def("insertTitleWidget", (void(qtribbon::RibbonBar::*)(int, int *)) & qtribbon::RibbonBar::insertTitleWidget,
               "C++: qtribbon::RibbonBar::insertTitleWidget(int, int *) --> void", pybind11::arg("index"),
               pybind11::arg("widget"));
        cl.def("addFileMenu",
               (class qtribbon::RibbonMenu * (qtribbon::RibbonBar::*)()) & qtribbon::RibbonBar::addFileMenu,
               "C++: qtribbon::RibbonBar::addFileMenu() --> class qtribbon::RibbonMenu *",
               pybind11::return_value_policy::automatic);
        cl.def("ribbonHeight", (int(qtribbon::RibbonBar::*)() const) & qtribbon::RibbonBar::ribbonHeight,
               "C++: qtribbon::RibbonBar::ribbonHeight() const --> int");
        cl.def("setRibbonHeight", (void(qtribbon::RibbonBar::*)(int)) & qtribbon::RibbonBar::setRibbonHeight,
               "C++: qtribbon::RibbonBar::setRibbonHeight(int) --> void", pybind11::arg("height"));
        cl.def("tabBar",
               (class qtribbon::RibbonTabBar * (qtribbon::RibbonBar::*)() const) & qtribbon::RibbonBar::tabBar,
               "C++: qtribbon::RibbonBar::tabBar() const --> class qtribbon::RibbonTabBar *",
               pybind11::return_value_policy::automatic);
        cl.def("quickAccessToolBar", (int *(qtribbon::RibbonBar::*)() const) & qtribbon::RibbonBar::quickAccessToolBar,
               "C++: qtribbon::RibbonBar::quickAccessToolBar() const --> int *",
               pybind11::return_value_policy::automatic);
        cl.def("addQuickAccessButton",
               (void(qtribbon::RibbonBar::*)(int *)) & qtribbon::RibbonBar::addQuickAccessButton,
               "C++: qtribbon::RibbonBar::addQuickAccessButton(int *) --> void", pybind11::arg("button"));
        cl.def("setQuickAccessButtonHeight",
               (void(qtribbon::RibbonBar::*)(int)) & qtribbon::RibbonBar::setQuickAccessButtonHeight,
               "C++: qtribbon::RibbonBar::setQuickAccessButtonHeight(int) --> void", pybind11::arg("height"));
        cl.def("title", (int(qtribbon::RibbonBar::*)() const) & qtribbon::RibbonBar::title,
               "C++: qtribbon::RibbonBar::title() const --> int");
        cl.def("setTitle", (void(qtribbon::RibbonBar::*)(const int &)) & qtribbon::RibbonBar::setTitle,
               "C++: qtribbon::RibbonBar::setTitle(const int &) --> void", pybind11::arg("title"));
        cl.def("setTitleWidgetHeight", (void(qtribbon::RibbonBar::*)(int)) & qtribbon::RibbonBar::setTitleWidgetHeight,
               "C++: qtribbon::RibbonBar::setTitleWidgetHeight(int) --> void", pybind11::arg("height"));
        cl.def("rightToolBar", (int *(qtribbon::RibbonBar::*)() const) & qtribbon::RibbonBar::rightToolBar,
               "C++: qtribbon::RibbonBar::rightToolBar() const --> int *", pybind11::return_value_policy::automatic);
        cl.def("addRightToolButton", (void(qtribbon::RibbonBar::*)(int *)) & qtribbon::RibbonBar::addRightToolButton,
               "C++: qtribbon::RibbonBar::addRightToolButton(int *) --> void", pybind11::arg("button"));
        cl.def("setRightToolBarHeight",
               (void(qtribbon::RibbonBar::*)(int)) & qtribbon::RibbonBar::setRightToolBarHeight,
               "C++: qtribbon::RibbonBar::setRightToolBarHeight(int) --> void", pybind11::arg("height"));
        cl.def("helpRibbonButton", (int *(qtribbon::RibbonBar::*)() const) & qtribbon::RibbonBar::helpRibbonButton,
               "C++: qtribbon::RibbonBar::helpRibbonButton() const --> int *",
               pybind11::return_value_policy::automatic);
        cl.def("setHelpButtonIcon",
               (void(qtribbon::RibbonBar::*)(const int &)) & qtribbon::RibbonBar::setHelpButtonIcon,
               "C++: qtribbon::RibbonBar::setHelpButtonIcon(const int &) --> void", pybind11::arg("icon"));
        cl.def("removeHelpButton", (void(qtribbon::RibbonBar::*)()) & qtribbon::RibbonBar::removeHelpButton,
               "C++: qtribbon::RibbonBar::removeHelpButton() --> void");
        cl.def("collapseRibbonButton",
               (int *(qtribbon::RibbonBar::*)() const) & qtribbon::RibbonBar::collapseRibbonButton,
               "C++: qtribbon::RibbonBar::collapseRibbonButton() const --> int *",
               pybind11::return_value_policy::automatic);
        cl.def("setCollapseButtonIcon",
               (void(qtribbon::RibbonBar::*)(const int &)) & qtribbon::RibbonBar::setCollapseButtonIcon,
               "C++: qtribbon::RibbonBar::setCollapseButtonIcon(const int &) --> void", pybind11::arg("icon"));
        cl.def("removeCollapseButton", (void(qtribbon::RibbonBar::*)()) & qtribbon::RibbonBar::removeCollapseButton,
               "C++: qtribbon::RibbonBar::removeCollapseButton() --> void");
        cl.def("category",
               (class qtribbon::RibbonCategory * (qtribbon::RibbonBar::*)(const int &) const) &
                   qtribbon::RibbonBar::category,
               "C++: qtribbon::RibbonBar::category(const int &) const --> class qtribbon::RibbonCategory *",
               pybind11::return_value_policy::automatic, pybind11::arg("name"));
        cl.def("categories", (int(qtribbon::RibbonBar::*)() const) & qtribbon::RibbonBar::categories,
               "C++: qtribbon::RibbonBar::categories() const --> int");
        cl.def(
            "addCategory",
            [](qtribbon::RibbonBar &o, const int &a0) -> qtribbon::RibbonCategory * { return o.addCategory(a0); }, "",
            pybind11::return_value_policy::automatic, pybind11::arg("title"));
        cl.def(
            "addCategory",
            [](qtribbon::RibbonBar &o, const int &a0, enum qtribbon::RibbonCategoryStyle const &a1)
                -> qtribbon::RibbonCategory * { return o.addCategory(a0, a1); },
            "", pybind11::return_value_policy::automatic, pybind11::arg("title"), pybind11::arg("style"));
        cl.def("addCategory",
               (class qtribbon::RibbonCategory *
                (qtribbon::RibbonBar::*)(const int &, enum qtribbon::RibbonCategoryStyle, int)) &
                   qtribbon::RibbonBar::addCategory,
               "C++: qtribbon::RibbonBar::addCategory(const int &, enum qtribbon::RibbonCategoryStyle, int) --> class "
               "qtribbon::RibbonCategory *",
               pybind11::return_value_policy::automatic, pybind11::arg("title"), pybind11::arg("style"),
               pybind11::arg("color"));
        cl.def("addNormalCategory",
               (class qtribbon::RibbonNormalCategory * (qtribbon::RibbonBar::*)(const int &)) &
                   qtribbon::RibbonBar::addNormalCategory,
               "C++: qtribbon::RibbonBar::addNormalCategory(const int &) --> class qtribbon::RibbonNormalCategory *",
               pybind11::return_value_policy::automatic, pybind11::arg("title"));
        cl.def("addContextCategory",
               (class qtribbon::RibbonContextCategory * (qtribbon::RibbonBar::*)(const int &, int)) &
                   qtribbon::RibbonBar::addContextCategory,
               "C++: qtribbon::RibbonBar::addContextCategory(const int &, int) --> class "
               "qtribbon::RibbonContextCategory *",
               pybind11::return_value_policy::automatic, pybind11::arg("title"), pybind11::arg("color"));
        cl.def("addContextCategories",
               (class qtribbon::RibbonContextCategories * (qtribbon::RibbonBar::*)(const int &, const int &, int)) &
                   qtribbon::RibbonBar::addContextCategories,
               "C++: qtribbon::RibbonBar::addContextCategories(const int &, const int &, int) --> class "
               "qtribbon::RibbonContextCategories *",
               pybind11::return_value_policy::automatic, pybind11::arg("name"), pybind11::arg("titles"),
               pybind11::arg("color"));
        cl.def("showCategoryByIndex", (void(qtribbon::RibbonBar::*)(int)) & qtribbon::RibbonBar::showCategoryByIndex,
               "C++: qtribbon::RibbonBar::showCategoryByIndex(int) --> void", pybind11::arg("index"));
        cl.def(
            "showContextCategory",
            (void(qtribbon::RibbonBar::*)(class qtribbon::RibbonCategory *)) & qtribbon::RibbonBar::showContextCategory,
            "C++: qtribbon::RibbonBar::showContextCategory(class qtribbon::RibbonCategory *) --> void",
            pybind11::arg("category"));
        cl.def(
            "hideContextCategory",
            (void(qtribbon::RibbonBar::*)(class qtribbon::RibbonCategory *)) & qtribbon::RibbonBar::hideContextCategory,
            "C++: qtribbon::RibbonBar::hideContextCategory(class qtribbon::RibbonCategory *) --> void",
            pybind11::arg("category"));
        cl.def("categoryVisible",
               (bool(qtribbon::RibbonBar::*)(class qtribbon::RibbonCategory *)) & qtribbon::RibbonBar::categoryVisible,
               "C++: qtribbon::RibbonBar::categoryVisible(class qtribbon::RibbonCategory *) --> bool",
               pybind11::arg("category"));
        cl.def("removeCategory",
               (void(qtribbon::RibbonBar::*)(class qtribbon::RibbonCategory *)) & qtribbon::RibbonBar::removeCategory,
               "C++: qtribbon::RibbonBar::removeCategory(class qtribbon::RibbonCategory *) --> void",
               pybind11::arg("category"));
        cl.def("removeCategories",
               (void(qtribbon::RibbonBar::*)(class qtribbon::RibbonContextCategories *)) &
                   qtribbon::RibbonBar::removeCategories,
               "C++: qtribbon::RibbonBar::removeCategories(class qtribbon::RibbonContextCategories *) --> void",
               pybind11::arg("categories"));
        cl.def(
            "setCurrentCategory",
            (void(qtribbon::RibbonBar::*)(class qtribbon::RibbonCategory *)) & qtribbon::RibbonBar::setCurrentCategory,
            "C++: qtribbon::RibbonBar::setCurrentCategory(class qtribbon::RibbonCategory *) --> void",
            pybind11::arg("category"));
        cl.def("currentCategory",
               (class qtribbon::RibbonCategory * (qtribbon::RibbonBar::*)()) & qtribbon::RibbonBar::currentCategory,
               "C++: qtribbon::RibbonBar::currentCategory() --> class qtribbon::RibbonCategory *",
               pybind11::return_value_policy::automatic);
        cl.def("minimumSizeHint", (int(qtribbon::RibbonBar::*)()) & qtribbon::RibbonBar::minimumSizeHint,
               "C++: qtribbon::RibbonBar::minimumSizeHint() --> int");
        cl.def("_collapseButtonClicked", (void(qtribbon::RibbonBar::*)()) & qtribbon::RibbonBar::_collapseButtonClicked,
               "C++: qtribbon::RibbonBar::_collapseButtonClicked() --> void");
        cl.def("showRibbon", (void(qtribbon::RibbonBar::*)()) & qtribbon::RibbonBar::showRibbon,
               "C++: qtribbon::RibbonBar::showRibbon() --> void");
        cl.def("hideRibbon", (void(qtribbon::RibbonBar::*)()) & qtribbon::RibbonBar::hideRibbon,
               "C++: qtribbon::RibbonBar::hideRibbon() --> void");
        cl.def("ribbonVisible", (bool(qtribbon::RibbonBar::*)() const) & qtribbon::RibbonBar::ribbonVisible,
               "C++: qtribbon::RibbonBar::ribbonVisible() const --> bool");
        cl.def("setRibbonVisible", (void(qtribbon::RibbonBar::*)(bool)) & qtribbon::RibbonBar::setRibbonVisible,
               "C++: qtribbon::RibbonBar::setRibbonVisible(bool) --> void", pybind11::arg("visible"));
    }
}

#include <pybind11/pybind11.h>

#include <algorithm>
#include <functional>
#include <map>
#include <memory>
#include <stdexcept>
#include <string>

using ModuleGetter = std::function<pybind11::module &(std::string const &)>;

void bind_qtribbon_constants(std::function<pybind11::module &(std::string const &namespace_)> &M);
void bind_qtribbon_panel(std::function<pybind11::module &(std::string const &namespace_)> &M);
void bind_qtribbon_tabbar(std::function<pybind11::module &(std::string const &namespace_)> &M);

PYBIND11_MODULE(qtribbon, root_module) {
    root_module.doc() = "qtribbon module";

    std::map<std::string, pybind11::module> modules;
    ModuleGetter M = [&](std::string const &namespace_) -> pybind11::module & {
        auto it = modules.find(namespace_);
        if (it == modules.end())
            throw std::runtime_error("Attempt to access pybind11::module for namespace " + namespace_ +
                                     " before it was created!!!");
        return it->second;
    };

    modules[""] = root_module;

    static std::vector<std::string> const reserved_python_words{
        "nonlocal",
        "global",
    };

    auto mangle_namespace_name([](std::string const &ns) -> std::string {
        if (std::find(reserved_python_words.begin(), reserved_python_words.end(), ns) == reserved_python_words.end())
            return ns;
        return ns + '_';
    });

    std::vector<std::pair<std::string, std::string>> sub_modules{
        {"", "qtribbon"},
    };
    for (auto &p : sub_modules)
        modules[p.first.empty() ? p.second : p.first + "::" + p.second] =
            modules[p.first].def_submodule(mangle_namespace_name(p.second).c_str(),
                                           ("Bindings for " + p.first + "::" + p.second + " namespace").c_str());

    // pybind11::class_<std::shared_ptr<void>>(M(""), "_encapsulated_data_");

    bind_qtribbon_constants(M);
    bind_qtribbon_panel(M);
    bind_qtribbon_tabbar(M);
}

// Source list file: bindings/qtribbon.sources
// qtribbon.cpp
// qtribbon/constants.cpp
// qtribbon/panel.cpp
// qtribbon/tabbar.cpp

// Modules list file: bindings/qtribbon.modules
// qtribbon
