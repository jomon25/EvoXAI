cmake_minimum_required(VERSION 3.14)
project(EvoXAICPP VERSION 1.0)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_BUILD_TYPE Release)

add_library(engine INTERFACE src/engine.hpp)

target_include_directories(engine INTERFACE src)
target_link_libraries(engine INTERFACE grpc++ protobuf spdlog::spdlog)
