#include "pico/stdlib.h"

typedef void(*funcPtr)(void);

int code[] = {0x01000000,0x02000000,0x03000000};

const uint OUT_PIN = 16;
int pc = 0;

void setHigh() {
    gpio_put(OUT_PIN, 1);
    pc++;
}

void setLow() {
    gpio_put(OUT_PIN, 0);
    pc++;
}

void jump() {
    pc = 0;
}

funcPtr jumpTable[] = {setHigh, setLow, jump};

int main() {
// Initialize the GPIO pin
    gpio_init(OUT_PIN);
    gpio_set_dir(OUT_PIN, GPIO_OUT);
    while(1) {
        jumpTable[pc]();        
    }
    return 0;
}
