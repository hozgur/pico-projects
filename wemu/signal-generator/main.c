#include "pico/stdlib.h"

const uint OUT_PIN = 16;
const uint LED_PIN = 17;

int main() {

    
    gpio_init(LED_PIN);
    gpio_init(OUT_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    gpio_set_dir(OUT_PIN, GPIO_OUT);
    while (true) {
        gpio_put(LED_PIN, 1);
        sleep_ms(250);
        gpio_put(LED_PIN, 0);
        sleep_ms(250);
    }
}