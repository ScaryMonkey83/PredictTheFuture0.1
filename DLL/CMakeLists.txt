cmake_minimum_required(VERSION 3.13)
project(DLL)

set(CMAKE_CXX_STANDARD 14)

add_library(DLL library.cpp library.h)

find_package(Boost)
IF (Boost_FOUND)
    include_directories(${Boost_INCLUDE_DIR})
endif()

set(Boost_USE_STATIC_LIBS OFF)