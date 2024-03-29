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
        cursor.execute("""INSERT INTO Sequences Values(%s, %s, %s)""",
                       (name, description, file_name))
    except (errors.Error, errors.Warning):
        cursor.execute("""UPDATE Sequences SET Sequence = %s, Description = %s, File_Name = %s 
                        WHERE Sequence = %s""",
                       (name, description, file_name, name))
    return True


def experimentAdd(sequence, conditions, measurements, cursor):
    experiment = ExperimentReturn()
    count = len(conditions)
    experiment.sequence = sequence
    for measurement in measurements:
        experiment.measurements[measurement["measure"]] = measurement["measureValue"]
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
                cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int WHERE Experiment_ID = %s
                                    AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_Float WHERE Experiment_ID = %s
                                    AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean WHERE Experiment_ID = %s
                                    AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_String WHERE Experiment_ID = %s
                                    AND Condition_Name = %s AND Condition_Value = %s)""",
                               (iD[0], condition, experiment.conditions[condition],
                                iD[0], condition, experiment.conditions[condition],
                                iD[0], condition, experiment.conditions[condition],
                                iD[0], condition, experiment.conditions[condition]))
                iDs = cursor.fetchall()
               
                for i in iDs:
                    checks.append(i[0])
                prevCheck = True
                
            else:
                for i in checks:
                    
                    cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int WHERE Experiment_ID = %s
                                    AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_Float WHERE Experiment_ID = %s
                                    AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean WHERE Experiment_ID = %s
                                    AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_String WHERE Experiment_ID = %s
                                    AND Condition_Name = %s AND Condition_Value = %s)""",
                                   (i, condition, experiment.conditions[condition],
                                    i, condition, experiment.conditions[condition],
                                    i, condition, experiment.conditions[condition],
                                    i, condition, experiment.conditions[condition]))

                    iDs = cursor.fetchall()
                    
                    if not iDs:
                        checks.remove(i)

    if checks:
        return False

    cursor.execute("""SELECT COUNT(*) FROM (
                    (SELECT DISTINCT Experiment_ID FROM Experiment_Int)
                    UNION 
                    (SELECT DISTINCT Experiment_ID FROM Experiment_Float)
                    UNION 
                    (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean)
                    UNION 
                    (SELECT DISTINCT Experiment_ID FROM Experiment_String)) as id_count """)

    iD = cursor.fetchone()[0] + 1

    prevInsert = False
    for condition in experiment.conditions:
        cursor.execute("""SELECT Domain FROM Condition_Domains WHERE Condition_Name = %s""", (condition,))
        d = cursor.fetchone()

        if d is False:
            return False
        if d[0] == "Boolean":
            if experiment.conditions[condition].lower() in ['t', '1']:
                experiment.conditions[condition] = 1
            elif experiment.conditions[condition].lower() in ['f', '0']:
                experiment.conditions[condition] = 0

        if not prevInsert:
            try:
                cursor.execute(
                    """INSERT INTO Experiment_""" + d[0] + """ VALUES (%s, %s, %s, %s, %s)""",
                    (iD, experiment.sequence, condition, experiment.conditions[condition], count))

                prevInsert = True
                experiment.iD = iD

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

    for measurement in experiment.measurements:
        cursor.execute("SELECT Domain FROM Measurement_Domains WHERE Measurement_Name = %s", (measurement,))
        domain = cursor.fetchone()
        if not domain:
            return False
        if domain[0] == "Boolean":
            if experiment.measurements[measurement].lower() in ['t', '1']:
                experiment.measurements[measurement] = 1
            elif experiment.measurements[measurement].lower() in ['f', '0']:
                experiment.measurements[measurement] = 0

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
                
                experiment.measurements[exp[1]] = exp[2]
                if (str(exp[1]),str(exp[2])) not in answer:
                    answer.append((str(exp[1]), str(exp[2])))
    
    return answer


