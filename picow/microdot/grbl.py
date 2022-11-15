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
        return res

def close():
    if ser and ser.isOpen():
        ser.close()

def getResponse():
    if ser and ser.isOpen():
        print("Waiting for response")
        return ser.readline().decode().strip()

def getStatus():
    if ser and ser.isOpen():
        status = sendCommand("?")        
        if status:
            stat =parseStatus(status)
            print(stat)
            return stat
        else:
            return None

def parseStatus(status):
    if status:
        if status.startswith("<"):
            status = status[1:]
        if status.endswith(">"):
            status = status[:-1]
        status = status.split("|")
        result = {}
        result["Status"] = status[0]
        status = status[1:]
        for s in status:
            if s.startswith("WCO:"):
                s = s[4:]
                s = s.split(",")
                result["WCO"] = {"X": float(s[0]), "Y": float(s[1]), "Z": float(s[2])}
            elif s.startswith("MPos:"):
                s = s[5:]
                s = s.split(",")
                result["MPos"] = {"X": float(s[0]), "Y": float(s[1]), "Z": float(s[2])}
            elif s.startswith("WPos:"):
                s = s[5:]
                s = s.split(",")
                result["WPos"] = {"X": float(s[0]), "Y": float(s[1]), "Z": float(s[2])}
            elif s.startswith("FS:"):
                s = s[3:]
                s = s.split(",")
                result["FS"] = {"S": float(s[0]), "F": float(s[1])}            
            elif s.startswith("Pn"):
                s = s[2:]
                s = s.split(",")
                result["Pn"] = {"X": int(s[0]), "Y": int(s[1]), "Z": int(s[2]), "A": int(s[3]), "B": int(s[4]), "C": int(s[5])}
            elif s.startswith("Ov:"):
                s = s[3:]
                s = s.split(",")
                result["Ov"] = {"A": int(s[0]), "B": int(s[1]), "C": int(s[2])}
            elif s.startswith("Ln:"):
                s = s[3:]
                result["Ln"] = int(s)
        return result