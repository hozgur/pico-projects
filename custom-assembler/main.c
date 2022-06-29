#include <stdio.h>
#include "pico/stdlib.h"


// Command Groups
#define CMD_GROUP_BITBANG 0x80000000

enum insts {WAIT0,WAIT1,SET0,SET1,JMP};


void step(int inst) {
    if(inst & CMD_GROUP_BITBANG) {
        
    }
}



#define OUT_PIN 25
int main() {
// Initialize the GPIO pin
    
    gpio_init(OUT_PIN);
    gpio_set_dir(OUT_PIN, GPIO_OUT);
     
    stdio_init_all(); // Initialize chosen serial port
    while(true) {
        printf("Hello World!\n");
        sleep_ms(500);
    }
    return 0;
}
