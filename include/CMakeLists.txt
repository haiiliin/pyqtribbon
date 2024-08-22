cmake_minimum_required(VERSION 3.16)

project(qtribbon LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
set(PROJECT_SOURCES
        main.cpp
        qtribbon/category.hpp
        qtribbon/constants.hpp
        qtribbon/gallery.hpp
        qtribbon/menu.hpp
        qtribbon/panel.hpp
        qtribbon/ribbonbar.hpp
        qtribbon/separator.hpp
        qtribbon/tabbar.hpp
        qtribbon/titlewidget.hpp
        qtribbon/toolbutton.hpp
        qtribbon/resources.qrc
)

if(${QT_VERSION_MAJOR} GREATER_EQUAL 6)
    qt_add_executable(qtribbon MANUAL_FINALIZATION ${PROJECT_SOURCES})
else()
    if(ANDROID)
        add_library(qtribbon SHARED ${PROJECT_SOURCES})
    else()
        add_executable(qtribbon ${PROJECT_SOURCES})
    endif()
endif()

target_link_libraries(qtribbon PRIVATE Qt${QT_VERSION_MAJOR}::Widgets)

if(QT_VERSION_MAJOR EQUAL 6)
    qt_finalize_executable(qtribbon)
endif()
