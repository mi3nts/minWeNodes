
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
import time
import serial
import pynmea2
from collections import OrderedDict

import json

dataFolder     = mD.dataFolder
gpsPort        = mD.gpsPort
statusJsonFile = mD.statusJsonFile

baudRate  = 9600


def gpsToggle():
    try:    
        with open(statusJsonFile, 'r') as f:
            data = json.load(f)

        return data['gps'] == "on" 
    except Exception as e:
            
        print(e)
        print("GPS Turned Off")
        return False

    



def main():
    gpsToggle()
    reader = pynmea2.NMEAStreamReader()
    ser = serial.Serial(
    port= gpsPort,\
    baudrate=baudRate,\
    parity  =serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

    lastGPRMC = time.time()
    lastGPGGA = time.time()
    delta  = 2
    print("connected to: " + ser.portstr)

    #this will store the line
    line = []
    while True:
        try:
            for c in ser.read():
                line.append(chr(c))
                if chr(c) == '\n' and gpsToggle():
                    dataString     = (''.join(line))
                    dateTime  = datetime.datetime.now()

                    if (dataString.startswith("$GPGGA") and mSR.getDeltaTime(lastGPGGA,delta)):
                        lastGPGGA = time.time()
                        mSR.GPSGPGGA2Write(dataString,dateTime)
                        
                    if (dataString.startswith("$GPRMC") and mSR.getDeltaTime(lastGPRMC,delta)):
                        lastGPRMC = time.time()
                        mSR.GPSGPRMC2Write(dataString,dateTime)
                       
                    line = []
                    break
        except Exception as e:
            
            print(e)
            print()
            
    ser.close()



if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Monitoring GPS Sensor on port: {0}".format(gpsPort[0])+ " with baudrate " + str(baudRate))
    main()