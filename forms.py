from flask import Flask, render_template, request,redirect,url_for,session, logging
from wtforms import Form,StringField,TextAreaField,validators, SelectField, RadioField, ValidationError
import mysql.connector
import queries

# CUSTOM USER INPUT VALIDATORS
def validateName(form, field):
    if(len(field.data) == 0 ):
        raise ValidationError("Name Already Exists")


#USER INPUT FORMS
class AddConditionForm(Form):
        conditions = StringField('Condition Name', [validators.Length(min=1,max=50), validateName])
        domain = RadioField("Domain",choices=[('int',"Integer"),('Boolean',"Boolean"),('String',"String"),("Float","Float")])

class AddMeasurementForm(Form):
        measurement = StringField('Measurement Name', [validators.Length(min=1,max=50), validateName])
        domain = RadioField("Domain",choices=[('int',"Integer"),('Boolean',"Boolean"),('String',"String"),("Float","Float")])

class ModifySequenceForm(Form):
    sequence = SelectField("Sequence Name")
    description = StringField("Description",[validators.Length(min=1,max=50), validators.InputRequired()])
    filename = StringField("Sequence File", [validators.Length(min=1,max=50)])

class InsertMeasurementForm(Form):
    test = "test"


class SequenceSelectForm(Form):
        sequences = SelectField(label="Select Sequence")



