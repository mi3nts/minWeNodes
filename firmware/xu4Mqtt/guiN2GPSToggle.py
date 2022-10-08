# # Import tkinter and webview libraries
# from tkinter import *
# import webview
  
# # define an instance of tkinter
# tk = Tk()
  
# #  size of the window where we show our website
# tk.geometry("800x450")
# Import tkinter and webview libraries
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
import time
from collections import OrderedDict
from os import listdir
from os.path import isfile, join
from mintsXU4 import mintsLatest as mL
import os 
import nmap, socket
import yaml
import json

# # Open website
# webview.create_window('MINTS', 'http://mdash.circ.utdallas.edu:3000/d/central_node_demo/central-node-demo?orgId=1&refresh=5s')
# webview.start()
from PyQt5 import QtWidgets, QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl
import sys

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

class wearableWindow(QMainWindow):
    def __init__(self):
        super(wearableWindow, self).__init__()
        self.setStyleSheet("background-color: black;")
        self.setGeometry(0,1080-50,1920,50)
        self.setWindowTitle("MINTS Wearable EOD 001")
       
        self.initUI()

    def initUI(self):

        # creating label for the UTD Logo 
        self.utdLogo = QLabel(self)
        self.utdLogo.setGeometry(QtCore.QRect(1920-95,0,50,50))
        self.utdLogo.setText("")
        self.utdLogo.setPixmap(QtGui.QPixmap('res/utd.png'))
        self.utdLogo.setScaledContents(True)
        self.utdLogo.setObjectName("UTD Logo")
        
        # creating label for the Mints Logo 
        self.mintsLogo = QLabel(self)
        self.mintsLogo.setGeometry(QtCore.QRect(1920-50,0,50,50))
        self.mintsLogo.setText("")
        self.mintsLogo.setPixmap(QtGui.QPixmap('res/mi3nts.png'))
        self.mintsLogo.setScaledContents(True)
        self.mintsLogo.setObjectName("Mints Logo")


        self.infoTextUTD = QtWidgets.QLabel(self)
        self.infoTextUTD.setGeometry(QtCore.QRect(1920-1000,0,50,50))
        self.infoTextUTD.setText("The University of Texas at Dallas\n https://mints.utdallas.edu/")
        self.infoTextUTD.setStyleSheet("color: grey;") 
        self.infoTextUTD.adjustSize()
        # self.infoTextUTD.move(75,55)
    
        self.infoTextMints = QtWidgets.QLabel(self)
        self.infoTextMints.setGeometry(QtCore.QRect(1920-1000,25,50,50))
        self.infoTextMints.setText("Multi-Scale Integrated Interactive Intelligent Sensing & Simulation for Actionable Insights in Service of Society\n https://mints.utdallas.edu/")
        self.infoTextMints.setStyleSheet("color: grey;") 
        self.infoTextMints.adjustSize()
        # self.infoTextMints.move(75,55)
 
        self.gpsButton = QtWidgets.QPushButton(self)
        self.gpsButton.setGeometry(QtCore.QRect(5,5,400,40))        
        self.gpsButton.setText("GPS")
        self.gpsButton.setStyleSheet("color: white;") 
        self.gpsButton.clicked.connect(self.mainGPS)
        
        # creating label for the Mints Logo 
        self.statusBar = QtWidgets.QLabel(self)
        self.statusBar.setGeometry(QtCore.QRect(405,5,510,50))
        self.statusBar.setText("MINTS Wearable EOD 001")
        self.statusBar.setStyleSheet("color: white;") 
        self.statusBar.adjustSize()
        # self.statusBar.move(200,12)

    def mainGPS(self):
        hostFound,hostID,hostIP =  self.getHostMac()
        self.gpsToggle(hostFound,hostID,hostIP)

    
    def getHostMac(self):
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

    def readLatestTime(self,hostID,sensorID):
        
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
    
    def writeLatestTime(self,hostID,sensorID,dateTime):
        fileName = latestFolder + "/" + hostID+"_"+sensorID+".json"
        mSR.directoryCheck2(fileName)
        sensorDictionary = OrderedDict([
                    ("dateTime"            ,str(dateTime))
                    ])
        with open(fileName, "w") as outfile:
            json.dump(sensorDictionary,outfile)



    def gpsToggle(self,hostFound,hostID,hostIP):
        if hostFound:
            mSR.directoryCheck2(hostsStatusJsonFile)
            out = os.popen('rsync -avzrtu -e "ssh" teamlary@' +hostIP+":"+statusJsonFile+" "+ hostsStatusJsonFile).read()
            # print(out)
            dateTime = datetime.datetime.now() 
            if mSR.gpsStatus(hostsStatusJsonFile):
                print("GPS Currently Active, Turning GPS Off")
                out = os.popen("ssh teamlary@"+ hostIP+' "cd ' + repos + 'minWeNodes/firmware/xu4Mqtt && ./gpsHalt.sh"').read()
                # print(out)
                time.sleep(0.1)
                out = os.popen('scp ' + gpsOffJsonFile + ' teamlary@' +hostIP+":"+statusJsonFile).read()
                #print()
                time.sleep(0.1)
                out = os.popen("ssh teamlary@"+ hostIP+' "cd ' + repos + 'minWeNodes/firmware/xu4Mqtt && nohup ./gpsReRun.sh >/dev/null 2>&1 &"').read()
                # print(out)
                
                sensorDictionary = OrderedDict([
                    ("dateTime"            ,str(dateTime)),
                    ("status"              ,str(12))
                    ])

                mL.writeMQTTLatestWearable(sensorDictionary,"MWS001",hostID) 

            else:
    
                print("GPS Currently Inactive, Turning GPS On")
                out = os.popen("ssh teamlary@"+ hostIP+' "cd ' + repos + 'minWeNodes/firmware/xu4Mqtt && ./gpsHalt.sh"').read()
                # print(out)
                time.sleep(0.1)
                out = os.popen('scp ' + gpsOnJsonFile + ' teamlary@' +hostIP+":"+statusJsonFile).read()
                #print(out)
                time.sleep(0.1)
                out = os.popen("ssh teamlary@"+ hostIP+' "cd ' + repos + 'minWeNodes/firmware/xu4Mqtt &&  nohup ./gpsReRun.sh >/dev/null 2>&1 &"').read()
                # print(out)
                
                sensorDictionary = OrderedDict([
                    ("dateTime"            ,str(dateTime)),
                    ("status"              ,str(11))
                    ])
                mL.writeMQTTLatestWearable(sensorDictionary,"MWS001",hostID) 
            out = os.popen('rsync -avzrtu -e "ssh" teamlary@' +hostIP+":"+statusJsonFile+" "+ hostsStatusJsonFile).read()
            print("Current GPS Status:", mSR.gpsStatus(hostsStatusJsonFile))
        else:
            print("No Host Found")
        

    
def window():
    app = QApplication(sys.argv)
    win = wearableWindow()
    win.show()
    sys.exit(app.exec_())

window()




