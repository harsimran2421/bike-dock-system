#!/usr/bin/python

#References:
#    https://bradmontgomery.net/blog/sending-sms-messages-amazon-sns-and-python/
#    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
#    https://aws.amazon.com/sns/
#    https://stackoverflow.com/questions/35422490/pyqt5-add-image-in-background-of-mainwindow-layout
#     https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html
#     https://pimylifeup.com/raspberry-pi-rfid-rc522/ 

import sys
import datetime
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QWidget
from PyQt5.uic import loadUi
from PySide.QtCore import *
from PyQt5 import QtWidgets, QtGui, QtCore
from time import sleep
import boto3
from boto3.dynamodb.conditions import Key, Attr
from time import gmtime, strftime, sleep
from PyQt5.QtGui import QImage
#MQTT setup
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient 

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
continue_reading = True

dynamodb = boto3.resource('dynamodb')

myclient = AWSIoTMQTTClient("harry")
myclient.configureEndpoint("a3t3pe4wp4iz6-ats.iot.us-east-1.amazonaws.com", 8883)
myclient.configureCredentials("/home/pi/Desktop/final-project/aws_new/AmazonRootCA1.pem", "/home/pi/Desktop/final-project/aws_new/818af5f799-private.pem.key", "/home/pi/Desktop/final-project/aws_new/818af5f799-certificate.pem.crt")
myclient.configureAutoReconnectBackoffTime(1, 32, 20)
myclient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myclient.configureDrainingFrequency(2)  # Draining: 2 Hz
myclient.configureConnectDisconnectTimeout(10)  # 10 sec
myclient.configureMQTTOperationTimeout(5)  # 5 sec

myclient.connect()

global listA
global listB
global slot_inputvalue1
global slot_temp2
global flag
global test_flag
global rfid_value
global RFID_val
username_login_flag = 0
rfid_login_flag = 0
slot_value = 0
username = '' 
passwordc = ''
repeat_flag = 1
check_flag = 0
proj_flag = 0
login_flag = 1
conf_flag = 0
mobile_number = ""
first_name = ""


class initial_page(QtWidgets.QDialog):
    def __init__(self, parent= None):
        super(initial_page, self).__init__(parent)
        loadUi ('initial.ui',self)
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        self.setFont(font)
        self.setWindowOpacity(10.0)
        self.setStyleSheet("background-image: url(bike-dock-system1.jpg);\n"
                "")
        self.setWindowTitle('Options')
        self.username_button.clicked.connect(self.username_buttonc)  
        self.rfid_button.clicked.connect(self.rfid_buttonc)  

    def username_buttonc(self):
        global username_login_flag
        username_login_flag = 1
        self.accept()

    def rfid_buttonc(self):
        global rfid_login_flag
        rfid_login_flag = 1
        self.accept()

class Login_rfid(QtWidgets.QDialog):
    def __init__(self, parent= None):
        super(Login_rfid, self).__init__(parent)
        loadUi ('login_rfid.ui',self)
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        self.setFont(font)
        self.setWindowOpacity(10.0)
        self.setStyleSheet("background-image: url(bike-dock-system1.jpg);\n"
                "")
        self.setWindowTitle('Login!')
        self.scan_button.clicked.connect(self.login_compare)  
    def login_compare(self):
        self.scan_label.setText("currently scanning!!!")
        self.scan_label.repaint()
        global test_flag
        global slot_value
        global rfid_value
        global continue_reading
        TAGRead = MFRC522.MFRC522()
        while continue_reading:
            # Scan for cards   
            time.sleep(1)
            (status,TagType) = TAGRead.MFRC522_Request(TAGRead.PICC_REQIDL)
            # If a card is found
            if status == TAGRead.MI_OK:
                print ("Card detected")
    
            # Get the UID of the card
            (status,uid) = TAGRead.MFRC522_Anticoll()
            # If we have the UID, continue
            if status == TAGRead.MI_OK:
                rfid_value = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
                print(rfid_value)
                continue_reading = False
        table1 = dynamodb.Table('users')
        response = table1.scan(
                FilterExpression=Attr('RFID_value').eq(rfid_value)
                )
        items = response['Items']
        global username
        global password
        valid_flag = 0
        for i in items:
            print("entered for loop")
            valid_flag = 1
            username = i['first_name']
            password = i['last_name']
            if i['slot'] == '0' and i['RFID_value'] == rfid_value:
                test_flag = 1
                self.accept()
                break
            elif i['RFID_value'] == rfid_value:
                slot_value = i['slot']
                test_flag = 0
                self.accept()
                break
            else:
                print("Enetered else loop")
                QtWidgets.QMessageBox.warning(self,'Error','Invalid Entry')
                sys.exit(app.exec_())       
        if valid_flag == 0:
            print("Enetered else loop")
            QtWidgets.QMessageBox.warning(self,'Error','Invalid Entry')
            sys.exit(app.exec_())       
        print(items)

