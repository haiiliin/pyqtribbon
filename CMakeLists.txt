cmake_minimum_required(VERSION 3.16)

project(qtribbon LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Widgets Gui)
qt_standard_project_setup()

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

qt_add_executable(qtribbon
    main.cpp
)
target_link_libraries(qtribbon PRIVATE Qt6::Core Qt6::Widgets Qt6::Gui)
