# Import tkinter and webview libraries
from fileinput import filename
from tkinter import *
from traceback import print_stack
import webview
import glob
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
import time
import serial
import pynmea2
from collections import OrderedDict
from os import listdir
from os.path import isfile, join
from mintsXU4 import mintsLatest as mL
import csv
import os 
import nmap, socket
import yaml
import json

dataFolder          = mD.dataFolder
gpsPort             = mD.gpsPort
statusJsonFile      = mD.statusJsonFile
hostsFile           = mD.hostsFile
locationsFile       = mD.locationsFile
hostsDataFolder     = mD.hostsDataFolder
statusJsonFile      = mD.statusJsonFile
hostsStatusJsonFile = mD.hostsStatusJsonFile
gpsOnJsonFile       = mD.gpsOnJsonFile
gpsOffJsonFile      = mD.gpsOffJsonFile

hosts     = yaml.load(open(hostsFile),Loader=yaml.FullLoader)
locations = yaml.load(open(locationsFile),Loader=yaml.FullLoader)

repos        = locations['locations']['repos']
rawFolder    = locations['locations']['rawFolder']
latestFolder = locations['locations']['latestFolder']

def getHostMac():
    scanner = nmap.PortScanner()
    hostNodes = hosts['nodeIDs']
    dateTime = datetime.datetime.now() 

    for hostIn in hostNodes:
        ipAddress = hostIn['IP']    
        host = socket.gethostbyname(ipAddress)
        scanner.scan(host, '1', '-v')
        ipState = scanner[host].state()
        if ipState == "up":
            hostID = os.popen("ssh teamlary@"+ ipAddress+' "cat /sys/class/net/eth0/address"').read().replace(":","").replace("\n","")
            if hostID == hostIn['nodeID']:
                print("Host " + hostID + " found @" + ipAddress) 
                sensorDictionary = OrderedDict([
                    ("dateTime"             ,str(dateTime)),
                    ("status1"               ,2.212)
                    ])
                mSR.sensorFinisherWearable(dateTime,hostID,"MINTSCS005",sensorDictionary)
                return True, hostID,hostIn['IP'];
            else:
                print("Host " + hostID + " found with incorrect IP:" + ipAddress)
                sensorDictionary = OrderedDict([
                    ("dateTime"             ,str(dateTime)),
                    ("status"                ,str(0.0))
                    ])
                mSR.sensorFinisherWearable(dateTime,hostID,"MINTSCS001",sensorDictionary)
                
                # ADD Incorrect IP Error
                sensorDictionary = OrderedDict([
                    ("dateTime"             ,str(dateTime)),
                    ("error"                ,str(2.0))
                    ])
                
                mSR.sensorFinisherWearable(dateTime,hostID,"MINTSES001",sensorDictionary)                
                
                return False, 0,0;
                    
    print("No hosts found")                
    sensorDictionary = OrderedDict([
                    ("dateTime"             ,str(dateTime)),
                    ("status"               ,str(0.0))
                    ])
    mSR.sensorFinisherWearable(dateTime,hostID,"MINTSCS001",sensorDictionary)    
    return False, -1,0;

def readLatestTime(hostID,sensorID):
    fileName = latestFolder + "/" + hostID+"_"+sensorID+".json"
    if os.path.isfile(fileName):
        try:    
            with open(fileName, 'r') as f:
                data = json.load(f)
            return datetime.datetime.strptime(data['dateTime'],'%Y-%m-%d %H:%M:%S.%f')

        except Exception as e:
            
            print(e)
    else:
        return datetime.datetime.strptime("2022-10-04 22:40:40.204179",'%Y-%m-%d %H:%M:%S.%f')
   
def writeLatestTime(hostID,sensorID,dateTime):
    fileName = latestFolder + "/" + hostID+"_"+sensorID+".json"
    mSR.directoryCheck2(fileName)
    sensorDictionary = OrderedDict([
                ("dateTime"            ,str(dateTime))
                ])
    with open(fileName, "w") as outfile:
        json.dump(sensorDictionary,outfile)

def syncHostData(hostFound,hostID,hostIP):
    dateTime = datetime.datetime.now() 
    if hostFound:
        mSR.directoryCheck2(dataFolder+"/"+hostID+"/")
        os.system('rsync -avzrtu -e "ssh" teamlary@' + hostIP + ":" + rawFolder + hostID +"/ " + dataFolder + "/" + hostID)
        sensorDictionary = OrderedDict([
                    ("dateTime"             ,str(dateTime)),
                    ("status1"               ,24)
                    ])
        print(sensorDictionary)
        mSR.sensorFinisherWearable(dateTime,hostID,"MINTSCS005",sensorDictionary)  
        # mL.writeMQTTLatestWearable(hostID,"MINTSCS001",sensorDictionary) 
        time.sleep(10)

        csvDataFiles = glob.glob(dataFolder+"/"+hostID+ "/*/*/*/*.csv")
        csvDataFiles.sort()

        for csvFile in csvDataFiles:
            print("================================================")
            print(csvFile)
            try:
                with open(csvFile, "r") as f:
                    sensorID       = csvFile.split("_")[-4]
                    reader            = csv.DictReader(f)
                    rowList           = list(reader)
                    # rowList.sort()
                    # print(rowList)
                    latestDateTime    = readLatestTime(hostID,sensorID)
                    # print(latestDateTime)
                    csvLatestDateTime = datetime.datetime.strptime(rowList[-1]['dateTime'],'%Y-%m-%d %H:%M:%S.%f')

                    if csvLatestDateTime > latestDateTime:
                        for rowData in rowList:
                            dateTimeRow = datetime.datetime.strptime(rowData['dateTime'],'%Y-%m-%d %H:%M:%S.%f')
                            if dateTimeRow > latestDateTime:
                                try:
                                    print("Publishing MQTT Data ==> Node ID:"+hostID+ ", Sensor ID:"+ sensorID+ ", Time stamp: "+ str(dateTimeRow))
                                    mL.writeMQTTLatestWearable(hostID,sensorID,rowData)  
                                    time.sleep(0.001)
                                    
                                except Exception as e:
                                    print(e)
                                    print("Data row not published")
                        writeLatestTime(hostID,sensorID,csvLatestDateTime)
                        print("================================================")
                        print("Latest Date Time ==> Node:"+ hostID + ", SensorID:"+ sensorID)
                        print(csvLatestDateTime)
                        print("================================================")

            except Exception as e:
                print(e)
                print("Data file not published")
                print(csvFile)



def main():
    while True:
        hostFound,hostID,hostIP = getHostMac()
        syncHostData(hostFound,hostID,hostIP)
        time.sleep(10)

if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    main()