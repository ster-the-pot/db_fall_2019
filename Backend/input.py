from experiment import ExperimentReturn
from experiment import Experiment


def conditionAdd(name, domain, cursor, mydb):
    cursor.execute("INSERT INTO Experiment_Domains "
                   "Values(" + name + ", " + domain + ')')
    mydb.commit()


def measurementAdd(name, domain, cursor, mydb):
    cursor.execute("INSERT INTO Measurement_Domains "
                   "Values(" + name + ", " + domain + ')')
    mydb.commit()


def sequenceAdd(name, description, cursor, mydb, file_name=None):
    cursor.execute("INSERT INTO Sequences "
                   "Values(" + name + ", " + description + ", " + file_name +
                   ") ON DUPLICATE KEY UPDATE Name = " + name)
    mydb.commit()


def experimentAdd(experiment, cursor):
    iD = 0
    for condition in experiment.conditions:
        cursor.execute("SELECT Domain FROM Condition_Domains WHERE Condition_Name = " + condition)
        domain = cursor.fetchall()
        if domain is None:
            continue
        prevInsert = False
        initCond = 0
        initValue = 0
        for d in domain:
            if not prevInsert:

                cursor.execute(
                    "INSERT INTO Experiment_" + str(d[0]) + " (Sequence, Condition_Name, Condition_Value) VALUES ("
                    + str(experiment.sequence) + ", " + str(condition) + ", " + str(experiment.conditions[condition]) + ')')
                prevInsert = True
                initCond = condition
                initValue = experiment.conditions[condition]
            else:
                cursor.execute("SELECT Experiment_ID FROM Experiment_" + str(d[0]) +
                               " WHERE sequence = " + str(experiment.sequence) +
                               " AND condition ")
                expIDs = cursor.fetchall()

                if expIDs is None:
                    continue

                for i in expIDs:
                    iD = i
                cursor.execute("INSERT INTO Experiment_" + str(d[0]) + " VALUES (" +
                               str(iD) + ", " + str(experiment.sequence) + ", " + str(condition) + ", "
                               + str(experiment.conditions[condition]) + ')')
    for measurement in experiment.measurements:
        cursor.execute("SELECT Domain FROM Measurement_Domains WHERE Measurement_Name =" + str(measurement))
        domain = cursor.fetchall
        if domain is None:
            continue
        for d in domain:
            cursor.execute("INSERT INTO Measurement_" + str(d[0]) + " Values (" +
                           str(iD) + ", " + str(measurement) + ", " + str(experiment.measurements[measurement]) + ')')


def experimentInfo(condition, value, cursor):
    answer = []
    cursor.execute("SELECT Domain "
                   "FROM Condition_Domains "
                   "WHERE Condition_Name = " + str(condition))
    domain = cursor.fetchone()
    if domain is None:
        return
    cursor.execute("SELECT Experiment_ID "
                   "FROM Experiment_" + str(domain[0]) +
                   " WHERE Condition_Name = " + str(condition) +
                   " AND Condition_Value = " + str(value))

    expIDs = cursor.fetchall()

    if expIDs is None:
        return
    for iD in expIDs:
        ex = ExperimentReturn()
        ex.id = iD
        ex.conditions[str(condition)] = value
        cursor.execute("SELECT * FROM Measurement_Int WHERE Experiment_ID = " + str(iD))

        exps = cursor.fetchall()
        for exp in exps:
            ex.measurements[exp[1]] = exp[2]

        cursor.execute("SELECT * FROM Measurement_Float WHERE Experiment_ID = " + str(iD))

        exps = cursor.fetchall()
        for exp in exps:
            ex.measurements[exp[1]] = exp[2]

        cursor.execute("SELECT * FROM Measurement_Boolean WHERE Experiment_ID = " + str(iD))

        exps = cursor.fetchall()
        for exp in exps:
            ex.measurements[exp[1]] = exp[2]

        cursor.execute("SELECT * FROM Measurement_String WHERE Experiment_ID = " + str(iD))

        exps = cursor.fetchall()
        for exp in exps:
            ex.measurements[exp[1]] = exp[2]

        answer.append(ex)

    return answer


