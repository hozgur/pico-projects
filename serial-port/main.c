#include <stdio.h>
#include "pico/stdlib.h"

#define OUT_PIN 25
int main() {
// Initialize the GPIO pin
    
    gpio_init(OUT_PIN);
    gpio_set_dir(OUT_PIN, GPIO_OUT);
     // Initialize chosen serial port
    stdio_init_all();
    while(true) {
        printf("Hello World!\n");
        sleep_ms(500);
    }
    return 0;
}
