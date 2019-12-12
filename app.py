from flask import Flask, render_template,request,redirect,url_for,session, logging, flash
from wtforms import Form,StringField,TextAreaField,validators, SelectField
import mysql.connector
import forms
import queries

app = Flask(__name__)
app.debug= True
app.secret_key="bryceSterlingCool"


@app.route("/")
def homePage():
        return render_template('index.html')

@app.route("/query/experiment", methods=["GET","POST"])
def experimentPage():
        formMVal = forms.QueryMeasurementForm(request.form)
        
        if(request.method=="POST"):
                if(request.form["btn"] == "mVal" and formMVal.validate()):
                        print("Do Experiment Lookup")
                        #results of query
                        conditionList = formMVal.getConditions()
                        sequence = formMVal.sequence.data
                        #################################
                        measurements = [("Measurement1","MeasurementValue1"),("Measurement2","MeasurementValue2"),("Measurement3","MeasurementValue3")]
                        return render_template('experiment.html',formMVal=formMVal, measurements=measurements) 
                elif(request.form["btn"] == "addCond"):
                        print("add conditions")
                        formMVal.addCondition()
                        
                        return render_template('experiment.html',formMVal=formMVal, showMeasure="true")                
        return render_template('experiment.html',formMVal=formMVal)

@app.route("/query/side", methods=["GET","POST"])
def sideBySidePage():
        formMVal = forms.QueryMeasurementForm(request.form)
        formMVal1 = forms.QueryMeasurementForm(request.form)
        
        if(request.method=="POST"):
                if(request.form["btn"] == "mVal" and formMVal.validate()):
                        print("Do Experiment Lookup")
                        #results of query
                        conditionList = formMVal.getConditions()
                        sequence = formMVal.sequence.data
                        #################################
                        measurements = [("Measurement1","MeasurementValue1"),("Measurement2","MeasurementValue2"),("Measurement3","MeasurementValue3")]
                        return render_template('side.html',formMVal=formMVal, formMVal1=formMVal1, measurements=measurements) 
                elif(request.form["btn"] == "addCond"):
                        print("add conditions")
                        formMVal.addCondition()
                        
                        return render_template('side.html',formMVal=formMVal, formMVal1=formMVal1, showMeasure="true")
         

        return render_template('side.html',formMVal=formMVal, formMVal1=formMVal1)



@app.route("/input", methods=["GET","POST"])
def inputPage():
        formCond = forms.AddConditionForm(request.form)
        formMeasure = forms.AddMeasurementForm(request.form)
        formSeq = forms.ModifySequenceForm(request.form)
        formMVal = forms.InsertMeasurementForm(request.form)
        formFile = forms.CSVFileUpload(request.form)

        
        #seqList=queries.getAllSequences()

        if(request.method == 'POST'):

                #print(request.form)
                #print(formMVal.validate())
        

                if(request.form["btn"] == "condition" and formCond.validate()):
                        print("Do Condition Insert")
                elif(request.form["btn"] == "measure" and formMeasure.validate()):
                        print("Do measure Insert")
                elif(request.form["btn"] == "sequence" and formSeq.validate()):
                        print("Do sequence modify")
                elif(request.form["btn"] =="mVal" and formMVal.validate()):
                        print("Do mval insert")
                        #resultSet of form submission
                        sequence = formMVal.sequence.data
                        measurement = formMVal.measurement.data
                        mVal = formMVal.value.data
                        print(sequence)
                        print(measurement)
                        print(mVal)
                        conditionList = formMVal.getConditions()
                        print(conditionList)
                        
                        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq, formMVal=formMVal, formFile=formFile)
                        
                        #insertion into database

                elif(request.form["btn"] == "addCond"):
                        formMVal.addCondition()
                        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq, formMVal=formMVal, showMeasure="true",formFile=formFile)
                elif(request.form["btn"] == "fileUpload" and formFile.validate()):
                        print("file upload")
                        if(forms.validateFile(request.files["file"])):
                                flash("File Uploaded Successfully","success")
                        else:
                                flash("File Failed to Upload. Invalid File Type!","failed")

                        
        
        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq, formMVal=formMVal,formFile=formFile)

@app.route("/about", methods =["GET","POST"])
def aboutPage():
        return render_template("about.html")

if __name__ == "__main__":
    app.run()