def cotainsSequence(sequence, cursor):
    ids = []

    cursor.execute("(SELECT Experiment_ID FROM Experiment_Int WHERE Sequence = " + str(sequence) +
                   ") UNION "
                   "(SELECT Experiment_ID FROM Experiment_Float WHERE Sequence = " + str(sequence) +
                   ") UNION "
                   "(SELECT Experiment_ID FROM Experiment_Boolean WHERE Sequence = " + str(sequence) +
                   ") UNION "
                   "(SELECT Experiment_ID FROM Experiment_String WHERE Sequence = " + str(sequence) + ')')

    iDs = cursor.fetchall()

    for iD in iDs:
        ids.append(iD[0])
    return ids


def side_by_side(sequence1, conditions1, sequence2, conditions2, cursor):
    cursor.execute("(SELECT Experiment_ID FROM Experiment_Int WHERE Sequence = " + str(sequence1) +
                   ") UNION "
                   "(SELECT Experiment_ID FROM Experiment_Float WHERE Sequence = " + str(sequence1) +
                   ") UNION "
                   "(SELECT Experiment_ID FROM Experiment_Boolean WHERE Sequence = " + str(sequence1) +
                   ") UNION "
                   "(SELECT Experiment_ID FROM Experiment_String WHERE Sequence = " + str(sequence1) + ')')
    ids = cursor.fetchall()

    valid = []
    for iD in ids:
        for condition in conditions1:
            cursor.execute("(SELECT Experiment_ID FROM Experiment_Int WHERE Condition_Name = " + str(condition) +
                           " AND Experiment_ID = " + str(iD) + ") UNION "
                           "(SELECT Experiment_ID FROM Experiment_String WHERE Condition_Name = " + str(condition) +
                           " AND Experiment_ID = " + str(iD) + ") UNION "
                           "(SELECT Experiment_ID FROM Experiment_Float WHERE Condition_Name = " + str(condition) +
                           " AND Experiment_ID = " + str(iD) + ") UNION "
                           "(SELECT Experiment_ID FROM Experiment_Boolean WHERE Condition_Name = " + str(condition) +
                           " AND Experiment_ID = " + str(iD) + ')')
            val = cursor.fetchall()

            if val is None:
                continue
            for v in val:
                if v not in valid:
                    valid.append(v)

def multipleExp(sequences, conditions, measurements, cursor):
    answer = []
    experiments = []
    for sequence in sequences:
        entry = ExperimentReturn()
        cursor.execute("(SELECT Experiment_ID FROM Experiment_Int WHERE Sequence = " + str(sequence) +
                       ") UNION "
                       "(SELECT Experiment_ID FROM Experiment_Float WHERE Sequence = " + str(sequence) +
                       ") UNION "
                       "(SELECT Experiment_ID FROM Experiment_Boolean WHERE Sequence = " + str(sequence) +
                       ") UNION "
                       "(SELECT Experiment_ID FROM Experiment_String WHERE Sequence = " + str(sequence) + ')')
        ids = cursor.fetchall()
        valid = []
        for iD in ids:
            for condition in conditions:
                cursor.execute("(SELECT Experiment_ID FROM Experiment_Int WHERE Condition_Name = " + str(condition) +
                               " AND Experiment_ID = " + str(iD) + ") UNION "
                                "(SELECT Experiment_ID FROM Experiment_String WHERE Condition_Name = " + str(condition) +
                               " AND Experiment_ID = " + str(iD) + ") UNION "
                               "(SELECT Experiment_ID FROM Experiment_Float WHERE Condition_Name = " + str(condition) +
                               " AND Experiment_ID = " + str(iD) + ") UNION "
                               "(SELECT Experiment_ID FROM Experiment_Boolean WHERE Condition_Name = " + str(condition) +
                               " AND Experiment_ID = " + str(iD) + ')')

                exps = cursor.fetchall

                if exps is None:
                    continue

                for exp in exps:
                    entry.iD = exp[0]
                    entry.sequence = exp[1]
                    entry.conditon[exp[2]] = exp[3]
                    for measurement in measurements:
                        cursor.execute("SELECT Measurement_Name, Measurement_Value FROM Measurement_Int, "
                                       "Measurement_Boolean, Measurement_Float, Measurement_String "
                                       "WHERE ")
