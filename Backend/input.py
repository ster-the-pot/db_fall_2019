from experiment import ExperimentReturn, Experiment
from mysql.connector import errors as errors


def conditionAdd(name, domain, cursor):
    n = name
    d = domain
    if d.lower() == "float":
        d = "Float"
    elif domain.lower() == "boolean":
        d = "Boolean"
    elif domain.lower() == "int":
        d = "Int"
    elif domain.lower() == "string":
        d = "String"
    else:
        return False
    try:
        cursor.execute("""INSERT INTO Condition_Domains Values(%s, %s)""", (n, d))
    except (errors.Error, errors.Warning) as error:
        return False
    return True


def measurementAdd(name, domain, cursor):
    n = name
    d = domain
    if d.lower() == "float":
        d = "Float"
    elif domain.lower() == "boolean":
        d = "Boolean"
    elif domain.lower() == "int":
        d = "Int"
    elif domain.lower() == "string":
        d = "String"
    else:
        return False
    try:
        cursor.execute("""INSERT INTO Measurement_Domains Values(%s, %s)""", (n, d))
    except (errors.Error, errors.Warning):
        return False
    return True


def sequenceAdd(name, description, cursor, file_name=None):
    try:
        cursor.execute("""INSERT INTO Sequences Values(%s, %s, %s) ON DUPLICATE KEY UPDATE Sequence = %s
                        AND Description = %s AND File_Name = %s""",
                       (name, description, file_name, name, description, file_name))
    except (errors.Error, errors.Warning):
        return False
    return True


def experimentAdd(sequence, conditions, measurement, value, cursor):
    experiment = Experiment()
    experiment.sequence = sequence
    experiment.measurements[measurement] = value
    print(conditions)
    for condition in conditions:
        experiment.conditions[condition["condition"]] = condition["value"]
            
    iD = 0
    for condition in experiment.conditions:
        cursor.execute("""SELECT Domain FROM Condition_Domains WHERE Condition_Name = %s""", (condition,))
        domain = cursor.fetchall()
        
        if domain is False:
            return False
        prevInsert = False
    
        initCond = 0
        initValue = 0
        for d in domain:
            if not prevInsert:
                try:
                    cursor.execute(
                        """INSERT INTO Experiment_%s (Sequence, Condition_Name, Condition_Value) VALUES (%s, %s, %s)""",
                        (d[0], experiment.sequence, condition, experiment.conditions[condition]))
                    prevInsert = True
                    initCond = condition
                    initValue = experiment.conditions[condition]
                except (errors.Error, errors.Warning) as error:
                    print(error)
                    return False

            else:
                cursor.execute("""SELECT Experiment_ID FROM Experiment_%s
                               WHERE Sequence = %s 
                               AND Condition_Name = %s
                               AND Condition_Value = %s""", (d[0], experiment.sequence, initCond, initValue))
                expIDs = cursor.fetchall()

                if expIDs is False:
                    continue

                for i in expIDs:
                    iD = i
                try:
                    cursor.execute("""INSERT INTO Experiment_%s VALUES (%s, %s, %s, %s)'""",
                                   (d[0], iD, experiment.sequence, condition, experiment.conditions[condition]))
                except (errors.Error, errors.Warning) as error:
                    print(error)
                    return False
    for measurement in experiment.measurements:
        cursor.execute("SELECT Domain FROM Measurement_Domains WHERE Measurement_Name = %s", (measurement,))
        domain = cursor.fetchall()
        if domain is False:
            continue
        for d in domain:
            try:
                cursor.execute("""INSERT INTO Measurements_"""+d[0] + """ Values (%s, %s, %s)""",
                               (iD, measurement, experiment.measurements[measurement]))
            except (errors.Error, errors.Warning) as error:
                print(error)
                return False
    return True


def experimentInfo(condition, value, cursor):
    answer = []
    cursor.execute("""SELECT Domain FROM Condition_Domains WHERE Condition_Name = %s""", (condition,))
    domain = cursor.fetchall()
    if domain is False:
        return
    cursor.execute("""SELECT Experiment_ID 
                   FROM Experiment_%s 
                   WHERE Condition_Name = %s 
                   AND Condition_Value = %s 
                   ORDER BY Experiment_ID DESC""", (domain[0], condition, value))

    expIDs = cursor.fetchall()

    if expIDs is False:
        return
    for iD in expIDs:
        ex = ExperimentReturn()
        ex.id = iD
        ex.conditions[str(condition)] = value

        cursor.execute("""SELECT Sequence FROM Experiment_%s 
                       WHERE Experiment_ID = %s""", (domain[0], iD))

        sequence = cursor.fetchone()

        ex.sequence = sequence[0]

        cursor.execute("""(SELECT DISTINCT * FROM Measurement_Int WHERE Experiment_ID = %s) UNION 
                       "(SELECT DISTINCT * FROM Measurement_Float WHERE Experiment_ID = %s) UNION 
                       "(SELECT DISTINCT * FROM Measurement_Boolean WHERE Experiment_ID = %s) UNION 
                       "(SELECT DISTINCT * FROM Measurement_Int WHERE Experiment_ID = %s) 
                       "ORDER BY Experiment_ID DESC""", (iD, iD, iD, iD))

        exps = cursor.fetchall()
        for exp in exps:
            ex.measurements[exp[1]] = exp[2]

        answer.append(ex)

    return answer


