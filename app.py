from flask import Flask, render_template,request,redirect,url_for,session, logging
from wtforms import Form,StringField,TextAreaField,validators, SelectField
import mysql.connector
import forms
import queries

app = Flask(__name__)
app.debug= True


@app.route("/")
def homePage():
        return render_template('index.html')

@app.route("/input", methods=["GET","POST"])
def inputPage():
        formCond = forms.AddConditionForm(request.form)
        formMeasure = forms.AddMeasurementForm(request.form)
        formSeq = forms.ModifySequenceForm(request.form)
        formSeq.sequence.choices=queries.getAllSequences()
        print(len(queries.getAllSequences()))

        if(request.method == 'POST'):
                print("Origin: " , request.form['btn'], "results: " , request.form, formSeq.sequence.data)
                if(request.form["btn"] == "condition" and formCond.validate()):
                        print("Do Condition Insert")
                elif(request.form["btn"] == "measure" and formMeasure.validate()):
                        print("Do measure Insert")
                elif(request.form["btn"] == "sequence" and formSeq.validate()):
                        print("Do sequence modify")
        
        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq)

@app.route("/about", methods =["GET","POST"])
def aboutPage():
        return render_template("about.html")

if __name__ == "__main__":
    app.run()
