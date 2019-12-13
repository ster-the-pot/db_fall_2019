import mysql.connector as mysql
import pandas as pd
import numpy as np


def csvInput(csv, cursor):
    df = pd.read_csv(csv, index_col=0)

    for column in df.columns:
        df[column].replace('', np.nan, inplace=True)

    for column in df.columns:

        experiment = column.split('_', maxsplit=1)
        cursor.execute("""SELECT Sequence FROM Sequences WHERE Sequence=%s""", (experiment[0],))

        sequence = cursor.fetchall()

        if sequence is False:
            # Output sequence missing error here
            continue

        conditions = experiment[1].split('_')
        condList = [conditions[index] + '_' + conditions[index + 1] for index in range(len(conditions) - 1)]

        prevInsert = False
        iD = -1
        initCond = 0
        initValue = 0
        for condition in condList:
            expr = condition.split('_')
            cursor.execute("""
                            SELECT Condition_Name, Domain 
                           FROM Condition_Domains 
                           WHERE Condition_Name = %s""", (expr[0],))

            condRS = cursor.fetchall()

            for c in condRS:
                domain = c[1]
                value = expr[1]
                if domain.lower() == "float":
                    domain = "Float"
                    value = float(expr[1])
                elif domain.lower() == "boolean":
                    domain = "Boolean"
                    if value.lower() in ['t', '1']:
                        value = True
                    elif value.lower() in ['f', '0']:
                        value = False
                elif domain.lower() == "int":
                    domain = "Int"
                    value = int(expr[1])
                elif domain.lower() == "string":
                    domain = "String"
                    value = expr[1]
                else:
                    continue
                if not prevInsert:
                    cursor.execute("INSERT INTO Experiment_%s"
                                   " (Sequence, Condition_Name, Condition_Value) VALUES %s"
                                   "(%s, %s, %s", (domain, experiment[0], c[0], value))
                    initCond = c[0]
                    initValue = value
                    prevInsert = True
                else:
                    cursor.execute("""SELECT DISTINCT Experiment_ID"
                                   FROM Experiment_%s
                                   WHERE Sequence = %s
                                   AND Condition_Name = %s
                                   AND Condition_Value = %s""",
                                   (domain, experiment[0], initCond, initValue))
                    expIDs = cursor.fetchall()
                    for result in expIDs:
                        iD = result[0]
                    cursor.execute("""INSERT INTO Experiment_%s VALUES (%s, %s, %s)""",
                                   (domain, experiment[0], c[0], value))
        if iD == -1:
            continue
        for row in df.index.values:
            cursor.execute("""SELECT Measurement_Name, Domain 
                           FROM Measurement_Domains 
                           WHERE Measurement = %s""", (row.str,))
            measRS = cursor.fetchall()
            if measRS is False:
                # Output measurement missing error
                continue
            cell = df.loc[row.str, column.str]
            for r in measRS:
                rDomain = r[1]
                rValue = cell
                if rDomain.lower() == "float":
                    rDomain = "Float"
                    rValue = float(cell)
                elif rDomain.lower() == "boolean":
                    rDomain = "Boolean"
                    if rValue.lower() in ['t', '1']:
                        rValue = True
                    elif rValue.lower() in ['f', '0']:
                        rValue = False
                elif rDomain.lower() == "int":
                    rDomain = "Int"
                    rValue = int(cell)
                elif rDomain.lower() == "string":
                    domain = "String"
                    rValue = str(cell)
                else:
                    continue
                cursor.execute("""INSERT INTO Measurement_%s" + rDomain +
                               " VALUES (%s, %s, %s)""", (rDomain, iD, r[0], rValue))
