cmake_minimum_required(VERSION 3.13)
include(pico_sdk_import.cmake)
project(file_system C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(PICO_BOARD pico_w)
pico_sdk_init()
add_executable(file_system
  main.cpp
  file_system.cpp
  lfs/lfs.c
  lfs/lfs_util.c
)

pico_enable_stdio_usb(file_system 0)
pico_enable_stdio_uart(file_system 1)
pico_add_extra_outputs(file_system)
target_link_libraries(file_system pico_stdlib pico_cyw43_arch_none)