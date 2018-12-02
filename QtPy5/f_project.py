import sys
import Adafruit_DHT
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from PySide.QtCore import *
from PyQt5 import QtCore
from PyQt5 import QtWidgets
global listA
global listB
global slot_inputvalue1
global slot_temp2
global flag
class Login(QtWidgets.QDialog):
    def __init__(self, parent= None):
        super(Login, self).__init__(parent)
        loadUi ('Final_project_Login.ui',self)
        self.setWindowTitle('Login!')
        self.pushButton1.clicked.connect(self.login_compare)  
    def login_compare(self):
        if (self.inputuser.text() == '111' and self.inputpswd.text() == '111'):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self,'Error','Invalid Entry')
            sys.exit(app.exec_())

            
class confirm(QDialog):
    def __init__(self):
        super(confirm, self).__init__()
        loadUi ('Final_project_Config.ui',self)
        self.setWindowTitle('Confirmation!')
        self.pushButton4.clicked.connect(self.on_pushButton4_clicked)
        self.pushButton5.clicked.connect(self.on_pushButton5_clicked)
        self.on_pushButton4_clicked()        
    
    @pyqtSlot()
   
    def on_pushButton4_clicked(self):
        self.label_6.setText("Yasir")            
    def on_pushButton5_clicked(self):
        self.accept()

class project(QDialog):
    def __init__(self):
        super(project, self).__init__()
        loadUi ('Final_project.ui',self)
        self.setWindowTitle('Welcome!')
        self.pushButton2.clicked.connect(self.on_pushButton2_clicked)
        self.pushButton3.clicked.connect(self.on_pushButton3_clicked)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.spinBox1.setValue(0)
        self.slot1.setText("A")
        self.slot2.setText("X")
        self.slot3.setText("X")
        self.slot4.setText("X")
        self.slot5.setText("X")
        self.slot6.setText("X")
        self.slot7.setText("X")
        self.slot8.setText("X")
        self.slot9.setText("X")
        #slot_inputvalue2
        #self.slot10.setText("0")
        #slot_inputvalue1
        global slot_temp2
        global slot_inputvalue1            
    @pyqtSlot()            
                          
    def on_pushButton_clicked(self):
        global slot_inputvalue1
        global slot_temp2
        global flag
        slot_inputvalue1= self.spinBox1.value()
        print("User selected Slot \t")
        print(slot_inputvalue1)
        if(slot_inputvalue1 ==1):
            slot_temp2 = 1
            print("one\n")
            flag=1
            self.labelstatus.setText("Available")
        elif(slot_inputvalue1 == 2):
            slot_temp2 = 0
            print("two\n")
            flag=0
            self.labelstatus.setText("Occupied")
        elif(slot_inputvalue1 == 3):
            slot_temp2 = self.slot3.Text()
            print("three\n")
        else:
            slot_temp2 = 1
            print("poly\n")
            self.labelstatus.setText("Occupied")


        print("\nslot is")
        print(slot_temp2)

            
    def on_pushButton2_clicked(self):
        if (slot_inputvalue1 and slot_temp2 and flag):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self,'Unavailable','Not Empty!')
            
    def on_pushButton3_clicked(self):
        sys.exit(app.exec_())


app = QApplication(sys.argv)
login = Login()

if login.exec_() == QtWidgets.QDialog.Accepted:
    w = project()
    w.show()
    if w.exec_() == QtWidgets.QDialog.Accepted:
        x=confirm()
        x.show()
        if x.exec_() == QtWidgets.QDialog.Accepted:
            z=Login()
            z.show()
    sys.exit(app.exec_())
