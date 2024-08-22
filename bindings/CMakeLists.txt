cmake_minimum_required(VERSION 3.16)
project(qtribbon)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets)

# Obtain the parent directories of the current directory
get_filename_component(PARENT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} DIRECTORY)

# Include directories
include_directories(${PARENT_DIRECTORY}/include)

# Set up Python, be sure to have NumPy installed
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 2.13.0 CONFIG REQUIRED)

# Add pybind11 module
pybind11_add_module(qtribbon qtribbon.cpp)
set_target_properties(qtribbon PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PPARENT_DIRECTORY}/pyqtribbon/$<0:>)
target_link_libraries(qtribbon PRIVATE Qt${QT_VERSION_MAJOR}::Widgets)
install(TARGETS qtribbon LIBRARY DESTINATION pyqtribbon COMPONENT qtribbon)
