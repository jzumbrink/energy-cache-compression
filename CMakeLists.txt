cmake_minimum_required(VERSION 4.0)
project(EnergyEfficientAlgorithms)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_compile_options(-O3 -march=native -mtune=native)

add_subdirectory("${CMAKE_SOURCE_DIR}/external/ips4o")

######################
# Testing Algorithms #
######################
add_executable(TestingAlgorithms testing_algorithms.cpp
        cli.hpp)

set_target_properties(TestingAlgorithms PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin
)

target_link_libraries(TestingAlgorithms PRIVATE ips4o)

target_include_directories(TestingAlgorithms PRIVATE
        ${CMAKE_SOURCE_DIR}/external/ips4o/include
)

######################
#      Sorting       #
######################
add_executable(Sorting sorting.cpp
        cli.hpp)

set_target_properties(Sorting PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin
)

target_link_libraries(Sorting PRIVATE ips4o)

target_include_directories(Sorting PRIVATE
        ${CMAKE_SOURCE_DIR}/external/ips4o/include
)