class Login(QtWidgets.QDialog):
    def __init__(self, parent= None):
        super(Login, self).__init__(parent)
        loadUi ('Final_project_Login.ui',self)
        self.setWindowTitle('Login!')
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        self.setFont(font)
        self.setWindowOpacity(0)
        self.setStyleSheet("background-image: url(bike-dock-system1.jpg);\n"
                "")
        self.pushButton1.clicked.connect(self.login_compare)  
        currentDT = datetime.datetime.now()
        self.label_4.setText(currentDT.strftime("%I:%M:%S %p"))
        self.label_4.repaint()
        self.label_6.setText(currentDT.strftime("%Y/%m/%d"))
        self.label_6.repaint()

    def login_compare(self):
        global test_flag
        global slot_value
        global username
        global password
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
                break
            elif i['last_name'] == password:
                slot_value = i['slot']
                test_flag = 0
                self.accept()
                break
        print(items)
            
class confirm(QDialog):
    def __init__(self):
        global first_name

        super(confirm, self).__init__()
        loadUi ('Final_project_Config.ui',self)
        self.setWindowTitle('Confirmation!')
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        self.setFont(font)
        self.setWindowOpacity(10.0)
        self.setStyleSheet("background-image: url(bike-dock-system1.jpg);\n"
                "")
        self.label_6.setText(first_name)
        self.label_6.repaint()
        currentDT = datetime.datetime.now()
        self.label_8.setText(currentDT.strftime("%I:%M:%S %p"))
        self.label_8.repaint()
        self.pushButton4.clicked.connect(self.on_pushButton4c_clicked)
        self.pushButton5.clicked.connect(self.on_pushButton5c_clicked)
    @pyqtSlot()
   
    def on_pushButton4c_clicked(self):
        global first_name
        global slot_inputvalue1
        global mobile_number
        message_value = "Booking complete for" + first_name + " Slot value: " + str (slot_inputvalue1) + " and dock 1"
        message = "{\"message_value\":\"" + message_value +"\",\"mobile_number\":\"" + mobile_number + "\"}"
        myclient.publish("harry_policy_new",message, 0)
        self.accept()
    def on_pushButton5c_clicked(self):
        self.accept()
        
class checkout(QDialog):
    def __init__(self):
        super(checkout, self).__init__()
        loadUi ('Final_project_Checkout.ui',self)
        global slot_value
        global username
        global password
        self.setWindowTitle('Checkout!')
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        self.setFont(font)
        self.setWindowOpacity(10.0)
        self.setStyleSheet("background-image: url(bike-dock-system1.jpg);\n"
                "")
        self.checkout_username.setText(username)
        self.checkout_slot.setText(str(slot_value))
        self.checkout_dock.setText("1")
        self.checkout_yes.clicked.connect(self.on_checkout_yesc_clicked)
        self.checkout_no.clicked.connect(self.on_checkout_noc_clicked)

    def on_checkout_yesc_clicked(self): 
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
        message_value = "Checkout complete for" + first_name + " Slot value: " + str (slot_inputvalue1) + " and dock 1"
        message = "{\"message_value\":\"" + message_value +"\",\"mobile_number\":\"" + mobile_number + "\"}"
        myclient.publish("harry_policy_new",message, 0)
        login_flag = 1
        repeat_flag = 1
        QtWidgets.QMessageBox.warning(self,'Checkout complete','Checkout complete!!!!!')
        sys.exit(app.exec_())

    def on_checkout_noc_clicked(self):
        self.accept()
class project(QDialog):
    def __init__(self):
        super(project, self).__init__()
        loadUi ('Final_project.ui',self)
        self.setWindowTitle('Welcome!')
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        self.setFont(font)
        self.setWindowOpacity(10.0)
        currentDT = datetime.datetime.now()
        self.label_9.setText(currentDT.strftime("%I:%M:%S %p"))
        self.label_9.repaint()
        self.label_11.setText(currentDT.strftime("%Y/%m/%d"))
        self.label_11.repaint()

