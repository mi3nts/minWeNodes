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

dataFolder     = mD.dataFolder
gpsPort        = mD.gpsPort
statusJsonFile = mD.statusJsonFile
hostsFile      = mD.hostsFile


hosts       = yaml.load(open(hostsFile))

def getHostMac():
    scanner = nmap.PortScanner()
    hostNodes = hosts['nodeIDs']
    for hostIn in hostNodes:
        ipAddress = hostIn['IP']    
        host = socket.gethostbyname(ipAddress)
        scanner.scan(host, '1', '-v')
        ipState = scanner[host].state()
        print("IP Status: ", scanner[host].state())
        if ipState == "up":
            print("ssh teamlary@"+ ipAddress+' "cat /sys/class/net/eth0/address"')
            hostID = os.popen("ssh teamlary@"+ ipAddress+' "cat /sys/class/net/eth0/address"').read().replace(":","").replace(" ","")
            print(hostID)
            print(hostIn['nodeID'])
            print(hostIn['nodeID']== str(hostID))
            if hostID == hostIn['nodeID']:
                print("Host " + hostID + " found @" + ipAddress) 
                return True, hostID;
            else:
                print("Host " + hostID + " found with incorrect IP:" + ipAddress)
                return False, 0;
    print("No Host found")                
    return False, -1;
     


def main():
    hostFound,hostID = getHostMac()
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