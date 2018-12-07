
'''
References:
    https://bradmontgomery.net/blog/sending-sms-messages-amazon-sns-and-python/

'''



import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from PySide.QtCore import *
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from time import sleep
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

client = boto3.client(
        "sns",
        aws_access_key_id =
        aws_secret_access_key = 
        region_name=
        )


global listA
global listB
global slot_inputvalue1
global slot_temp2
global flag
global test_flag
slot_value = 0
username = '' 
passwordc = ''
global RFID_val
repeat_flag = 1
check_flag = 0
proj_flag = 0
login_flag = 1
conf_flag = 0
mobile_number = ""
first_name = ""

class Login(QtWidgets.QDialog):
    def __init__(self, parent= None):
        super(Login, self).__init__(parent)
        loadUi ('Final_project_Login.ui',self)
        self.setWindowTitle('Login!')
        self.pushButton1.clicked.connect(self.login_compare)  
    def login_compare(self):
        global test_flag
        global slot_value
        global username
        global password
        global repeat_flag
        global check_flag
        global proj_flag
        username = self.inputuser.text()
        password = self.inputpswd.text()
        table1 = dynamodb.Table('users')
        response = table1.scan(
                FilterExpression=Attr('email_id').eq(username)
                )
        items = response['Items']
        for i in items:
            if i['last_name'] != password:
                QtWidgets.QMessageBox.warning(self,'Error','Invalid Entry')
                sys.exit(app.exec_())       
            elif i['slot'] == '0' and i['last_name'] == password:
                test_flag = 1
                self.accept()
                repeat_flag = 1
                proj_flag = 1
                break
            elif i['last_name'] == password:
                slot_value = i['slot']
                self.accept()
                test_flag = 0
                repeat_flag = 1
                check_flag = 1
                break
        print(items)
#        if (self.inputuser.text() == '111' and self.inputpswd.text() == '111'):
#            self.accept()
#        else:
#            QtWidgets.QMessageBox.warning(self,'Error','Invalid Entry')
#            sys.exit(app.exec_())

            
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
        global login_flag
        global repeat_flag
        login_flag = 1
        repeat_flag = 1
    def on_pushButton5_clicked(self):
        global login_flag
        global repeat_flag
        login_flag = 1
        repeat_flag = 1

class checkout(QDialog):
    def __init__(self):
        super(checkout, self).__init__()
        loadUi ('Final_project_Checkout.ui',self)
        global slot_value
        global username
        global password
        self.setWindowTitle('Checkout!')
        self.checkout_username.setText(username)
        self.checkout_slot.setText(str(slot_value))
        self.checkout_dock.setText("1")
        self.checkout_yes.clicked.connect(self.on_checkout_yes_clicked)
        self.checkout_no.clicked.connect(self.on_checkout_no_clicked)

    def on_checkout_yes_clicked(self): 
        global login_flag
        global repeat_flag
        global username
        global slot_value
        global mobile_number
        global first_name
        table = dynamodb.Table('Availability')
        table1 = dynamodb.Table('users')
        response = table1.scan(
                FilterExpression=Attr('email_id').eq(username)
                )
        items = response['Items']
        global RFID_val
        for i in items:
           RFID_val = i['RFID_value']
           mobile_number = i['mobile_number']
           first_name = i['first_name']
        print("RFID value: " + RFID_val)
        print("username" + username)
        print("slot_value" + str(slot_value))
        slot_inputvalue1 = int(slot_value)
        table.update_item(
                Key={
                    'dock': 1,
                    'slot': slot_inputvalue1
                    },
                UpdateExpression='SET booking = :val1',
                ExpressionAttributeValues={
                    ':val1': 'available'
                    }
                )
        table1.update_item(
                Key={
                    'email_id': username,
                    'RFID_value': RFID_val
                    },
                UpdateExpression='SET dock = :val1',
                ExpressionAttributeValues={
                    ':val1': '0'
                    }
                )
        table1.update_item(
                Key={
                    'email_id': username,
                    'RFID_value': RFID_val
                    },
                UpdateExpression='SET slot = :val1',
                ExpressionAttributeValues={
                    ':val1': '0'
                    }
                )
        client.publish(
        PhoneNumber = mobile_number,
        Message = "Check out complete"
        )
        login_flag = 1
        repeat_flag = 1
    def on_checkout_no_clicked(self):
        global login_flag
        global repeat_flag
        login_flag = 1
        repeat_flag = 1
      # sys.exit(app.exec_())

