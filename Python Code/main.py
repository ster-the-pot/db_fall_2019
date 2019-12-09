import mysql.connector as mysql
import pandas as pd

mydb = mysql.connect(
    host="18.224.202.17",
    user="pythonApp",
    passwd="bryceSterlingDB"
)

cursor = mydb.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS GeneExpression")

cursor.execute("CREATE TABLE IF NOT EXISTS Sequences "
               "(Name varchar(255) PRIMARY KEY,"
               "Description varchar(255),"
               "File_Name varchar(255))")

cursor.execute("CREATE TABLE IF NOT EXISTS Condition_Domains "
               "(Condition Varchar(255) PRIMARY KEY,"
               "Domain Varchar(255))")

cursor.execute("CREATE TABLE IF NOT EXISTS Measurement_Domains"
               "(Measurement Varchar(255) PRIMARY KEY,"
               "Domain Varchar(255))")

cursor.execute("CREATE TABLE IF NOT EXISTS Experiment_Int"
               "(Experiment_ID Int NOT NULL AUTO_INCREMENT,"
               "Sequence varchar(255),"
               "Condition_Name varchar(255),"
               "Condition_Value Int,"
               "FOREIGN KEY (Sequence) REFERENCES Sequences(Name),"
               "FOREIGN KEY (Condition_Name) REFERENCES Condition_Domains(Condition))")

cursor.execute("CREATE TABLE IF NOT EXISTS Experiment_Boolean"
               "(Experiment_ID Int NOT NULL AUTO_INCREMENT,"
               "Sequence varchar(255),"
               "Condition_Name varchar(255),"
               "Condition_Value Bool,"
               "FOREIGN KEY (Sequence) REFERENCES Sequences(Name),"
               "FOREIGN KEY (Condition_Name) REFERENCES Condition_Domains(Condition))")

cursor.execute("CREATE TABLE IF NOT EXISTS Experiment_String"
               "(Experiment_ID Int NOT NULL AUTO_INCREMENT,"
               "Sequence varchar(255),"
               "Condition_Name varchar(255),"
               "Condition_Value String,"
               "FOREIGN KEY (Sequence) REFERENCES Sequences(Name),"
               "FOREIGN KEY (Condition_Name) REFERENCES Condition_Domains(Condition))")

cursor.execute("CREATE TABLE IF NOT EXISTS Experiment_Float"
               "(Experiment_ID Int NOT NULL AUTO_INCREMENT,"
               "Sequence varchar(255),"
               "Condition_Name varchar(255),"
               "Condition_Value Double,"
               "FOREIGN KEY (Sequence) REFERENCES Sequences(Name),"
               "FOREIGN KEY (Condition_Name) REFERENCES Condition_Domains(Condition))")

cursor.execute("CREATE TABLE IF NOT EXISTS Measurements_Int"
               "(Experiment_ID Int NOT NULL AUTO_INCREMENT,"
               "Measurement_Name varchar(255),"
               "Measurement_Value Int"
               "FOREIGN KEY (Measurement_Name) REFERENCES Measurement_Domains(Measurement))")

cursor.execute("CREATE TABLE IF NOT EXISTS Measurements_Boolean"
               "(Experiment_ID Int NOT NULL AUTO_INCREMENT,"
               "Measurement_Name varchar(255),"
               "Measurement_Value Bool,"
               "FOREIGN KEY (Measurement_Name) REFERENCES Measurement_Domains(Measurement))")

cursor.execute("CREATE TABLE IF NOT EXISTS Measurements_String"
               "(Experiment_ID Int NOT NULL AUTO_INCREMENT,"
               "Measurement_Name varchar(255),"
               "Measurement_Value varchar(255),"
               "FOREIGN KEY (Measurement_Name) REFERENCES Measurement_Domains(Measurement))")

cursor.execute("CREATE TABLE IF NOT EXISTS Measurements_Float"
               "(Experiment_ID Int NOT NULL AUTO_INCREMENT,"
               "Measurement_Name varchar(255),"
               "Measurement_Value Double,"
               "FOREIGN KEY (Measurement_Name) REFERENCES Measurement_Domains(Measurement))")

df = pd.read_csv()

for column in df.columns.values:

    experiment = column.str.split('_', n=1)
    cursor.execute("SELECT Name "
                   "FROM Sequences "
                   "WHERE Name = " + experiment[0])

    if not cursor.next():
        # Output condition missing error here
        continue
    sequence = cursor.fetchall()
    conditions = experiment[1].split('_')
    condList = [conditions[index] + '_' + conditions[index+1] for index in range(len(conditions)-1)]

    for condition in condList:
        expr = condition.split('_')
        cursor.execute("SELECT Condition, Domain "
                                "FROM Condition_Domains "
                                "WHERE Condition = " + expr[0])
        if not cursor.next():
            continue
        condRS = cursor.fetchall()
        exp = False
        for row in df.index.values:
            cursor.execute("SELECT Measurement "
                            "FROM Measurement_Domains "
                            "WHERE Measurement = " + row.str)
            if not cursor.next():
                # Output measurement missing error
                continue
            cell = df.loc[row.str, column.str]
            measRS = cursor.fetchall()
            for c in condRS:
                if not exp:
                    cursor.execute("INSERT INTO Experiment_" + c[1] +
                                   " (Sequence, Condition_Name, Condition_Value) VALUES "
                                   "(" + experiment[0] + ", " + condRS[0] + ", " + cell + ')')
                    exp = True
                else:
                    cursor.execute("SELECT Experiment_ID"
                                          "FROM Experiment_" + c[1] +
                                          " WHERE Sequence = " + experiment[0]
                                            + " AND Condition_Name = " + condRS[0]
                                            + " AND Condition_Value = " + cell)
                    expIDs = cursor.fetchall()
                    expid = 0
                    for result in expIDs:
                        expid = result[0]
                    cursor.execute("INSERT INTO Experiment_" + c[1] +
                                   " VALUES (" + expid + ", " + experiment[0] + ", "
                                   + condRS[0] + ", " + cell + ')')
                for r in measRS:
                    cursor.execute("SELECT Experiment_ID"
                                   "FROM Experiment_" + c[1] +
                                   " WHERE Sequence = " + experiment[0]
                                   + " AND Condition_Name = " + condRS[0]
                                   + " AND Condition_Value = " + cell)
                    expIDs = cursor.fetchall()
                    expid = 0
                    for result in expIDs:
                        expid = result[0]

            else:
                cursor.execute("SELECT Experiment_ID "
                               "FROM ")


cursor.execute("INSERT IGNORE INTO Sequences VALUES() ON DUPLICATE KEY UPDATE Name = Name)")
