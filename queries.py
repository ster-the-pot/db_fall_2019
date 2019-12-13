# file for all database queries/activities

def getAllSequences(cursor):
    results = []
    cursor.execute("SELECT Name FROM Sequences")

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
    for condition in conditions:
        results[conditon[0]] = condition[1]
    return results
