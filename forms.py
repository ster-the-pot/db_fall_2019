from flask import Flask, render_template, request,redirect,url_for,session, logging
from wtforms import Form,StringField,TextAreaField,validators, SelectField,RadioField,ValidationError,FieldList,FormField, FileField
from werkzeug.utils import secure_filename
import os

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
    sequence = SelectField("Sequence Name", default="Select Sequence Name")
    description = StringField("Description",[validators.Length(min=1,max=50), validators.InputRequired()])
    filename = StringField("Sequence File", [validators.Length(min=1,max=50)])



# Experiment Input 

#used for rendering a condition input with value for said condition
class ConditionForm(Form):
    condition = SelectField("Measurement", default="Select Measurement", choices=[("Cond2","Cond2"),("Cond1","Cond1")])
    value= value  = StringField('', [validators.Length(min=1,max=50), validateName])

#overarching form for rendering experiment input
class InsertMeasurementForm(Form):
    sequence = SelectField(label="Select Sequence")
    measurement = sequence = SelectField("Measurement", default="Select Measurement", choices=[("Me1","Me1"),("Me2","Me2")])
    value  = StringField('Measurement Value', [validators.Length(min=1,max=50), validateName])

    condList = FieldList(FormField(ConditionForm))

    def addCondition(self):
        self.condList.append_entry()
        print(self.condList)

    def getConditions(self):
        conditionList = []
        while(len(self.condList) is not 0):
            conditionList.append(self.condList.pop_entry().data)
            #conditionList.append({"condition":rawCond.})
        return conditionList

            
        
#CSV FILE UPLOAD

def validateFile(file):
    print(file.filename)
    if(file.filename == ""):
        return False
    filename = secure_filename(file.filename)
    file.save()
    print(filename)
    return True

#validation functions
class CSVFileUpload(Form):
    file = FileField("")




#handles addition of Conditions in Experiment Modal
