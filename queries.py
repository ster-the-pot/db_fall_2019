# file for all database queries/activities
import mysql.connector as mysql

mydb = mysql.connect(
    host="18.224.202.17",
    user="pythonApp",
    passwd="bryceSterlingDB",
    database="biology"
)

cursor = mydb.cursor()

def getAllSequenceNames(cursor):
    results = []
    cursor.execute("SELECT Sequence FROM Sequences")

    sequences = cursor.fetchall()
    for sequence in sequences:
        results.append((str(sequence[0]), str(sequence[0])))
    return results


def getAllConditions(cursor):
    cursor.execute("""(SELECT Condition_Name, Condition_Value FROM Experiment_Int) UNION 
                   (SELECT Condition_Name, Condition_Value FROM Experiment_Float) UNION 
                   (SELECT Condition_Name, Condition_Value FROM Experiment_Boolean) UNION 
                   (SELECT Condition_Name, Condition_Value FROM Experiment_String)""")

    conditions = cursor.fetchall()
    return conditions


def getAllMeasurementNames(cursor):
    results = []
    cursor.execute("""SELECT Measurement_Name FROM Measurement_Domains""")
    measurements = cursor.fetchall()
    print("HERE")
    for measurement in measurements:
        print(str(measurement[0]), str(measurement[0]))
        results.append((str(measurement[0]), str(measurement[0])))
    return results


def getAllConditionNames(cursor):
    results = []
    cursor.execute("""SELECT Condition_Name FROM Condition_Domains""")
    measurements = cursor.fetchall()
    for measurement in measurements:
        print(str(measurement[0]), str(measurement[0]))
        results.append((str(measurement[0]), str(measurement[0])))
    return results
