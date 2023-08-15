#include "pico/stdlib.h"
#include "stdio.h"
#include "pico/mutex.h"

const uint LED_PIN = 14;
const uint SIGNAL_PIN = 10;

#define BUFFER_SIZE 8192
uint32_t buffer[BUFFER_SIZE];
volatile uint32_t writeIndex = 0;
uint32_t readIndex = 0;
static mutex_t buffer_mutex;
volatile uint32_t lastTime = 0;
volatile bool bufferOverflow = false;
volatile uint32_t itemCount = 0;

void gpio_callback(uint gpio, uint32_t events) {
    uint32_t time = time_us_32();
    uint32_t elapsed = time - lastTime; 
    lastTime = time;

    uint32_t signal = gpio_get(SIGNAL_PIN);
    uint32_t data = (signal << 31) | (elapsed & 0x7fffffff);

    mutex_enter_blocking(&buffer_mutex);

    if (itemCount == BUFFER_SIZE) {
        // Buffer is full. Overwrite the oldest data and move the readIndex.
        bufferOverflow = true;
        gpio_put(LED_PIN, 1); // Turn on the LED
        readIndex = (readIndex + 1) % BUFFER_SIZE; // Move readIndex to next position
    } else {
        itemCount++;
    }

    buffer[writeIndex] = data;
    writeIndex = (writeIndex + 1) % BUFFER_SIZE;

    mutex_exit(&buffer_mutex);
}


void uart_send_data(uart_inst_t *uart, uint32_t data) {
    for (int i = 0; i < 4; i++) {
        uart_putc(uart, (data >> (i * 8)) & 0xFF);
    }
}

int main() {
    stdio_init_all();
    timer_hw->dbgpause = 0;
    gpio_init(LED_PIN);
    gpio_init(SIGNAL_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    gpio_set_dir(SIGNAL_PIN, GPIO_IN);
    printf("Logic Analyzer Started\n");
    // test led
    gpio_put(LED_PIN, 1);
    sleep_ms(1000);
    gpio_put(LED_PIN, 0);
    uart_init(uart0, 115200 * 4);  // Double the standard 115200 baud rate

    mutex_init(&buffer_mutex);

    // Set up interrupt
    gpio_set_irq_enabled_with_callback(SIGNAL_PIN, GPIO_IRQ_EDGE_RISE | GPIO_IRQ_EDGE_FALL, true, &gpio_callback);

    while (true) {
        while (itemCount > 0) {
            mutex_enter_blocking(&buffer_mutex);
            //printf("%08x\n", buffer[readIndex]);
            uart_send_data(uart0, buffer[readIndex]);
            readIndex = (readIndex + 1) % BUFFER_SIZE;
            itemCount--;
            mutex_exit(&buffer_mutex);
        }

        // Once we start freeing up buffer space, turn off the LED if it was on due to overflow.
        if (bufferOverflow && itemCount < BUFFER_SIZE) {
            bufferOverflow = false;
            gpio_put(LED_PIN, 0); // Turn off the LED
        }
    }
}