# # Import tkinter and webview libraries
# from tkinter import *
# import webview
  
# # define an instance of tkinter
# tk = Tk()
  
# #  size of the window where we show our website
# tk.geometry("800x450")
  
# # Open website
# webview.create_window('MINTS', 'http://mdash.circ.utdallas.edu:3000/d/central_node_demo/central-node-demo?orgId=1&refresh=5s')
# webview.start()
from PyQt5 import QtWidgets, QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys


class wearableWindow(QMainWindow):
    def __init__(self):
        super(wearableWindow, self).__init__()
        self.setStyleSheet("background-color: black;")
        self.setGeometry(100,100,1920,75)
        self.setWindowTitle("MINTS Wearable EOD 001")
       
        self.initUI()

    def initUI(self):

        # creating label for the UTD Logo 
        self.utdLogo = QLabel(self)
        self.utdLogo.setGeometry(QtCore.QRect(0,0,75,75))
        self.utdLogo.setText("")
        self.utdLogo.setPixmap(QtGui.QPixmap('res/utd.png'))
        self.utdLogo.setScaledContents(True)
        self.utdLogo.setObjectName("UTD Logo")
        
        # creating label for the Mints Logo 
        self.mintsLogo = QLabel(self)
        self.mintsLogo.setGeometry(QtCore.QRect(1920-75,0,75,75))
        self.mintsLogo.setText("")
        self.mintsLogo.setPixmap(QtGui.QPixmap('res/mi3nts.png'))
        self.mintsLogo.setScaledContents(True)
        self.mintsLogo.setObjectName("Mints Logo")

        self.utdText = QtWidgets.QLabel(self)
        self.utdText.setText("The University of Texas at Dallas")
        self.utdText.setStyleSheet("background:gray") 
        self.utdText.move(75,50)

        # self.gpsButton = QtWidgets.QPushButton(self)
        # self.gpsButton.setText("GPS Toggle")
        # self.gpsButton.clicked.connect(self.clicked)
        # self.gpsButton.move(150,50)

    def clicked(self):
        self.label.setText("You Pressed the Button")
        self.update()

    def update(self):
        self.label.adjustSize()
    
    
def window():
    app = QApplication(sys.argv)
    win = wearableWindow()
    win.show()
    sys.exit(app.exec_())

window()




