// // Logic Anaylzer

// #include "pico/stdlib.h"
// #include "stdio.h"

// const uint LED_PIN      = 14;
// const uint SIGNAL_PIN   = 10;

// int main() {
//     // Initialize chosen serial port
//     stdio_init_all();
//     timer_hw->dbgpause = 0; // on debugging halt, keep timer running
//     uint lastSignal = 0;
//     uint lastTime = time_us_32();
//     gpio_init(LED_PIN);
//     gpio_init(SIGNAL_PIN);
//     gpio_set_dir(LED_PIN, GPIO_OUT);
//     gpio_set_dir(SIGNAL_PIN, GPIO_IN);
//     printf("Logic Analyzer Started\n");
//     while (true) {
//        // Read Signal Pin if state changed print to serial binary with microseconds
//        // if signal is 1 then print 31th bit 1 and 30th bit is elapsed time
//        // Send serial data hexadecimal
//          uint signal = gpio_get(SIGNAL_PIN);
//             if (signal != lastSignal) {
//                 lastSignal = signal;
//                 uint32_t time = time_us_32();
//                 uint32_t elapsed = time - lastTime;
//                 lastTime = time;
//                 uint32_t data = (signal << 31) | (elapsed & 0x7fffffff);
//                 printf("%08x\n", data);
//                 gpio_put(LED_PIN, signal);
//             } 
//     }
// }

#include "pico/stdlib.h"
#include "stdio.h"
#include "hardware/sync.h"
const uint LED_PIN = 14;
const uint SIGNAL_PIN = 10;

#define BUFFER_SIZE 8192
uint32_t buffer[BUFFER_SIZE];
volatile uint32_t writeIndex = 0;
uint32_t readIndex = 0;
volatile uint32_t lastTime = 0;
volatile bool bufferOverflow = false;
volatile uint32_t itemCount = 0;

void gpio_callback(uint gpio, uint32_t events) {
    uint32_t time = time_us_32();
    uint32_t elapsed = time - lastTime; 
    lastTime = time;

    uint32_t signal = gpio_get(SIGNAL_PIN);
    uint32_t data = (signal << 31) | (elapsed & 0x7fffffff);

    buffer[writeIndex] = data;
    atomic_add(&writeIndex, 1);

    
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

    // Set up interrupt
    gpio_set_irq_enabled_with_callback(SIGNAL_PIN, GPIO_IRQ_EDGE_RISE | GPIO_IRQ_EDGE_FALL, true, &gpio_callback);

    while (true) {
        while (readIndex != writeIndex) {
            uart_send_data(uart0, buffer[readIndex]);
            atomic_store(readIndex, (readIndex + 1) % BUFFER_SIZE);  // Atomic store operation
        }
    }
}
