from flask import Flask, render_template, request,redirect,url_for,session, logging
from wtforms import Form,StringField,TextAreaField,validators, SelectField, RadioField, ValidationError
import mysql.connector

def validateName(form, field):
    if(len(field.data) == 0 ):
        raise ValidationError("Name Already Exists")

class AddConditionForm(Form):
        conditions = StringField('Condition Name', [validators.Length(min=6,max=50), validateName])
        domain = RadioField("Domain",choices=[('int',"Integer"),('Boolean',"Boolean"),('String',"String"),("Float","Float")])

class AddMeasurementForm(Form):
        conditions = StringField('Measurement Name', [validators.Length(min=6,max=50), validateName])
        domain = RadioField("Domain",choices=[('int',"Integer"),('Boolean',"Boolean"),('String',"String"),("Float","Float")])

class ModifySequenceForm(Form):
    test = "test"

class InsertMeasurementForm(Form):
    test = "test"


class SequenceSelectForm(Form):
        sequences = SelectField(label="Select Sequence")