def containsSequence(sequence, cursor):
    exps = []

    cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int WHERE Sequence = %s) UNION 
                   "(SELECT DISTINCT Experiment_ID FROM Experiment_Float WHERE Sequence = %s) UNION 
                   "(SELECT DISTINCT Experiment_ID FROM Experiment_Boolean WHERE Sequence = %s) UNION 
                   "(SELECT DISTINCT Experiment_ID FROM Experiment_String WHERE Sequence = %s)""",
                   (sequence, sequence, sequence, sequence))

    iDs = cursor.fetchall()

    for iD in iDs:
        exp = ExperimentReturn()
        exp.iD = iD[0]
        exp.sequence = sequence
        cursor.execute("""(SELECT Condition_Name, Condition_Value FROM Experiment_Int WHERE Experiment_ID = %s) UNION 
                       "(SELECT Condition_Name, Condition_Value FROM Experiment_Float WHERE Experiment_ID = %s) UNION 
                       "(SELECT Condition_Name, Condition_Value FROM Experiment_Boolean WHERE Experiment_ID = %s) UNION 
                       "(SELECT Condition_Name, Condition_Value FROM Experiment_Int WHERE Experiment_ID = %s)""",
                       (iD, iD, iD, iD))

        results = cursor.fetchall()
        for result in results:
            exp.conditions[result[0]] = result[1]
        if exp not in exps:
            exps.append(exp)
    return exps


def side_by_side(exp1, exp2, cursor):
    shared = {}
    cursor.execute("""(SELECT Measurement_Name, Measurement_Value FROM Measurement_Int Where Experiment_ID = %s) UNION 
                   "(SELECT Measurement_Name, Measurement_Value FROM Measurement_Float Where Experiment_ID = %S) UNION 
                   "(SELECT Measurement_Name, Measurement_Value FROM Measurement_Boolean Where Experiment_ID = %s) UNION 
                   "(SELECT Measurement_Name, Measurement_Value FROM Measurement_String Where Experiment_ID = %s)""",
                   (exp1.iD, exp1.iD, exp1.iD, exp1.iD))

    results1 = cursor.fetchall()

    for result in results1:
        exp1.measurements[result[0]] = result[1]

    cursor.execute("""(SELECT Measurement_Name, Measurement_Value FROM Measurement_Int Where Experiment_ID = %s) UNION 
                   "(SELECT Measurement_Name, Measurement_Value FROM Measurement_Float Where Experiment_ID = %s") UNION 
                   "(SELECT Measurement_Name, Measurement_Value FROM Measurement_Boolean Where Experiment_ID = %s) UNION 
                   "(SELECT Measurement_Name, Measurement_Value FROM Measurement_String Where Experiment_ID = %s""",
                   (exp2.iD, exp2.iD, exp2.iD, exp2.iD))

    results2 = cursor.fetchall()

    for result in results2:
        exp2.measurements[result[0]] = result[1]

    for result in exp1.measurements:
        if result in exp2.measurements:
            if result not in shared:
                shared[result] = exp1.measurements[result]
    for result in exp2.measurements:
        if result in exp1.measurements:
            if result not in shared:
                shared[result] = exp2.measurements[result]

    return shared


def multipleExp(sequences, conditions, measurements, cursor):
    answer = []
    for sequence in sequences:
        entry = ExperimentReturn()
        cursor.execute("""(SELECT Experiment_ID FROM Experiment_Int WHERE Sequence = %s) UNION 
                       "(SELECT Experiment_ID FROM Experiment_Float WHERE Sequence = %s) UNION 
                       "(SELECT Experiment_ID FROM Experiment_Boolean WHERE Sequence = %s) UNION 
                       "(SELECT Experiment_ID FROM Experiment_String WHERE Sequence = %s)""",
                       (sequence, sequence, sequence, sequence))
        ids = cursor.fetchall()

        if ids is False:
            continue

        valid = []
        for iD in ids:
            for condition in conditions:
                cursor.execute("""(SELECT * FROM Experiment_Int WHERE Condition_Name = %s 
                               AND Experiment_ID = %s) UNION 
                               (SELECT * FROM Experiment_String WHERE Condition_Name = %s 
                               AND Experiment_ID = %s) UNION 
                               (SELECT * FROM Experiment_Float WHERE Condition_Name = %s 
                               AND Experiment_ID = %s) UNION 
                               (SELECT * FROM Experiment_Boolean WHERE Condition_Name = %s 
                               AND Experiment_ID = %s)""",
                               (condition, iD, condition, iD, condition, iD, condition, iD))

                exps = cursor.fetchall()

                if exps is False:
                    continue

                for exp in exps:
                    entry.iD = exp[0]
                    entry.sequence = exp[1]
                    entry.conditions[exp[2]] = exp[3]
                    for measurement in measurements:
                        cursor.execute("""(SELECT Measurement_Name, Measurement_Value FROM Measurement_Int 
                                       WHERE Measurement_Name = %s 
                                       AND Experiment_ID = %s) UNION 
                                       (SELECT Measurement_Name, Measurement_Value FROM Measurement_Float 
                                       WHERE Measurement_Name = %s 
                                       AND Experiment_ID = %s) UNION 
                                       (SELECT Measurement_Name, Measurement_Value FROM Measurement_Boolean 
                                       WHERE Measurement_Name = %s 
                                       AND Experiment_ID = %s) UNION 
                                       (SELECT Measurement_Name, Measurement_Value FROM Measurement_String 
                                       WHERE Measurement_Name = %s 
                                       AND Experiment_ID = %s)""",
                                       (measurement, iD, measurement, iD, measurement, iD, measurement, iD))

                        measures = cursor.fetchall()
                        if measures is False:
                            continue
                        for measure in measures:
                            entry.measurements[measure[0]] = measure[1]
        answer.append(entry)
    return answer