#        self.setStyleSheet("background-image: url(bike-dock-system1.jpg);\n"
#               "")
#        self.setStyleSheet("font-color: rgb(0,0,0);\n"
#                "")
        self.pushButton2.clicked.connect(self.on_pushButton2c_clicked)
        self.pushButton3.clicked.connect(self.on_pushButton3c_clicked)
        self.pushButton.clicked.connect(self.on_pushButtonc_clicked)
        table = dynamodb.Table('Availability')
        response = table.scan(
                FilterExpression=Attr('booking').eq("available") & Attr('dock').eq(1)
                )
        items = response['Items']
        print(items)
        self.spinBox1.setValue(0)
        self.spinBox2.setValue(1)
        self.slot1.setStyleSheet("background-color: rgb(128, 0, 0);\n")
        self.slot2.setStyleSheet("background-color: rgb(128, 0, 0);\n")
        self.slot3.setStyleSheet("background-color: rgb(128, 0, 0);\n")
        self.slot4.setStyleSheet("background-color: rgb(128, 0, 0);\n")
        self.slot5.setStyleSheet("background-color: rgb(128, 0, 0);\n")
        self.slot6.setStyleSheet("background-color: rgb(128, 0, 0);\n")
        self.slot7.setStyleSheet("background-color: rgb(128, 0, 0);\n")
        self.slot8.setStyleSheet("background-color: rgb(128, 0, 0);\n")
        self.slot9.setStyleSheet("background-color: rgb(128, 0, 0);\n")
        for i in items:
            if i['slot'] == 1:
            #    self.slot1.setText("A")
                self.slot1.setStyleSheet("background-color: rgb(0, 128, 0);\n")
            elif i['slot'] == 2:
             #   self.slot2.setText("A")
                self.slot2.setStyleSheet("background-color: rgb(0, 128, 0);\n")
            elif i['slot'] == 3:
              #  self.slot3.setText("A")
                self.slot3.setStyleSheet("background-color: rgb(0, 128, 0);\n")
        global slot_temp2
        global slot_inputvalue1            
    @pyqtSlot()            
                          
    def on_pushButtonc_clicked(self):
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
            self.slot1.setStyleSheet("background-color: rgb(128, 0, 0);\n")
            self.slot2.setStyleSheet("background-color: rgb(128, 0, 0);\n")
            self.slot3.setStyleSheet("background-color: rgb(128, 0, 0);\n")
            self.slot4.setStyleSheet("background-color: rgb(128, 0, 0);\n")
            self.slot5.setStyleSheet("background-color: rgb(128, 0, 0);\n")
            self.slot6.setStyleSheet("background-color: rgb(128, 0, 0);\n")
            self.slot7.setStyleSheet("background-color: rgb(128, 0, 0);\n")
            self.slot8.setStyleSheet("background-color: rgb(128, 0, 0);\n")
            self.slot9.setStyleSheet("background-color: rgb(128, 0, 0);\n")
            for i in items:
                if i['slot'] == 1:
                    self.slot1.setStyleSheet("background-color: rgb(0, 128, 0);\n")
                    self.slot1.repaint()
                elif i['slot'] == 2:
                    self.slot2.setStyleSheet("background-color: rgb(0, 128, 0);\n")
                    self.slot2.repaint()
                elif i['slot'] == 3:
                    self.slot3.setStyleSheet("background-color: rgb(0, 128, 0);\n")
                    self.slot3.repaint()
            slot_temp2 = 0
            flag = 0
        print(items)

    def on_pushButton2c_clicked(self):
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
            print(mobile_number)
            # Send your sms message by publishing it to mqtt.
            message_value = "Booking complete for" + first_name + " Slot value: " + str (slot_inputvalue1) + " and dock 1"
            message = "{\"message_value\":\"" + message_value +"\",\"mobile_number\":\"" + mobile_number + "\"}"
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self,'Unavailable','Not Empty!')
            
    def on_pushButton3c_clicked(self):
        sys.exit(app.exec_())

class unlock_slot(QDialog):
    def __init__(self):
        super(unlock_slot, self).__init__()
        loadUi ('unlock.ui',self)
        self.setWindowTitle('unlock window')
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        self.setFont(font)
        self.setWindowOpacity(10.0)
        self.setStyleSheet("background-image: url(bike-dock-system1.jpg);\n"
                "")

        self.unlock_button.clicked.connect(self.on_unlock_buttonc_clicked)
        self.timer_value.setValue(10) 
        self.status_label.setText("Closed!")

    def on_unlock_buttonc_clicked(self):
        timer_val = self.timer_value.value() 
        self.status_label.setText("open")
        self.status_label.repaint()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(11,GPIO.OUT)
        GPIO.output(11,GPIO.HIGH)
        sleep(timer_val)
        GPIO.output(11,GPIO.LOW)
        self.status_label.setText("Closed")
        self.accept()

app = QApplication(sys.argv)
Initial = initial_page()
if Initial.exec_() == QtWidgets.QDialog.Accepted:
    if username_login_flag == 1:
        login = Login()
        if login.exec_() == QtWidgets.QDialog.Accepted:
            if test_flag == 1:
                w = project()
                w.show()
                if w.exec_() == QtWidgets.QDialog.Accepted:
                    x=confirm()
                    x.show()
                    if x.exec_() == QtWidgets.QDialog.Accepted: 
                        sys.exit(app.exec_())
            elif test_flag == 0:
                w = checkout()
                w.show()
                if w.exec_() == QtWidgets.QDialog.Accepted:
                    unlock_val = unlock_slot()
                    if unlock_val.exec_() == QtWidgets.QDialog.Accepted:
                        sys.exit(app.exec_())
    elif rfid_login_flag == 1:
        login = Login_rfid()
        if login.exec_() == QtWidgets.QDialog.Accepted:
            if test_flag == 1:
                w = project()
                w.show()
                if w.exec_() == QtWidgets.QDialog.Accepted:
                    x=confirm()
                    x.show()
                    if x.exec_() == QtWidgets.QDialog.Accepted: 
                        sys.exit(app.exec_())
            elif test_flag == 0:
                w = checkout()
                w.show()
                if w.exec_() == QtWidgets.QDialog.Accepted:
                    unlock_val = unlock_slot()
                    if unlock_val.exec_() == QtWidgets.QDialog.Accepted:
                        sys.exit(app.exec_())
