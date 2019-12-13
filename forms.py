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
    description = StringField("Description",[validators.Length(min=1,max=50), validators.InputRequired()])
    filename = StringField("Sequence File")



# Experiment Input 

#used for rendering a condition input with value for said condition
class ConditionForm(Form):
    condition = SelectField("Measurement", default="Select Measurement", choices=queries.getAllConditionNames(queries.cursor))
    value= value  = StringField('', [validators.Length(min=1,max=50), validateName])

class ConditionFormNoVal(Form):
    condition = SelectField("Measurement", default="Select Measurement", choices=queries.getAllConditionNames(queries.cursor))

#overarching form for rendering experiment input
class InsertMeasurementForm(Form):
    sequence = SelectField(label="Select Sequence",choices=queries.getAllSequenceNames(queries.cursor))
    measurement = SelectField("Measurement", default="Select Measurement", choices=queries.getAllMeasurementNames(queries.cursor))
    value  = StringField('Measurement Value', [validators.Length(min=1,max=50), validateName])

    condList = FieldList(FormField(ConditionForm))

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


class DualQueryMeasurementForm(Form):
    # retrieval of all sequence values
    choices = queries.getAllSequenceNames(queries.cursor)

    seq1 = SelectField(label="Select Sequence1",choices=choices)
    seq2 = SelectField(label="Select Sequence2",choices=choices)
    cond1 = FieldList(FormField(ConditionFormNoVal))
    cond2 = FieldList(FormField(ConditionFormNoVal))

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


