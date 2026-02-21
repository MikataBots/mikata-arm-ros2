cmake_minimum_required(VERSION 3.22)
project(mikata_arm_bringup)

find_package(ament_cmake REQUIRED)

ament_package()

install(DIRECTORY launch config DESTINATION share/${PROJECT_NAME})
