import mysql.connector as mysql
import pandas as pd
import numpy as np

mydb = mysql.connect(
    host="18.224.202.17",
    user="pythonApp",
    passwd="bryceSterlingDB"
)

cursor = mydb.cursor()

df = pd.read_csv()

for column in df.columns.values:
    df[column.str].replace('', np.nan, inplace=True)

    experiment = column.str.split('_', n=1)
    cursor.execute("SELECT Name "
                   "FROM Sequences "
                   "WHERE Name = " + experiment[0])

    sequence = cursor.fetchall()

    if sequence is None:
        # Output condition missing error here
        continue

    conditions = experiment[1].split('_')
    condList = [conditions[index] + '_' + conditions[index + 1] for index in range(len(conditions) - 1)]

    prevInsert = False
    initCond = 0
    initValue = 0
    for condition in condList:
        expr = condition.split('_')
        cursor.execute("SELECT Condition, Domain "
                       "FROM Condition_Domains "
                       "WHERE Condition_Name = " + expr[0])

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
                if expr[1].lower() in ['t', '1']:
                    value = True
                elif expr[1].lower() in ['f', '0']:
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
                               "(" + experiment[0] + ", " + c[0] + ", " + value + ')')
                initCond = c[0]
                initValue = value
                mydb.commit()
                prevInsert = True
            else:
                cursor.execute("SELECT Experiment_ID"
                               "FROM Experiment_" + domain +
                               " WHERE Sequence = " + experiment[0]
                               + " AND Condition_Name = " + initCond
                               + " AND Condition_Value = " + initValue)
                expIDs = cursor.fetchall()
                iD = 0
                for result in expIDs:
                    iD = result[0]
                cursor.execute("INSERT INTO Experiment_" + domain +
                               " VALUES (" + iD + ", " + experiment[0] + ", "
                               + c[0] + ", " + value + ')')
                mydb.commit()
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
                        if expr[1].lower() in ['t', '1']:
                            rValue = True
                        elif expr[1].lower() in ['f', '0']:
                            rValue = False
                    elif rDomain.lower() == "int":
                        rDomain = "Int"
                        rValue = int(cell)
                    elif rDomain.lower() == "string":
                        domain = "String"
                        rValue = str(cell)
                    else:
                        continue
                    cursor.execute("SELECT Experiment_ID"
                                   "FROM Experiment_" + domain +
                                   " WHERE Sequence = " + experiment[0]
                                   + " AND Condition_Name = " + c[0]
                                   + " AND Condition_Value = " + value)
                    expIDs = cursor.fetchall()
                    iD = 0
                    if expIDs is None:
                        continue
                    for result in expIDs:
                        iD = result[0]
                    cursor.execute("INSERT INTO Measurement_" + rDomain +
                                   " VALUES (" + iD + ", " + r[0] + ", "
                                   + rValue + ')')
                    mydb.commit()
