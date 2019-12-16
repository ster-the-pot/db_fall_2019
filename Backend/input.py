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


def experimentAdd(sequence, conditions, measurements, value, cursor):
    experiment = ExperimentReturn()
    count = len(conditions)
    experiment.sequence = sequence
    for measurement in measurements:
        experiment.measurements[measurement["measurement"]] = measurement["value"]
    for condition in conditions:
        experiment.conditions[condition["condition"]] = condition["value"]

    cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int Where Sequence = %s AND Condition_Count = %s) 
                    UNION 
                   (SELECT DISTINCT Experiment_ID FROM Experiment_Float Where Sequence = %s AND Condition_Count = %s) 
                   UNION 
                   (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean Where Sequence = %s AND Condition_Count = %s) 
                   UNION 
                   (SELECT DISTINCT Experiment_ID FROM Experiment_String Where Sequence = %s AND Condition_Count = %s)""",
                   (sequence, count, sequence, count, sequence, count, sequence, count))

    ret = cursor.fetchall()
    checks = []
    prevCheck = False

    for iD in ret:
        for condition in experiment.conditions:
            if not prevCheck:
                cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int Where Condition_Name = %s AND
                                    Experiment_ID = %s AND Condition_Value = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_Float Where Condition_Name = %s
                                    AND Experiment_ID = %s AND Condition_Value = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean Where Condition_Name = %s
                                    AND Experiment_ID = %s and Condition_Value = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_String Where Sequence = %s
                                    AND Experiment_ID = %s and Condition_Value = %s)""",
                               (condition, iD[0], experiment.conditions[condition],
                                condition, iD[0], experiment.conditions[condition],
                                condition, iD[0], experiment.conditions[condition],
                                condition, iD[0], experiment.conditions[condition]))
                iDs = cursor.fetchall()

                for i in iDs:
                    checks.append(i[0])
                prevCheck = True
                print(checks, "after prevCheck")
            else:
                for i in checks:
                    print(checks)
                    cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int Where Condition_Name = %s AND
                                        Experiment_ID = %s AND Condition_Value = %s) UNION 
                                        (SELECT DISTINCT Experiment_ID FROM Experiment_Float Where Condition_Name = %s
                                        AND Experiment_ID = %s AND Condition_Value = %s) UNION 
                                        (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean Where Condition_Name = %s
                                        AND Experiment_ID = %s AND Condition_Value = %s) UNION 
                                        (SELECT DISTINCT Experiment_ID FROM Experiment_String Where Sequence = %s
                                        AND Experiment_ID = %s AND Condition_Value = %s)""",
                                   (condition, i, experiment.conditions[condition],
                                    condition, i, experiment.conditions[condition],
                                    condition, i, experiment.conditions[condition],
                                    condition, i, experiment.conditions[condition]))

                    iDs = cursor.fetchall()

                    if not iDs:
                        checks.remove(i)

    if checks:
        return False

    cursor.execute("""SELECT COUNT (DISTINCT Experiment_ID) FROM (
                    (SELECT DISTINCT Experiment_ID FROM Experiment_Int)
                    UNION 
                    (SELECT DISTINCT Experiment_ID FROM Experiment_Float)
                    UNION 
                    (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean)
                    UNION 
                    (SELECT DISTINCT Experiment_ID FROM Experiment_String))""")

    iD = cursor.fetchone() + 1

    prevInsert = False
    for condition in experiment.conditions:
        cursor.execute("""SELECT Domain FROM Condition_Domains WHERE Condition_Name = %s""", (condition,))
        d = cursor.fetchone()

        if d is False:
            return False

        initCond = 0
        initValue = 0

        if not prevInsert:
            try:
                cursor.execute(
                    """INSERT INTO Experiment_""" + d[0] + """ VALUES (%s, %s, %s, %s, %s)""",
                    (iD, experiment.sequence, condition, experiment.conditions[condition], count))

                prevInsert = True
                experiment.iD = iD
                initCond = condition
                initValue = experiment.conditions[condition]

            except (errors.Error, errors.Warning) as error:
                print(error)
                return False

        else:
            try:
                cursor.execute("""INSERT INTO Experiment_""" + d[0] + """ VALUES (%s, %s, %s, %s, %s)""",
                               (experiment.iD, experiment.sequence, condition, experiment.conditions[condition], count))
            except (errors.Error, errors.Warning) as error:
                print(error)
                return False
    print(experiment.measurements, "MEASUREMENTS")

    for measurement in experiment.measurements:
        cursor.execute("SELECT Domain FROM Measurement_Domains WHERE Measurement_Name = %s", (measurement,))
        domain = cursor.fetchone()
        if not domain:
            return False
        print(domain)

        try:
            cursor.execute("""INSERT INTO Measurements_""" + domain[0] + """ Values (%s, %s, %s)""",
                           (experiment.iD, measurement, experiment.measurements[measurement]))
        except (errors.Error, errors.Warning) as error:
            print(error)
            return False
    return True


def experimentInfo(sequence, conditions, cursor):
    answer = []
    experiment = Experiment()
    experiment.sequence = sequence
    count = len(conditions)
    for condition in conditions:
        experiment.conditions[condition["condition"]] = condition["value"]
    for condition in experiment.conditions:
        cursor.execute("""SELECT Domain FROM Condition_Domains WHERE Condition_Name = %s""", (condition,))
        domain = cursor.fetchone()
        if domain is False:
            return
        cursor.execute("""SELECT DISTINCT Experiment_ID 
                   FROM Experiment_""" + domain[0] + """ 
                   WHERE Condition_Name = %s 
                   AND Condition_Value = %s 
                   AND Sequence = %s
                   ORDER BY Experiment_ID DESC""", (condition, experiment.conditions[condition], sequence))

        expIDs = cursor.fetchall()

        if not expIDs:
            return
        for iD in expIDs:
            print(iD[0])
            experiment.sequence = sequence
            experiment.iD = iD[0]

            # cursor.execute("""SELECT Sequence FROM Experiment_%s
            #              WHERE Experiment_ID = %s""", (domain[0], iD))

            # sequence = cursor.fetchone()

            # ex.sequence = sequence[0]

            cursor.execute("""(SELECT DISTINCT * FROM Measurements_Int WHERE Experiment_ID = %s) UNION 
                       (SELECT DISTINCT * FROM Measurements_Float WHERE Experiment_ID = %s) UNION 
                       (SELECT DISTINCT * FROM Measurements_Boolean WHERE Experiment_ID = %s) UNION 
                       (SELECT DISTINCT * FROM Measurements_String WHERE Experiment_ID = %s) 
                       ORDER BY Experiment_ID DESC""", (iD[0], iD[0], iD[0], iD[0]))

            exps = cursor.fetchall()
            for exp in exps:
                print(exp)
                experiment.measurements[exp[1]] = exp[2]
                answer.append((str(exp[1]), str(exp[2])))
    print(answer)
    return answer


