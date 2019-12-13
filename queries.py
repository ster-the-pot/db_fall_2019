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
    results = {}
    cursor.execute("""(SELECT Condition_Name, Condition_Value FROM Experiment_Int) UNION 
                   (SELECT Condition_Name, Condition_Value FROM Experiment_Float) UNION 
                   (SELECT Condition_Name, Condition_Value FROM Experiment_Boolean) UNION 
                   (SELECT Condition_Name, Condition_Value FROM Experiment_Boolean)""")

    conditions = cursor.fetchall()
    return conditions

def getAllConditionNames(cursor):
    results = []
    cursor.exeucte("SELECT Condition_Name FROM Condition_Domains")

    conditions = cursor.fetchall()

    for condition in conditions:
        results.append((str(condition[0]), str(condition[0])))
    return results

def getAllMeasurementNames(cursor):
    results = []
    cursor.exeucte("SELECT Measurement_Name FROM Measurment_Domains")

    measurements = cursor.fetchall()

    for measurement in measurements:
        results.append((str(measurement[0]), str(measurement[0])))
    return results