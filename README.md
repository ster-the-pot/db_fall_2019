# db_fall_2019
Database Biology Web Application

1.	RUNNING THE PROGRAM (FOR ADMINISTRATOR)
To get started, ensure you have a server with a python3 run-time environment installed and ready. Furthermore, if you wish to share the application across your network firewall rules should allow port 5000 (python can be configured to run the application on port 80)
Git link: https://github.com/ster-the-pot/db_fall_2019
A.	Connecting to the Database
The database is held in AWS at the address of  18.224.202.17 (on MYSQL port 3306). To configure the application to run on your own custom database, configure location and login credentials in the src/query.py file. 
B.	Preparing your run-time environment involves installing the following dependencies. (The recommended install agent is pip3
•	Mysql.connector
•	Flask web server
•	WTForms
All application specific code resides within the project directory. Python/Flask specific GUI related code is located in root folder, backed and database specific code is located under Backend/, and .html files as well as Flask specific jinja markup may be found in the /templates and /templates/includes directories. 
2.	USING THE PROGRAM (FOR CLIENTS AND USERS)
To begin, open your web browser of choice and visit localhost/5000 (the application has been most heavily tested under google chrome and is assured to work in this environment)


A.	Inputting Data
All data input operations may be performed from the /input page. This includes manual input of conditions, measurements, sequences, and experiments as well as automated CSV input of the data. NOTE: Before inputting experiments through the CSV or the online GUI, ensure all relevant condition types, measurement types, and possible sequences are inserted through the user interface.
B.	Querying Data
i.	Experiment Info:
The first page that may be used to query data is the Experiment info page. To visit this page, click it at the top navigation bar. Upon visiting the page, you will be presented with a dialogue to insert an experiment. In this dialogue you will input the sequence in question as well as the relevant conditions. Upon submission, the page will then show all measurements stored for said experiment. This page is great for identifying any experiment results that have been input. 
ii.	Side-By-Side
The second Query page, Side-By-Side, is similar to the Experiment Info page, however it allows for insertion of two experiments. A dialogue will appear allowing for the querying of all relevant conditions from both experiments, and once submitted the system will calculate all measurements common to the two experiments. This will be displayed in a table and may be printed using your browser of choice. 

