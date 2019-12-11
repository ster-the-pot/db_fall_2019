# file for all database queries/activities

def getAllSequences(cursor):
    results = []
    cursor.execute("SELECT Name FROM Sequences")

    sequences = cursor.fetchall()
    for sequence in sequences:
        results.append((str(sequence[0]), str(sequence[0])))
    return results


def getAllConditions(cursor):
    results = []
    cursor.execute("SELECT Name FROM Sequences")

    conditions = cursor.fetchall()
    for condition in conditions:
        results.append((str(condition[0]), str(condition[0])))
    return results