def side_by_side(sequence1, conditions1, sequence2, conditions2, cursor):
    shared = []
    experiment1 = Experiment()
    experiment1.sequence = sequence1
    for condition in conditions1:
        experiment1.conditions[condition["condition"]] = condition["value"]
    measurements1 = {}
    

    count = len(conditions1)
    cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int Where Sequence = %s AND Condition_Count = %s) 
                    UNION 
                   (SELECT DISTINCT Experiment_ID FROM Experiment_Float Where Sequence = %s AND Condition_Count = %s) 
                   UNION 
                   (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean Where Sequence = %s AND Condition_Count = %s) 
                   UNION 
                   (SELECT DISTINCT Experiment_ID FROM Experiment_String Where Sequence = %s AND Condition_Count = %s)""",
                   (experiment1.sequence, count, experiment1.sequence, count,
                    experiment1.sequence, count, experiment1.sequence, count))

    ret = cursor.fetchall()
    checks = []
    prevCheck = False
    for iD in ret:
        for condition in experiment1.conditions:
            
            if not prevCheck:
                cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int WHERE Experiment_ID = %s
                                AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                (SELECT DISTINCT Experiment_ID FROM Experiment_Float WHERE Experiment_ID = %s
                                AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean WHERE Experiment_ID = %s
                                AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                (SELECT DISTINCT Experiment_ID FROM Experiment_String WHERE Experiment_ID = %s
                                AND Condition_Name = %s AND Condition_Value = %s)""",
                               (iD[0], condition, experiment1.conditions[condition],
                                iD[0], condition, experiment1.conditions[condition],
                                iD[0], condition, experiment1.conditions[condition],
                                iD[0], condition, experiment1.conditions[condition]))
                iDs = cursor.fetchall()
                
                for i in iDs:
                    checks.append(i[0])
                prevCheck = True
                
            else:
                for i in checks:
                    cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int WHERE Experiment_ID = %s
                                    AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_Float WHERE Experiment_ID = %s
                                    AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean WHERE Experiment_ID = %s
                                    AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_String WHERE Experiment_ID = %s
                                    AND Condition_Name = %s AND Condition_Value = %s)""",
                                   (i, condition, experiment1.conditions[condition],
                                    i, condition, experiment1.conditions[condition],
                                    i, condition, experiment1.conditions[condition],
                                    i, condition, experiment1.conditions[condition]))

                    iDs = cursor.fetchall()

                    if not iDs:
                        checks.remove(i)

    for c in checks:
        cursor.execute("""(SELECT Measurement_Name, Measurement_Value FROM Measurements_Int Where Experiment_ID = %s) UNION 
                       (SELECT Measurement_Name, Measurement_Value FROM Measurements_Float Where Experiment_ID = %s) UNION 
                       (SELECT Measurement_Name, Measurement_Value FROM Measurements_Boolean Where Experiment_ID = %s) UNION 
                       (SELECT Measurement_Name, Measurement_Value FROM Measurements_String Where Experiment_ID = %s)""",
                       (c, c, c, c))
        results1 = cursor.fetchall()

        for result in results1:
            measurements1[result[0]] = result[1]

    experiment2 = Experiment()
    experiment2.sequence = sequence2
    for condition in conditions2:
        experiment2.conditions[condition["condition"]] = condition["value"]
    measurements2 = {}

    count = len(conditions2)

    cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int Where Sequence = %s AND Condition_Count = %s) 
                    UNION 
                   (SELECT DISTINCT Experiment_ID FROM Experiment_Float Where Sequence = %s AND Condition_Count = %s) 
                   UNION 
                   (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean Where Sequence = %s AND Condition_Count = %s) 
                   UNION 
                   (SELECT DISTINCT Experiment_ID FROM Experiment_String Where Sequence = %s AND Condition_Count = %s)""",
                   (experiment2.sequence, count, experiment2.sequence, count,
                    experiment2.sequence, count, experiment2.sequence, count))

    ret = cursor.fetchall()

    checks = []
    prevCheck = False
    for iD in ret:
        for condition in experiment2.conditions:
            if not prevCheck:
                cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int WHERE Experiment_ID = %s
                                AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                (SELECT DISTINCT Experiment_ID FROM Experiment_Float WHERE Experiment_ID = %s
                                AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean WHERE Experiment_ID = %s
                                AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                (SELECT DISTINCT Experiment_ID FROM Experiment_String WHERE Experiment_ID = %s
                                AND Condition_Name = %s AND Condition_Value = %s)""",
                               (iD[0], condition, experiment2.conditions[condition],
                                iD[0], condition, experiment2.conditions[condition],
                                iD[0], condition, experiment2.conditions[condition],
                                iD[0], condition, experiment2.conditions[condition]))
                iDs = cursor.fetchall()

                for i in iDs:
                    checks.append(i[0])
                prevCheck = True
            else:
                for i in checks:
                    cursor.execute("""(SELECT DISTINCT Experiment_ID FROM Experiment_Int WHERE Experiment_ID = %s
                                    AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_Float WHERE Experiment_ID = %s
                                    AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_Boolean WHERE Experiment_ID = %s
                                    AND Condition_Name = %s AND Condition_Value = %s) UNION 
                                    (SELECT DISTINCT Experiment_ID FROM Experiment_String WHERE Experiment_ID = %s
                                    AND Condition_Name = %s AND Condition_Value = %s)""",
                                   (i, condition, experiment2.conditions[condition],
                                    i, condition, experiment2.conditions[condition],
                                    i, condition, experiment2.conditions[condition],
                                    i, condition, experiment2.conditions[condition]))

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
        entry.sequence = sequence
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
            entry.iD = iD[0]
            for condition in conditions:
                cursor.execute("""(SELECT * FROM Experiment_Int WHERE Experiment_ID = %s 
                               AND Condition_Name = %s AND Condition_Value = %s) UNION 
                               (SELECT * FROM Experiment_String WHERE Experiment_ID = %s 
                               AND Condition_Name = %s AND Condition_Value = %s) UNION 
                               (SELECT * FROM Experiment_Float WHERE Experiment_ID = %s 
                               AND Condition_Name = %s AND Condition_Value = %s) UNION 
                               (SELECT * FROM Experiment_Boolean WHERE Experiment_ID = %s 
                               AND Condition_Name = %s AND Condition_Value = %s)""",
                               (iD, condition["condition"], condition["value"],
                                iD, condition["condition"], condition["value"],
                                iD, condition["condition"], condition["value"],
                                iD, condition["condition"], condition["value"]))

                exps = cursor.fetchall()

                if exps is False:
                    continue

                for exp in exps:
                    entry.conditions[exp[2]] = exp[3]
                    for measurement in measurements:
                        cursor.execute("""(SELECT Measurement_Name, Measurement_Value FROM Measurements_Int 
                                       WHERE Experiment_ID = %s and Measurement_Name = %s) UNION 
                                       (SELECT Measurement_Name, Measurement_Value FROM Measurements_Float 
                                       WHERE Experiment_ID = %s and Measurement_Name = %s) UNION 
                                       (SELECT Measurement_Name, Measurement_Value FROM Measurements_Boolean 
                                       WHERE Experiment_ID = %s and Measurement_Name = %s) UNION 
                                       (SELECT Measurement_Name, Measurement_Value FROM Measurements_String 
                                       WHERE Experiment_ID = %s and Measurement_Name = %s)""",
                                       (iD, measurement["measure"],
                                        iD, measurement["measure"],
                                        iD, measurement["measure"],
                                        iD, measurement["measure"]))

                        measures = cursor.fetchall()
                        if measures is False:
                            continue
                        for measure in measures:
                            entry.measurements[measure[0]] = measure[1]
        if entry.conditions:
            answer.append(entry)
    return answer