def side_by_side(sequence1, conditions1, sequence2, conditions2, cursor):
    shared = []
    measurements1 = {}
    measurements2 = {}
    count = len(conditions1)
    cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int Where Sequence = %s AND Condition_Count = %s) 
                    UNION 
                   (SELECT DISTINCT Experiment_ID FROM Experiment_Float Where Sequence = %s AND Condition_Count = %s) 
                   UNION 
                   (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean Where Sequence = %s AND Condition_Count = %s) 
                   UNION 
                   (SELECT DISTINCT Experiment_ID FROM Experiment_String Where Sequence = %s AND Condition_Count = %s)""",
                   (sequence1, count, sequence1, count, sequence1, count, sequence1, count))

    ret = cursor.fetchall()
    checks = []
    prevCheck = False

    for iD in ret:
        for condition in conditions1:
            if not prevCheck:
                cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int Where Condition_Name = %s AND
                                Experiment_ID = %s) UNION 
                                (SELECT DISTINCT Experiment_ID FROM Experiment_Float Where Condition_Name = %s
                                AND Experiment_ID = %s) UNION 
                                (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean Where Condition_Name = %s
                                AND Experiment_ID = %s) UNION 
                                (SELECT DISTINCT Experiment_ID FROM Experiment_String Where Sequence = %s
                                AND Experiment_ID = %s)""",
                               (condition["condition"], iD[0], condition["condition"], iD[0],
                                condition["condition"], iD[0], condition["condition"], iD[0]))
                iDs = cursor.fetchall()

                for i in iDs:
                    checks.append(i[0])
                prevCheck = True
                print(checks, "after prevCheck")
            else:
                for i in checks:
                    print(checks)
                    cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int Where Condition_Name = %s AND
                                    Experiment_ID = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_Float Where Condition_Name = %s
                                    AND Experiment_ID = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean Where Condition_Name = %s
                                    AND Experiment_ID = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_String Where Sequence = %s
                                    AND Experiment_ID = %s)""",
                                   (condition["condition"], i, condition["condition"], i,
                                    condition["condition"], i, condition["condition"], i))

                    iDs = cursor.fetchall()

                    if not iDs:
                        checks.remove(i)

    for c in checks:
        print(c, " c is")
        cursor.execute("""(SELECT Measurement_Name, Measurement_Value FROM Measurements_Int Where Experiment_ID = %s) UNION 
                       (SELECT Measurement_Name, Measurement_Value FROM Measurements_Float Where Experiment_ID = %s) UNION 
                       (SELECT Measurement_Name, Measurement_Value FROM Measurements_Boolean Where Experiment_ID = %s) UNION 
                       (SELECT Measurement_Name, Measurement_Value FROM Measurements_String Where Experiment_ID = %s)""",
                       (c, c, c, c))
        results1 = cursor.fetchall()

        for result in results1:
            measurements1[result[0]] = result[1]

    count = len(conditions2)

    cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int Where Sequence = %s AND Condition_Count = %s) 
                    UNION 
                   (SELECT DISTINCT Experiment_ID FROM Experiment_Float Where Sequence = %s AND Condition_Count = %s) 
                   UNION 
                   (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean Where Sequence = %s AND Condition_Count = %s) 
                   UNION 
                   (SELECT DISTINCT Experiment_ID FROM Experiment_String Where Sequence = %s AND Condition_Count = %s)""",
                   (sequence2, count, sequence2, count, sequence2, count, sequence2, count))

    ret = cursor.fetchall()

    checks = []
    prevCheck = False
    for iD in ret:
        for condition in conditions2:
            if not prevCheck:
                cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int Where Condition_Name = %s AND
                                Experiment_ID = %s) UNION 
                                (SELECT DISTINCT Experiment_ID FROM Experiment_Float Where Condition_Name = %s
                                AND Experiment_ID = %s) UNION 
                                (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean Where Condition_Name = %s
                                AND Experiment_ID = %s) UNION 
                                (SELECT DISTINCT Experiment_ID FROM Experiment_String Where Sequence = %s
                                AND Experiment_ID = %s)""",
                               (condition["condition"], iD[0], condition["condition"], iD[0],
                                condition["condition"], iD[0], condition["condition"], iD[0]))
                iDs = cursor.fetchall()

                for i in iDs:
                    checks.append(i[0])
                prevCheck = True
            else:
                temp = []
                for i in checks:
                    cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int Where Condition_Name = %s AND
                                    Experiment_ID = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_Float Where Condition_Name = %s
                                    AND Experiment_ID = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean Where Condition_Name = %s
                                    AND Experiment_ID = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_String Where Sequence = %s
                                    AND Experiment_ID = %s)""",
                                   (condition["condition"], i, condition["condition"], i,
                                    condition["condition"], i, condition["condition"], i))

                    iDs = cursor.fetchall()

                    if not iDs:
                        checks.remove(i)

    for c in checks:
        cursor.execute("""(SELECT Measurement_Name, Measurement_Value FROM Measurements_Int Where Experiment_ID = %s) UNION 
                       (SELECT Measurement_Name, Measurement_Value FROM Measurements_Float Where Experiment_ID = %s) UNION 
                       (SELECT Measurement_Name, Measurement_Value FROM Measurements_Boolean Where Experiment_ID = %s) UNION 
                       (SELECT Measurement_Name, Measurement_Value FROM Measurements_String Where Experiment_ID = %s)""",
                       (c, c, c, c))
        results2 = cursor.fetchall()

        for result in results2:
            measurements2[result[0]] = result[1]

    for result in measurements1:
        if result in measurements2:
            if result not in shared:
                shared.append((result, measurements1[result], measurements2[result]))

    return shared


def multipleExp(sequences, conditions, measurements, cursor):
    answer = []
    for sequence in sequences:
        entry = ExperimentReturn()
        cursor.execute("""(SELECT Experiment_ID FROM Experiment_Int WHERE Sequence = %s) UNION 
                       (SELECT Experiment_ID FROM Experiment_Float WHERE Sequence = %s) UNION 
                       (SELECT Experiment_ID FROM Experiment_Boolean WHERE Sequence = %s) UNION 
                       (SELECT Experiment_ID FROM Experiment_String WHERE Sequence = %s)""",
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
                        cursor.execute("""(SELECT Measurement_Name, Measurement_Value FROM Measurements_Int 
                                       WHERE Measurement_Name = %s 
                                       AND Experiment_ID = %s) UNION 
                                       (SELECT Measurement_Name, Measurement_Value FROM Measurements_Float 
                                       WHERE Measurement_Name = %s 
                                       AND Experiment_ID = %s) UNION 
                                       (SELECT Measurement_Name, Measurement_Value FROM Measurements_Boolean 
                                       WHERE Measurement_Name = %s 
                                       AND Experiment_ID = %s) UNION 
                                       (SELECT Measurement_Name, Measurement_Value FROM Measurements_String 
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
