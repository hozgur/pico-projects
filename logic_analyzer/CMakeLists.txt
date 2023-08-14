cmake_minimum_required(VERSION 3.13)
include(pico_sdk_import.cmake)
project(logic_an C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(PICO_BOARD pico_w)
pico_sdk_init()
# Add optimization flag
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O3")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")

add_executable(logic_an
  main.c
)

pico_enable_stdio_usb(logic_an 0)
pico_enable_stdio_uart(logic_an 1)
pico_add_extra_outputs(logic_an)
target_link_libraries(logic_an pico_stdlib pico_cyw43_arch_none)
