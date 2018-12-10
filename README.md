Repo for Embedded Interface Design Super Project

Author: 
	1. Harsimransingh Bindra
	2. Yasir Aslam Shah
	3. Sharanjeet Singh Mago

Date: 12/29/2018

Execution Instructions:

1. To run the ‘Automated Dock System’ Application on the Dock Console (Touch pad System) double click the icon with title ‘Automated Dock System’

2. To access the website on any system , click “ Automated Dock System” or click the link as http://bike-dock-system.s3-website-us-east-1.amazonaws.com/

Project Description:

In this project,there are three modules that work together forming our Automated Bike System .The first module is a Qt based application that is installed on Dock console and contains a UI interface allowing a user to book and checkout any slot. The other module is a website that allows a user to book a slot or checkout any slot remotely from a website. The third module is a dynamo Database that works coherently with both the website as well as the QtPy. In this project we have implemented DynamoDB, Lambda function, MQTT,websockets, SNS(Amazon Web Service SMS Service) and SPI. 

Key Elements:

Python and Node.js Elements: Various modules of project are written in Python . Python language is used for RFID module interfacing, QtPy application, MQTT & Lambda function interfacing and database creation & integration. Node.js is used to write the lambda function for database integration with the website.

QT and HTML Uis: PyQt application is used to create UIs to interact with users at Dock locations. The program for QtPy5 is written in Python and allows a user to sign in into the system and book a slot or check one out. HTMl Uis are used for webpage creation, formatting and database operations.

Communication protocols: In this project, various communication protocols are implemented as MQTT, SPI, HTTP,interfacing various hardware and software modules.

Two RPI3s are used as two Dock modules with PyQt loaded for user interaction while booking, checkout or opening of a dedicated slots.

Message Queuing : SNS simple Notification Services is used to notify a user using SMS service. SNS itself has its own messaging queuing service.

AWS IoT framework services: 
	- DynamoDB service
	- S3 bucket service
	- API gateway
	- Lambda function
	- SNS(simple notification service)
	- MQTT service
	- Python SDk

References:
	- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
	- https://aws.amazon.com/sns/
	- https://stackoverflow.com/questions/35422490/pyqt5-add-image-in-background-of-mainwindow-layout
	- https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html
	- https://pimylifeup.com/raspberry-pi-rfid-rc522/ 
	- https://www.youtube.com/watch?v=Byhg9BBsbJw
	- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/CurrentAPI.html 
	- https://en.wikipedia.org/wiki/Amazon_DynamoDB
	- https://aws.amazon.com/dynamodb/
	- https://aws.amazon.com/s3/
	- https://aws.amazon.com/api-gateway/

Extra Features:
	- website hosting on S3 bucket for to make it serverless
	- using python SDK in addition to MQTT communication service
	- Making use of DynamoDB AWS service as a alternative to use local database to avoi a single point of failure
	- Used Custom stylesheets to improve the UI of the website
