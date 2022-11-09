#grbl.py
from time import sleep
import serial
import config
from helpers import isPico
def connect():
    global ser
    try:
        ser = serial.Serial(config.serialPort, 115200, timeout=3)
    except Exception as e:
        print(e)
        print("Could not connect to serial port")
        ser = None
        return False    
    if ser.isOpen():
        print('Connected to: ' + ser.portstr)
        line = getResponse()
        if line:
            if line.startswith('Grbl'):
                print(line)
                return True
        else:
            line = getResponse()
            if line:
                if line.startswith('Grbl'):
                    print(line)
                    return True
                else:
                    print("Could not connect to grbl")
                    return False
            return False
    else:
        return False

def sendCommand(command):
    if ser and ser.isOpen():
        command = command + "\r"
        ser.write(command.encode())
        res = getResponse()
        print(res)

def close():
    if ser and ser.isOpen():
        ser.close()

def getResponse():
    if ser and ser.isOpen():
        print("Waiting for response")
        return ser.readline().decode().strip()