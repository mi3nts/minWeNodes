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

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

dataFolder          = mD.dataFolder
gpsPort             = mD.gpsPort
statusJsonFile      = mD.statusJsonFile
hostsFile           = mD.hostsFile
hostsDataFolder     = mD.hostsDataFolder
statusJsonFile      = mD.statusJsonFile
hostsStatusJsonFile = mD.hostsStatusJsonFile
gpsOnJsonFile       = mD.gpsOnJsonFile
gpsOffJsonFile      = mD.gpsOffJsonFile




hosts       = yaml.load(open(hostsFile),Loader=yaml.FullLoader)

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
        mSR.directoryCheck(hostsDataFolder+"/"+hostID+"/")
        mSR.directoryCheck(dataFolder+"/"+hostID+"/")
        os.system('rsync -avzrtu -e "ssh" teamlary@' +hostIP+":mintsData/raw/"+hostID +"/ " +hostsDataFolder+"/"+hostID)
        os.system('rsync -avzrtu -e "ssh" teamlary@' +hostIP+":mintsData/raw/"+hostID +"/ " +dataFolder+"/"+hostID)
        csvDataFiles = glob.glob(hostsDataFolder+"/"+hostID+ "/*/*/*/*.csv")
        for csvFile in csvDataFiles:
            print()
            try:
                with open(csvFile, "r") as f:
                    sensorID = csvFile.split("_")[-4]
                    reader = csv.DictReader(f)
                    rowList = list(reader)
                    for rowData in rowList:
                        try:
                            print("Publishing MQTT Data for sensorID:"+sensorID)
                            mL.writeMQTTLatestWearable(rowData,sensorID,hostID)  
                            time.sleep(0.001)
                        except Exception as e:
                            print(e)
                            print("Data row not published")
            except Exception as e:
                print(e)
                print("Data file not published")
                print(csvFile)

def gpsToggle(hostFound,hostIP):
    if hostFound:
        mSR.directoryCheck2(hostsStatusJsonFile)
        out = os.popen('rsync -avzrtu -e "ssh" teamlary@' +hostIP+":"+statusJsonFile+" "+ hostsStatusJsonFile).read()
        # print(out)

        if mSR.gpsStatus(hostsStatusJsonFile):
            print("GPS Currently Active, Turning GPS Off")
            out = os.popen("ssh teamlary@"+ hostIP+' "cd /home/teamlary/gitHubRepos/minWeNodes/firmware/xu4Mqtt && ./gpsHalt.sh"').read()
            # print(out)

            time.sleep(0.1)
            out = os.popen('scp ' + gpsOffJsonFile + ' teamlary@' +hostIP+":"+statusJsonFile).read()
            #print()
            time.sleep(0.1)
          
            out = os.popen("ssh teamlary@"+ hostIP+' "cd /home/teamlary/gitHubRepos/minWeNodes/firmware/xu4Mqtt && nohup ./gpsReRun.sh >/dev/null 2>&1 &"').read()
            # print(out)
        else:
   
            print("GPS Currently Inactive, Turning GPS On")
            out = os.popen("ssh teamlary@"+ hostIP+' "cd /home/teamlary/gitHubRepos/minWeNodes/firmware/xu4Mqtt && ./gpsHalt.sh"').read()
            # print(out)
   
            time.sleep(0.1)
            out = os.popen('scp ' + gpsOnJsonFile + ' teamlary@' +hostIP+":"+statusJsonFile).read()
            #print(out)
            time.sleep(0.1)
            
            out = os.popen("ssh teamlary@"+ hostIP+' "cd /home/teamlary/gitHubRepos/minWeNodes/firmware/xu4Mqtt &&  nohup ./gpsReRun.sh >/dev/null 2>&1 &"').read()
            # print(out)
   
        out = os.popen('rsync -avzrtu -e "ssh" teamlary@' +hostIP+":"+statusJsonFile+" "+ hostsStatusJsonFile).read()
        print("Current GPS Status:", mSR.gpsStatus(hostsStatusJsonFile))



def main():
    hostFound,hostID,hostIP = getHostMac()
    gpsToggle(hostFound,hostIP)


if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    main()