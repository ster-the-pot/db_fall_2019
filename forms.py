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
    seq = SelectField(label="Select Sequence",choices=[("Seq1","Seq1"),("Seq2","Seq2")])
    
    cond = FieldList(FormField(ConditionForm))

    def addCondition(self):
        self.cond.append_entry()

    def getConditions(self):
        conditionList = []
        while(len(self.cond) is not 0):
            conditionList.append(self.cond.pop_entry().data)
            #conditionList.append({"condition":rawCond.})
        return conditionList

    def getSequence(self):
        return self.seq.data


