import numpy as np
# read csv file
csvdata = open('data.csv', 'r').read()
# Split the string into lines and skip the header
lines = csvdata.strip().split("\n")[1:]

# Parse each line with first column as int8 and second column as float
data_list = [(np.int8(line.split(',')[0]), float(line.split(',')[1])) for line in lines]

# Convert the list into a numpy array
data = np.array(data_list, dtype=[('Signal', np.int8), ('Elapsed Time', float)])

NEW_SESSION = 0x100

WAIT_RESET  = 0
RESET       = 1
READ_BYTE   = 2
RESPONSE    = 3

RESET_THRESHOLD     = 400
PRESENSE_THRESHOLD  = 80
ZERO_THRESHOLD      = 15


def decode(data):
    state = WAIT_RESET
    bytes = []
    bits = 1
    new_session = True
    for signal, duration in data:
        if signal == 0:
            if duration > RESET_THRESHOLD:
                state = RESET
                new_session = True
                continue
            if state == RESET:
                if duration > PRESENSE_THRESHOLD:
                    state = READ_BYTE
                    command = 0
                    bits = 1
                    continue
                else:
                    print("Error on waiting for presence")
                    state = WAIT_RESET
                    continue

            if state == READ_BYTE:
                if duration > ZERO_THRESHOLD:
                    bits = bits << 1
                else:
                    command += bits
                    bits = bits << 1
                
                if bits == 256:
                    if new_session:
                        new_session = False
                        bytes.append(NEW_SESSION)
                    
                    bytes.append(command)
                    command = 0
                    bits = 1
    return bytes


rom_commands = {
    0x100:  "NEW_SESSION",
    0x33:   "READ_ROM",
    0x55:   "MATCH_ROM",
    0xCC:   "SKIP_ROM",
    0xF0:   "SEARCH_ROM",
    0xA5:   "RESUME",
    0x3C:   "OVERDRIVE_SKIP_ROM",
    0x69:   "OVERDRIVE_MATCH_ROM",
}

memory_commands = {
    0xAA:   "READ_PAD",
    0x55:   "COPY_PAD",
    0xF0:   "READ_MEMORY"
}

# States
READ_ROM_COMMAND    = 1
READ_MEM_ADDRESS    = 2
READ_MEMORY         = 3 
READ_SERIAL         = 4
VERIFY_SERIAL       = 5
READ_MEM_COMMAND    = 6

chip = {
    "serial": 0,
    "data": np.zeros(1024, dtype=np.uint8)
}

def parse(data):
    state = WAIT_RESET
    buffer = []
    address = 0
    for value in data:
        if value == NEW_SESSION:
            print("NEW_SESSION")
            state = READ_ROM_COMMAND
            continue

        if state == READ_ROM_COMMAND:
            if value in rom_commands:
                buffer = []
                if rom_commands[value] == "READ_ROM":
                    print("READ_ROM")
                    state = READ_SERIAL
                    continue
                if rom_commands[value] == "MATCH_ROM":
                    print("MATCH_ROM")
                    state = VERIFY_SERIAL
                    continue
                if rom_commands[value] == "SKIP_ROM":
                    print("SKIP_ROM")
                    state = READ_MEM_COMMAND
                    continue
                if rom_commands[value] == "SEARCH_ROM":
                    print("SEARCH_ROM (not implemented)")
                    state = WAIT_RESET
                    continue
                if rom_commands[value] == "RESUME":
                    print("RESUME (not implemented)")
                    state = WAIT_RESET
                    continue
                if rom_commands[value] == "OVERDRIVE_SKIP_ROM":
                    print("OVERDRIVE_SKIP_ROM (not implemented)")
                    state = WAIT_RESET
                    continue
                if rom_commands[value] == "OVERDRIVE_MATCH_ROM":
                    print("OVERDRIVE_MATCH_ROM (not implemented)")
                    state = WAIT_RESET
                    continue
            else:
                print("Unknown ROM command: %02X" % value)
                state = WAIT_RESET
                continue

        if state == READ_SERIAL:
            buffer.append(value)
            if len(buffer) == 8:
                chip["serial"] = buffer
                print("Serial: %02X%02X%02X%02X%02X%02X%02X%02X" % tuple(buffer))
                state = WAIT_RESET
                continue
        
        if state == VERIFY_SERIAL:
            buffer.append(value)
            if len(buffer) == 8:
                if buffer == chip["serial"]:
                    print("Serial: %02X%02X%02X%02X%02X%02X%02X%02X" % tuple(buffer))
                    state = READ_MEM_COMMAND
                else:
                    print("Serial: %02X%02X%02X%02X%02X%02X%02X%02X (mismatch)" % tuple(buffer))
                    state = WAIT_RESET
                continue
            
        if state == READ_MEM_COMMAND:
            if value in memory_commands:
                buffer = []
                if memory_commands[value] == "READ_PAD":
                    print("READ_PAD")
                    state = READ_MEMORY
                    continue
                if memory_commands[value] == "COPY_PAD":
                    print("COPY_PAD (not implemented)")
                    state = WAIT_RESET
                    continue
                if memory_commands[value] == "READ_MEMORY":
                    print("READ_MEMORY")
                    state = READ_MEM_ADDRESS
                    continue
            else:
                print("Unknown memory command: %02X" % value)
                state = WAIT_RESET
                continue
        
        if state == READ_MEM_ADDRESS:
            buffer.append(value)
            if len(buffer) == 2:
                address = buffer[0] + (buffer[1] << 8)
                print("Address: %04X" % address)
                state = READ_MEMORY
                continue
        
        if state == READ_MEMORY:
            chip["data"][address] = value
            print("Memory[%04X] = %02X" % (address, value))
            address += 1
            if address == 0x90:
                print("Memory read complete unbound reading memory")
                continue
data = decode(data)
parse(data)
