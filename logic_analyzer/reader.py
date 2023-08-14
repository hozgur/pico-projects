import serial
import struct
import csv
import sys
import select

# Configuration
PORT = '/dev/tty.usbmodem11102'
BAUD_RATE = 230400 * 2 # Adjust this to match your device's baud rate
OUTPUT_FILE = 'data.csv'
counter = 0
def main():
    global counter
    with serial.Serial(PORT, BAUD_RATE, timeout=1) as ser:
        with open(OUTPUT_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Signal", "Elapsed Time"])  # Write the header
            
            while True:
                # Check if a key has been pressed
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    print("\nKey pressed, stopping...")
                    break
                
                data = ser.read(4)  # Read 4 bytes (since you're sending uint32_t)

                # Ensure we've read 4 bytes before unpacking
                if len(data) == 4:
                    value = struct.unpack('<I', data)[0]  # '<I' is little-endian unsigned int
                    signal, elapsed = process_value(value)
                    counter += 1
                    # Write to CSV
                    writer.writerow([signal, elapsed])

def process_value(value):
    global counter
    signal = (value >> 31) & 0x1
    elapsed = value & 0x7fffffff
    #print(f"{counter}")
    return signal, elapsed

if __name__ == '__main__':
    main()
