# Import tkinter and webview libraries
from tkinter import *
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

dataFolder      = mD.dataFolder
gpsPort         = mD.gpsPort
statusJsonFile  = mD.statusJsonFile
hostsFile       = mD.hostsFile
hostsDataFolder = mD.hostsDataFolder

hosts       = yaml.load(open(hostsFile))

def getHostMac():
    scanner = nmap.PortScanner()
    hostNodes = hosts['nodeIDs']
    for hostIn in hostNodes:
        ipAddress = hostIn['IP']    
        host = socket.gethostbyname(ipAddress)
        scanner.scan(host, '1', '-v')
        ipState = scanner[host].state()
        if ipState == "up":
            hostID = os.popen("ssh teamlary@"+ ipAddress+' "cat /sys/class/net/eth0/address"').read().replace(":","").replace("\n","")
            if hostID == hostIn['nodeID']:
                print("Host " + hostID + " found @" + ipAddress) 
                return True, hostID,hostIn['IP'];
            else:
                print("Host " + hostID + " found with incorrect IP:" + ipAddress)
                return False, 0,0;
    print("No hosts found")                
    return False, -1,0;
     

def syncHostData(hostFound,hostID,hostIP):
    if hostFound:
        # Creating Folder 
        mSR.directoryCheck(hostsDataFolder+"/"+hostID+"/")
        mSR.directoryCheck(dataFolder+"/"+hostID+"/")
        os.system('rsync -avzrtu -e "ssh" teamlary@' +hostIP+":mintsData/raw/"+hostID +"/ " +hostsDataFolder+"/"+hostID)
        os.system('rsync -avzrtu -e "ssh" teamlary@' +hostIP+":mintsData/raw/"+hostID +"/ " +dataFolder+"/"+hostID)
        print()
        csvDataFiles = glob.glob(hostsDataFolder+"/"+hostID+ "/*/*/*/*.csv")
        print(csvDataFiles)
        for csvFile in csvDataFiles:
            print()
            with open(csvFile, "r") as f:
                sensorID = csvFile.split("_")[-4]
                # sensorID = sensorIDPre.replace("\n","").replace("\r","").replace("\t","")
                reader = csv.DictReader(f)
                rowList = list(reader)
                for rowData in rowList:
                    print("Publishing MQTT Data for sensorID:"+sensorID)
                    print(sensorID)
                    # mL.writeMQTTLatestWearable(rowData,sensorID,hostID)  









def main():
    hostFound,hostID,hostIP = getHostMac()
    syncHostData(hostFound,hostID,hostIP)

    # print("Main")
    # lk = glob.glob("/home/teamlary/mintsData/*/*/*/*/*/*.csv")
    # print(lk[10])
    # with open(lk[10], "r") as f:
    #     reader = csv.DictReader(f)
    #     a = list(reader)
    #     # print(reader)
    #     # print(a)

    # for lk2 in a:
    #     print("------------------------")
    #     print(lk2)
    #     mL.writeMQTTLatestWearable(lk2,"OPCN3","nodeIDWearable")  


if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    main()