class project(QDialog):
    def __init__(self):
        super(project, self).__init__()
        loadUi ('Final_project.ui',self)
        self.setWindowTitle('Welcome!')
        self.pushButton2.clicked.connect(self.on_pushButton2_clicked)
        self.pushButton3.clicked.connect(self.on_pushButton3_clicked)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        table = dynamodb.Table('Availability')
        response = table.scan(
                FilterExpression=Attr('booking').eq("available") & Attr('dock').eq(1)
                )
        items = response['Items']
        print(items)
        self.spinBox1.setValue(0)
        self.spinBox2.setValue(1)
        self.slot4.setText("X")
        self.slot5.setText("X")
        self.slot6.setText("X")
        self.slot7.setText("X")
        self.slot8.setText("X")
        self.slot9.setText("X")
        self.slot1.setText("X")
        self.slot2.setText("X")
        self.slot3.setText("X")
        for i in items:
            if i['slot'] == 1:
                self.slot1.setText("A")
            elif i['slot'] == 2:
                self.slot2.setText("A")
            elif i['slot'] == 3:
                self.slot3.setText("A")
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
        global table
        condition = "true"
        slot_inputvalue1= self.spinBox1.value()
        print("User selected Slot \t" + str(slot_inputvalue1))
        table = dynamodb.Table('Availability')
        table1 = dynamodb.Table('users')
        response = table.scan(
                FilterExpression=Attr('booking').eq("available") & Attr('dock').eq(1)
                )
        items = response['Items']
        for i in items:
            print(i['slot'])
            print(slot_inputvalue1)
            if i['slot'] == slot_inputvalue1:
                condition = "true"
                print("making condition true")
                break
            else:
                condition = "false"
        if condition == "true":
            self.labelstatus.setText("Available")
            flag=1
            slot_temp2 = 1
            print("Lets confirm this")
        else:
            self.labelstatus.setText("Occupied")
            self.slot4.setText("X")
            self.slot5.setText("X")
            self.slot6.setText("X")
            self.slot7.setText("X")
            self.slot8.setText("X")
            self.slot9.setText("X")
            self.slot1.setText("X")
            self.slot2.setText("X")
            self.slot3.setText("X")
            for i in items:
                if i['slot'] == 1:
                    self.slot1.setText("A")
                elif i['slot'] == 2:
                    self.slot2.setText("A")
                elif i['slot'] == 3:
                    self.slot3.setText("A")
            slot_temp2 = 0
            flag = 0
        print(items)

    def on_pushButton2_clicked(self):
        global slot_inputvalue1
        global slot_temp2
        global flag
        global username
        global mobile_number
        global first_name
        table = dynamodb.Table('Availability')
        table1 = dynamodb.Table('users')

        global RFID_val

        if (slot_inputvalue1 and slot_temp2 and flag):
            response = table1.scan(
                FilterExpression=Attr('email_id').eq(username)
                )
            items = response['Items']
            for i in items:
                RFID_val = i['RFID_value']
                username = i['email_id']
                mobile_number = i['mobile_number']
                first_name = i['first_name']
            table.update_item(
                    Key={
                        'dock': 1,
                        'slot': slot_inputvalue1
                        },
                    UpdateExpression='SET booking = :val1',
                    ExpressionAttributeValues={
                        ':val1': 'booked'
                        }
                    )
            table1.update_item(
                    Key={
                        'email_id': username,
                        'RFID_value': RFID_val
                        },
                    UpdateExpression='SET dock = :val1',
                    ExpressionAttributeValues={
                        ':val1': '1'
                        }
                    )
            table1.update_item(
                    Key={
                        'email_id': username,
                        'RFID_value': RFID_val
                        },
                    UpdateExpression='SET slot = :val1',
                    ExpressionAttributeValues={
                        ':val1': str(slot_inputvalue1)
                        }
                    )
            message_value = "Hello " + first_name + " Slot number: " + str(slot_inputvalue1) + " is booked at Dock number: 1"
            print(mobile_number)
            # Send your sms message.
            client.publish(
                PhoneNumber = mobile_number,
                Message = message_value
            )
            #self.accept()
            global conf_flag
            global repeat_flag
            conf_flag = 1
            repeat_flag = 1
        else:
            QtWidgets.QMessageBox.warning(self,'Unavailable','Not Empty!')
            
    def on_pushButton3_clicked(self):
        global login_flag
        global repeat_flag
        login_flag = 1
        repeat_flag = 1
        #sys.exit(app.exec_())


app = QApplication(sys.argv)

conf = confirm()
check = checkout()
proj= project()
login = Login()
'''
while 1:
    if login_flag == 1 and repeat_flag == 1:
        login.show()
        proj.hide()
        check.hide()
        conf.hide()
        login_flag = 0
        repeat_flag = 0
    elif proj_flag == 1 and repeat_flag == 1:
        login.hide()
        proj.show()
        check.hide()
        conf.hide()
        proj_flag = 0
        repeat_flag = 0
    elif check_flag == 1 and repeat_flag == 1:
        login.hide()
        proj.hide()
        check.show()
        conf.hide()
        check_flag = 0
        repeat_flag = 0
    elif conf_flag == 1 and repeat_flag == 1:
        login.hide()
        proj.hide()
        check.hide()
        conf.show()
        conf_flag = 0
        repeat_flag = 0
    sleep(0.5)
'''
if login.exec_() == QtWidgets.QDialog.Accepted:
    if test_flag == 1:
        w = project()
        w.show()
    elif test_flag == 0:
        w = checkout()
        w.show()
    if w.exec_() == QtWidgets.QDialog.Accepted:
        x=confirm()
        x.show()
