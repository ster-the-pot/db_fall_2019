# file for all database queries/activities
import mysql.connector as mysql

mydb = mysql.connect(
    host="18.224.202.17",
    user="pythonApp",
    passwd="bryceSterlingDB",
    database="biology"
)

cursor = mydb.cursor()

def getAllSequences(cursor):
    results = []
    cursor.execute("SELECT Name FROM Sequences")

    sequences = cursor.fetchall()
    for sequence in sequences:
        results.append((str(sequence[0]), str(sequence[0])))
    return results


def getAllConditions(sequence, cursor):
    results = []
    cursor.execute("(SELECT Condition_Name, Condition_Value FROM Experiment_Int WHERE Sequence = " + str(sequence) +
                   ") UNION "
                   "(SELECT Condition_Name, Condition_Value FROM Experiment_Float WHERE Sequence = " + str(sequence) +
                   ") UNION "
                   "(SELECT Condition_Name, Condition_Value FROM Experiment_Boolean WHERE Sequence = " + str(sequence) +
                   ") UNION "
                   "(SELECT Condition_Name, Condition_Value FROM Experiment_Boolean WHERE Sequence = " + str(sequence)
                   + ')')

    conditions = cursor.fetchall()
    for condition in conditions:
        results[condition[0]] = condition[1]
    return results
