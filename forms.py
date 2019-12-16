from flask import Flask, render_template, request,redirect,url_for,session, logging
from wtforms import Form,StringField,TextAreaField,validators, SelectField,RadioField,ValidationError,FieldList,FormField, FileField
from werkzeug.utils import secure_filename
import os
from Backend.csvparse import csvInput

import mysql.connector
import queries

# CUSTOM USER INPUT VALIDATORS
def validateName(form, field):
    if(field.data == "taken" ):
        raise ValidationError("Name Already Exists")


#USER INPUT FORMS
class AddConditionForm(Form):
        conditions = StringField('Condition Name', [validators.Length(min=1,max=50), validateName, validators.InputRequired()])
        domain = RadioField("Domain",choices=[('String',"String"),('Boolean',"Boolean"),('int',"Integer"),("Float","Float")], default="String")

class AddMeasurementForm(Form):
        measurement = StringField('Measurement Name', [validators.Length(min=1,max=50), validateName])
        domain = RadioField("Domain",choices=[('String',"String"),('Boolean',"Boolean"),('int',"Integer"),("Float","Float")],default="String")

class ModifySequenceForm(Form):
    sequence = StringField("Sequence Name",[validators.Length(min=1,max=50), validators.InputRequired()])
    description = StringField("Description")
    filename = StringField("Sequence File")



# Experiment Input 

#used for rendering a condition input with value for said condition
class ConditionForm(Form):
    condition = SelectField("Measurement", default="Select Measurement", choices=queries.getAllConditionNames(queries.cursor))
    value = value = StringField('', [validators.Length(min=1,max=50), validateName])

    def updateConditionChoices(self, choiceTuples):
        self.condition.choices = choiceTuples

class MeasurementForm(Form):
    measure = SelectField("Measurement", default="Select Measurement", choices=queries.getAllMeasurementNames(queries.cursor))
    measureValue = StringField('', [validators.Length(min=1,max=50), validateName])

    def updateMeasureChoices(self, choiceTuples):
        self.measure.choices = choiceTuples


class ConditionFormNoVal(Form):
    condition = SelectField("Measurement", default="Select Measurement", choices=queries.getAllConditionNames(queries.cursor))

#overarching form for rendering experiment input
class InsertMeasurementForm(Form):
    sequence = SelectField(label="Select Sequence",choices=queries.getAllSequenceNames(queries.cursor))
    condList = FieldList(FormField(ConditionForm),min_entries=1)
    measureList = FieldList(FormField(MeasurementForm),min_entries=1)

    def updateSequenceList(self):
        self.sequence.choices = queries.getAllSequenceNames(queries.cursor)

    def addMeasure(self):
        self.measureList.append_entry()

    # allow for multivariable measurements
    def getMeasureList(self):
        measureList = []
        while(len(self.measureList) is not 0):
            measureList.append(self.measureList.pop_entry().data)
            #conditionList.append({"condition":rawCond.})
        return measureList
    #allow for multi-var conditions

    def updateMeasurementList(self):
        measureTuples = queries.getAllMeasurementNames(queries.cursor)
        for measurement in self.measureList:
            measurement.updateMeasureChoices(measureTuples)

    def updateConditionsList(self):
        condTuples = queries.getAllConditionNames(queries.cursor)
        for condition in self.condList:
            condition.updateConditionChoices(condTuples)

    def addCondition(self):
        self.condList.append_entry()

    def getConditions(self):
        conditionList = []
        while(len(self.condList) is not 0):
            conditionList.append(self.condList.pop_entry().data)
            #conditionList.append({"condition":rawCond.})
        return conditionList

            
        
#CSV FILE UPLOAD

def validateFile(file):
    if(file.filename == ""):
        return False
    filename = file.filename

    if(filename.rsplit('.',1)[1].lower() == "csv"):
        filename = secure_filename(filename)
        print(filename)
        # call file save function
        return file
    else:
        return False
    
    

#validation functions
class CSVFileUpload(Form):
    file = FileField("")






class QueryMeasurementForm(Form):
    sequence = SelectField(label="Select Sequence",choices=queries.getAllSequenceNames(queries.cursor))
    condList = FieldList(FormField(ConditionForm))

    def addCondition(self):
        self.condList.append_entry()

    def getConditions(self):
        conditionList = []
        while(len(self.condList) is not 0):
            conditionList.append(self.condList.pop_entry().data)
            #conditionList.append({"condition":rawCond.})
        return conditionList


    def updateConditionsList(self):
        condTuples = queries.getAllConditionNames(queries.cursor)
        for condition in self.condList:
            condition.updateConditionChoices(condTuples)

    def updateSequenceList(self):
        self.sequence.choices = queries.getAllSequenceNames(queries.cursor)


    


class DualQueryMeasurementForm(Form):
    # retrieval of all sequence values
    choices = queries.getAllSequenceNames(queries.cursor)

    seq1 = SelectField(label="Select Sequence1",choices=choices)
    seq2 = SelectField(label="Select Sequence2",choices=choices)
    cond1 = FieldList(FormField(ConditionForm))
    cond2 = FieldList(FormField(ConditionForm))

    def addCondition(self, index):
        if(index == 1):
            self.cond1.append_entry()
        else:
            self.cond2.append_entry()
        
    

    def getConditions(self,index):
        conditionList = []
        if(index == 1):
            while(len(self.cond1) is not 0):
                conditionList.append(self.cond1.pop_entry().data)
            return conditionList
        else:
            while(len(self.cond2) is not 0):
                conditionList.append(self.cond2.pop_entry().data)
            return conditionList


    def getSequence(self, index):
        if(index ==1):
            return self.seq1.data
        else:
            return self.seq2.data
        

    def updateConditionsList(self):
        condTuples = queries.getAllConditionNames(queries.cursor)
        for condition in self.cond1:
            condition.updateConditionChoices(condTuples)
        for condition in self.cond2:            
            condition.updateConditionChoices(condTuples)

    def updateSequenceList(self):
        self.seq1.choices = queries.getAllSequenceNames(queries.cursor)
        self.seq2.choices = queries.getAllSequenceNames(queries.cursor)
            


