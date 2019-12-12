import mysql.connector as mysql
import pandas as pd
import numpy as np

mydb = mysql.connect(
    host="18.224.202.17",
    user="pythonApp",
    passwd="bryceSterlingDB"
)


def csvInput(csv, cursor):
    df = pd.read_csv(csv)

    for column in df.columns.values:
        df[column.str].replace('', np.nan, inplace=True)

        experiment = column.str.split('_', n=1)
        cursor.execute("SELECT Name "
                       "FROM Sequences "
                       "WHERE Name = " + str(experiment[0]))

        sequence = cursor.fetchall()

        if sequence is None:
            # Output condition missing error here
            continue

        conditions = experiment[1].split('_')
        condList = [conditions[index] + '_' + conditions[index + 1] for index in range(len(conditions) - 1)]

        prevInsert = False
        iD = 0
        initCond = 0
        initValue = 0
        for condition in condList:
            expr = condition.split('_')
            cursor.execute("SELECT Condition, Domain "
                           "FROM Condition_Domains "
                           "WHERE Condition_Name = " + str(expr[0]))

            condRS = cursor.fetchall()
            if condRS is None:
                continue

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
                    cursor.execute("INSERT INTO Experiment_" + domain +
                                   " (Sequence, Condition_Name, Condition_Value) VALUES "
                                   "(" + str(experiment[0]) + ", " + str(c[0]) + ", " + str(value) + ')')
                    initCond = c[0]
                    initValue = value
                    mydb.commit()
                    prevInsert = True
                else:
                    cursor.execute("SELECT Experiment_ID"
                                   "FROM Experiment_" + str(domain) +
                                   " WHERE Sequence = " + str(experiment[0])
                                   + " AND Condition_Name = " + str(initCond)
                                   + " AND Condition_Value = " + str(initValue))
                    expIDs = cursor.fetchall()
                    for result in expIDs:
                        iD = result[0]
                    cursor.execute("INSERT INTO Experiment_" + str(domain) +
                                   " VALUES (" + str(iD) + ", " + str(experiment[0]) + ", "
                                   + str(c[0]) + ", " + str(value) + ')')
                    mydb.commit()
        if iD is 0:
            continue
        for row in df.index.values:
            cursor.execute("SELECT Measurement_Name, Domain "
                           "FROM Measurement_Domains "
                           "WHERE Measurement = " + row.str)
            measRS = cursor.fetchall()
            if measRS is None:
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
                cursor.execute("INSERT INTO Measurement_" + rDomain +
                               " VALUES (" + str(iD) + ", " + str(r[0]) + ", "
                               + str(rValue) + ')')
                mydb.commit()
