/**
 * Copyright (c) 2022 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include "pico/stdlib.h"
#include "stdio.h"
#include "file_system.hpp"

int create_file() {
    // Create a file
    file_t *file = open_file("test.txt", "w");
    if (file == NULL) {
        printf("Error creating file\n");
        return -1;
    }

    // Write to the file
    const char *text = "Hello, world!\n";
    int result = write_file(file, text, strlen(text));
    if (result != 0) {
        printf("Error writing to file\n");
        return -1;
    }

    // Close the file
    result = close_file(file);
    if (result != 0) {
        printf("Error closing file\n");
        return -1;
    }
    return 0;
}

int read_file() {
    // Open the file again
    file_t *file = open_file("test.txt", "r");
    if (file == NULL) {
        printf("Error opening file\n");
        return -1;
    }

    // Read from the file
    char buffer[100];
    int result = read_file(file, buffer, sizeof(buffer));
    if (result < 0) {
        printf("Error reading from file\n");
        close_file(file);
        return -1;
    }
    buffer[result] = '\0';
    printf("Read %d bytes: %s\n", result, buffer);


    // Close the file
    result = close_file(file);
    if (result != 0) {
        printf("Error closing file\n");
        return -1;
    }
    return 0;
}

int main() {
    // Initialize chosen serial port
    stdio_init_all(); 
    timer_hw->dbgpause = 0; // on debugging halt, keep timer running
    const uint LED_PIN = 14;
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    // Led Test
    gpio_put(LED_PIN, 1);
    sleep_ms(500);
    gpio_put(LED_PIN, 0);
    
    printf("File System Test\n");

    // Mount the file system
    int result = mount();
    if (result < 0) {
        printf("Error mounting file system\n");
        return 1;
    }

    // Read file
    result = read_file();
    if (result < 0) {
        printf("Error reading file\n");
    }
    printf("Creating file\n");
    result = create_file();
    if (result < 0) {
        printf("Error creating file\n");
        return 1;
    }
    result = read_file();
    if (result < 0) {
        printf("Error reading file\n");
        return 1;
    }
    // Unmount the file system
    result = unmount();
    if (result != 0) {
        printf("Error unmounting file system\n");
        return 1;
    }
}
